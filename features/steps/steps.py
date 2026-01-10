from behave import *
from playwright.sync_api import sync_playwright, expect
import time

# --- Browser Fixture ---
# In a real Behave project, this goes in environment.py, 
# but for a single-file demo script, we hack it here or rely on the step opening it.

@given('the user navigates to "{url}"')
def step_open_url(context, url):
    print(f"DEBUG: Navigating to {url}")
    # Determine if running on Vercel/CI or Local
    import os
    is_headless = os.environ.get('VERCEL') == '1' or os.environ.get('CI') == 'true'
    
    # Start browser if not already started
    if not hasattr(context, 'playwright'):
        context.playwright = sync_playwright().start()
        # Launch with arguments for better visibility
        context.browser = context.playwright.chromium.launch(
            headless=is_headless, 
            slow_mo=1000 if not is_headless else 0, # Faster on CI
            args=["--start-maximized"] if not is_headless else ["--no-sandbox", "--disable-dev-shm-usage"]
        )
        # Create context
        if not is_headless:
             context.context = context.browser.new_context(viewport={"width": 1280, "height": 720})
        else:
             context.context = context.browser.new_context()
             
        context.page = context.context.new_page()
    context.page.goto(url)

@when('the user enters "{text}" into the "{selector}" field')
def step_enter_text(context, text, selector):
    print(f"DEBUG: Entering '{text}' into '{selector}'")
    page = context.page
    try:
        page.fill(f"#{selector}", text)
    except:
        try:
            page.get_by_placeholder(selector).fill(text)
        except:
            page.get_by_role("textbox", name=selector).fill(text)

@when('clicks the "{button_name}" button')
def step_click_btn(context, button_name):
    print(f"DEBUG: Clicking button '{button_name}'")
    # Handle possible navigation triggered by click
    try:
        # If it's the login button, we expect navigation
        if "login" in button_name.lower():
            # Create a promise for navigation before clicking
            with context.page.expect_navigation(timeout=5000):
                try:
                    context.page.get_by_role("button", name=button_name).click()
                except:
                     context.page.locator(f"text={button_name}").click()
        else:
             try:
                context.page.get_by_role("button", name=button_name).click()
             except:
                context.page.locator(f"text={button_name}").click()
             
    except Exception as e:
        print(f"DEBUG: Click handled (navigation or error): {e}")

    # Small stability wait
    time.sleep(1)

@then('the user should see "{text}"')
def step_verify_text(context, text):
    print(f"DEBUG: Verifying text '{text}'")
    expect(context.page.get_by_text(text)).to_be_visible()

# Cleanup (Optional hook if we had environment.py)
# For this script, the browser closes when the script ends.
