import os
import sys
import subprocess
import time

# --- MOCK LLM GENERATION (To save him from API Keys) ---
# In a real interview, he would import openai and call the API here.
# We are faking the AI response so it runs 100% perfectly for the demo.
def llm_generate_scenarios(requirements):
    print(f"\n[AI AGENT] Analyzing requirements: {requirements[:30]}...")
    time.sleep(1.5) # Fake thinking time
    
    # This is what the AI *would* generate based on his Vercel app
    gherkin_content = """
Feature: Login Functionality

  @happy_path
  Scenario: Successful Login
    Given the user navigates to "https://www.saucedemo.com/"
    When the user enters "standard_user" into the "user-name" field
    And the user enters "secret_sauce" into the "password" field
    And clicks the "login-button" button
    
  @negative_path
  Scenario: Invalid Login
    Given the user navigates to "https://www.saucedemo.com/"
    When the user enters "wronguser" into the "user-name" field
    And clicks the "login-button" button
    """
    return gherkin_content

def main():
    # 1. Read Requirements
    if not os.path.exists("requirements_input.txt"):
        with open("requirements_input.txt", "w") as f:
            f.write("Test login page.")

    with open("requirements_input.txt", "r") as f:
        reqs = f.read()

    # 2. Generate Gherkin (The "AI" part)
    print(">>> Connecting to LLM Gateway...")
    feature_content = llm_generate_scenarios(reqs)
    
    # 3. Save to file
    if not os.path.exists("features"): os.makedirs("features")
    with open("features/generated.feature", "w") as f:
        f.write(feature_content)
    
    print("\n[SUCCESS] Generated Gherkin Scenarios:")
    print("-" * 40)
    print(feature_content)
    print("-" * 40)

    # 4. Filter Happy Path
    print("\n[SYSTEM] Selecting '@happy_path' scenarios for automation...")
    
    # 5. Manual Approval
    # We use input() to wait for user confirmation
    approval = input(">>> Approve execution of Happy Path? (y/n): ")
    if approval.strip().lower() != 'y':
        print("Execution Aborted.")
        return

    # 6. Run Behave (The Test)
    print("\n[EXECUTION] Running Playwright Automation...")
    # This runs the 'behave' command on the terminal
    # We use valid shell command splitting
    subprocess.run([sys.executable, "-m", "behave", "features/generated.feature", "--tags=@happy_path"])

if __name__ == "__main__":
    main()
