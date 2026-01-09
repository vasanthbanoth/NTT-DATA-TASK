from behave import *
from playwright.sync_api import sync_playwright, expect

# --- Browser Fixture ---
# In a real Behave project, this goes in environment.py, 
# but for a single-file demo script, we hack it here or rely on the step opening it.

@given('the user navigates to "{url}"')
def step_open_url(context, url):
    # Start browser if not already started
    if not hasattr(context, 'playwright'):
        context.playwright = sync_playwright().start()
        context.browser = context.playwright.chromium.launch(headless=False, slow_mo=1000) # slow_mo makes it visible
        context.page = context.browser.new_page()
    context.page.goto(url)

@when('the user enters "{text}" into the "{selector}" field')
def step_enter_text(context, text, selector):
    # Heuristic: Try finding by ID first, then Placeholder, then Name
    page = context.page
    try:
        page.fill(f"#{selector}", text)
    except:
        try:
            page.get_by_placeholder(selector).fill(text)
        except:
            # Fallback: fuzzy match placeholder
            page.get_by_role("textbox", name=selector).fill(text)

@when('clicks the "{button_name}" button')
def step_click_btn(context, button_name):
    # Generic button clicker
    try:
        context.page.get_by_role("button", name=button_name).click()
    except:
        # Fallback for non-standard buttons (divs/spans)
        context.page.locator(f"text={button_name}").click()

@then('the user should see "{text}"')
def step_verify_text(context, text):
    expect(context.page.get_by_text(text)).to_be_visible()

# Cleanup (Optional hook if we had environment.py)
# For this script, the browser closes when the script ends.
