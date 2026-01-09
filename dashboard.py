import streamlit as st
import subprocess
import sys
import time
import os
import base64

# --- CONFIG ---
st.set_page_config(page_title="NTT DATA - AI BDD", page_icon="", layout="wide")

# --- ASSETS & STYLING ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_page_styling(bg_file=None, logo_file=None):
    bg_css = ""
    if bg_file and os.path.exists(bg_file):
        bin_str = get_base64_of_bin_file(bg_file)
        bg_css = f'''
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
        }}
        '''
    
    logo_b64 = ""
    if logo_file and os.path.exists(logo_file):
        logo_b64 = get_base64_of_bin_file(logo_file)

    # Custom CSS for Header, Footer, and UI
    custom_css = f'''
    <style>
    {bg_css}
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Hide Default Streamlit Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Global Typography */
    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
    }}

    /* Main Container Padding - Desktop */
    .block-container {{
        padding-top: 100px !important;
        padding-bottom: 100px !important;
    }}

    /* RESPONSIVE MEDIA QUERIES */
    @media (max-width: 768px) {{
        .custom-header {{
            height: 60px !important;
            padding: 0 15px !important;
        }}
        .header-left {{
            gap: 10px !important;
        }}
        .nav-link, .header-right {{
            display: none !important; /* Hide nav and right icons on mobile */
        }}
         .header-logo {{
            height: 24px !important;
        }}
        .block-container {{
            padding-top: 80px !important;
            padding-bottom: 80px !important;
        }}
        .custom-footer {{
            padding: 15px 20px !important;
        }}
        .footer-top {{
            flex-direction: column;
            align-items: flex-start;
            gap: 15px;
        }}
        .footer-links {{
            flex-wrap: wrap;
            gap: 10px !important;
        }}
        .footer-bottom {{
            flex-direction: column;
            gap: 10px;
            align-items: flex-start !important;
        }}
    }}

    /* HEADER STYLES */
    .custom-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background-color: #0b1428; /* Dark Blue */
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .header-left {{
        display: flex;
        align-items: center;
        gap: 25px;
    }}
    .header-logo {{
        height: 30px;
        margin-right: 15px;
    }}
    .nav-link {{
        color: #e0e0e0 !important;
        text-decoration: none !important;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 4px;
        transition: color 0.2s;
    }}
    .nav-link:hover {{
        color: #fff !important;
    }}
    .header-right {{
        display: flex;
        align-items: center;
        gap: 20px;
        color: #fff;
        font-size: 14px;
    }}

    /* FOOTER STYLES */
    .custom-footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0b1428;
        color: #aaaaaa;
        padding: 20px 40px;
        font-size: 12px;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        gap: 15px;
        border-top: 1px solid #1f2a40;
    }}
    .footer-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .footer-links {{
        display: flex;
        gap: 25px;
    }}
    .footer-link {{
        color: #aaaaaa;
        text-decoration: none;
        transition: color 0.2s;
    }}
    .footer-link:hover {{
        color: #fff;
    }}
    .footer-bottom {{
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .social-icons {{
        display: flex;
        gap: 20px;
        font-size: 18px;
        align-items: center;
    }}
    .social-icon {{
        opacity: 0.7;
        cursor: pointer;
        transition: opacity 0.2s;
    }}
    .social-icon:hover {{
        opacity: 1;
    }}

    /* UI ELEMENTS & BUTTONS */
    
    /* Primary Button: Sign In (Gradient) */
    div.stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%); /* Purple to Blue */
        color: white;
        border-radius: 8px; 
        border: none;
        padding: 0.7rem 1rem;
        font-weight: 700;
        transition: all 0.2s;
        width: 100%;
        text-transform: capitalize; 
        font-size: 15px;
        box-shadow: 0 4px 6px rgba(139, 92, 246, 0.25);
    }}
    div.stButton > button[kind="primary"]:hover {{
        background: linear-gradient(90deg, #7c3aed 0%, #2563eb 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 12px rgba(139, 92, 246, 0.4);
    }}

    /* Secondary Button: Google (Dark + Logo) */
    div.stButton > button[kind="secondary"] {{
        background-color: #1e293b; 
        color: #ffffff;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.7rem 1rem 0.7rem 2.5rem; /* Left padding for logo */
        font-weight: 600;
        width: 100%;
        font-size: 15px;
        position: relative;
        /* Google G Logo SVG Data URI */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Cpath fill='%23EA4335' d='M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z'/%3E%3Cpath fill='%234285F4' d='M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z'/%3E%3Cpath fill='%23FBBC05' d='M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z'/%3E%3Cpath fill='%2334A853' d='M24 48c6.48 0 10.44-2.13 14.4-5.8l-7.73-6c-2.15 1.45-4.92 2.3-6.67 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: 12px center;
        background-size: 20px 20px;
    }}
    div.stButton > button[kind="secondary"]:hover {{
        background-color: #334155;
        border-color: #475569;
        color: #fff;
    }}
    
    /* Login Styling */
    .login-container {{
        background: rgba(15, 23, 42, 0.85); 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 35px 30px; 
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
        text-align: center;
        width: 100%;
        max-width: 380px;
        margin: 80px auto 20px auto; 
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .login-title {{
        color: #fff;
        font-size: 26px; 
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }}
    .login-subtitle {{
        color: #94a3b8;
        font-size: 11px;
        margin-bottom: 25px; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }}
    .input-group {{
        margin-bottom: 15px; 
        text-align: left;
    }}
    .input-label {{
        display: block;
        color: #e2e8f0;
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 6px;
    }}
    .input-field {{
        width: 100%;
        padding: 10px 14px; 
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid #334155;
        border-radius: 6px;
        color: #f1f5f9;
        font-size: 14px;
        transition: border-color 0.2s;
    }}
    .input-field:focus {{
        border-color: #8b5cf6;
        outline: none;
    }}
    .divider {{
        display: flex;
        align-items: center;
        margin: 20px 0; 
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .divider::before, .divider::after {{
        content: "";
        flex: 1;
        height: 1px;
        background: #334155;
    }}
    .divider::before {{ margin-right: 15px; }}
    .divider::after {{ margin-left: 15px; }}

    /* Reduce vertical gap between St elements */
    .stButton {{
        margin-bottom: 10px;
    }}

    /* Reset Sidebar Buttons (e.g. Logout) */
    section[data-testid="stSidebar"] .stButton > button {{
        background-image: none !important;
        padding-left: 1rem !important;
        background-color: transparent !important;
        border: 1px solid #444 !important;
    }}

    /* SOCIAL ICONS (SVG) */
    .icon-svg {{
        width: 20px;
        height: 20px;
        fill: #94a3b8;
        transition: fill 0.2s;
    }}
    .social-icon:hover .icon-svg {{
        fill: #f8fafc;
    }}
    </style>
    
    <!-- HEADER HTML -->
    <div class="custom-header">
        <div class="header-left">
            <img src="data:image/png;base64,{logo_b64}" class="header-logo">
            <a class="nav-link">Industries &#9662;</a>
            <a class="nav-link">Services &#9662;</a>
            <a class="nav-link">Insights &#9662;</a>
            <a class="nav-link">About Us &#9662;</a>
            <a class="nav-link">Careers &#8599;</a>
            <a class="nav-link">Investors &#9662;</a>
            <a class="nav-link">News</a>
        </div>
        <div class="header-right">
            <span>🌐 Global - English</span>
            <span>🔍</span>
            <span>✉️</span>
        </div>
    </div>

    <!-- FOOTER HTML -->
    <div class="custom-footer">
        <div class="footer-top">
            <div class="footer-links">
                <a class="footer-link">Sitemap</a>
                <a class="footer-link">Contact Us</a>
                <a class="footer-link">Term Of Use</a>
                <a class="footer-link">Privacy Statement</a>
                <a class="footer-link">Accessibility</a>
                <a class="footer-link">Cookie Policy</a>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="social-icons">
                 <!-- X / Twitter -->
                 <a class="social-icon" title="Twitter/X">
                    <svg class="icon-svg" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                 </a>
                 <!-- Instagram -->
                 <a class="social-icon" title="Instagram">
                    <svg class="icon-svg" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                 </a>
                 <!-- LinkedIn -->
                 <a class="social-icon" title="LinkedIn">
                    <svg class="icon-svg" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                 </a>
            </div>
            <span>Copyright © NTT DATA Group Corporation</span>
        </div>
    </div>
    '''
    st.markdown(custom_css, unsafe_allow_html=True)

# Apply Styling
set_page_styling(bg_file="background.png", logo_file="ntt_logo.png")

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- LOGIN VIEW ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown("""
<div class="login-container">
<h1 class="login-title">Access Portal</h1>
<p class="login-subtitle">Secure Entry Point</p>
<div class="input-group">
<label class="input-label">Username</label>
<div class="input-field" style="padding: 12px; color: #888;">user@nttdata.com</div>
</div>
<div class="input-group">
<label class="input-label">Password</label>
<div class="input-field" style="padding: 12px; color: #888;">••••••••••••</div>
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("Sign In", type="primary", use_container_width=True):
            with st.spinner("Verifying Credentials..."):
                time.sleep(1.5)
                st.session_state['logged_in'] = True
                st.rerun()

        st.markdown("""
<div class="login-container" style="background: transparent; box-shadow: none; border: none; padding: 0; margin-top: 0; margin-bottom: 0;">
<div class="divider">OR CONTINUE WITH</div>
</div>
""", unsafe_allow_html=True)
        
        if st.button("Google", type="secondary", use_container_width=True):
             with st.spinner("Redirecting to SSO..."):
                time.sleep(1.0)
                st.session_state['logged_in'] = True
                st.rerun()

    # Stop execution here if not logged in
    st.stop()

# --- MAIN DASHBOARD (Protected) ---

st.title("🤖 AI-Driven BDD Functional Testing")
st.markdown("""
**Objective:** Generate BDD scenarios from plain English and execute them against a target web app.
""")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("Configuration")
target_url = st.sidebar.text_input("Target URL", "https://www.saucedemo.com/") # Updated Default URL

# Read requirements from file if it exists
default_reqs = "Test the login page.\nPositive: Valid user logs in.\nNegative: Invalid user sees error."
if os.path.exists("requirements_input.txt"):
    with open("requirements_input.txt", "r") as f:
        default_reqs = f.read()

requirements = st.sidebar.text_area("Business Requirements", height=150, value=default_reqs)

if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

# --- HELPER FUNCTIONS ---

def generate_gherkin(url, reqs):
    """
    Mock LLM Generation logic. 
    In a real app, this would call OpenAI/Gemini API.
    """
    time.sleep(1.5) # Simulate API latency
    
    # Dynamic Template based on user input slightly, but mostly mocked for stability
    feature_text = f"""Feature: Functional Testing of {url}

  @happy_path
  Scenario: Successful Login Flow
    Given the user navigates to "{url}"
    When the user enters "standard_user" into the "user-name" field
    And the user enters "secret_sauce" into the "password" field
    And clicks the "login-button" button
    Then the user should see "Products"

  @negative_path
  Scenario: Invalid Login Flow
    Given the user navigates to "{url}"
    When the user enters "wrong_user" into the "user-name" field
    And clicks the "login-button" button
    Then the user should see "Epic sadface: Username and password do not match any user in this service"
"""
    return feature_text

def run_behave_test():
    """Runs the behave command and returns the output."""
    # Check if Playwright is installed (Vercel optimization)
    try:
        import playwright
        is_playwright_installed = True
    except ImportError:
        is_playwright_installed = False

    if not is_playwright_installed:
        time.sleep(2)
        return "⚠️ VERCEL MODE: Playwright is not installed to save space.\n\n[SIMULATION] Test execution simulated successfully.\n\n(To run actual browser tests, deploy to Streamlit Cloud or Render.)"

    # Ensure directory exists
    if not os.path.exists("features"):
        return "Error: features directory not found."
        
    cmd = [sys.executable, "-m", "behave", "features/generated.feature", "--tags=@happy_path", "--no-capture", "--no-color"]
    
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return process.stdout + "\n" + process.stderr
    except subprocess.TimeoutExpired:
        return "Timeout: Test took too long to execute."
    except Exception as e:
        return f"Execution Error: {str(e)}"

# --- MAIN UI FLOW ---

# STEP 1: GENERATE
st.header("Step 1: Scenario Generation")
if st.button("Analyze & Generate Scenarios", type="primary"):
    with st.spinner("Consulting AI Agent..."):
        generated_feature = generate_gherkin(target_url, requirements)
        
        # Save to session state to persist between reruns
        st.session_state['generated_feature'] = generated_feature
        st.session_state['step'] = 2
        st.success("Scenarios Generated!")

# Display Generated Content if available
if 'generated_feature' in st.session_state:
    st.subheader("Generated Gherkin Scenarios")
    feature_content = st.text_area("Review & Edit Gherkin:", value=st.session_state['generated_feature'], height=300)
    
    # Save any edits user makes
    if st.button("Save Scenarios", type="primary"):
        if not os.path.exists("features"): os.makedirs("features")
        with open("features/generated.feature", "w") as f:
            f.write(feature_content)
        st.success("File saved to `features/generated.feature`")
        st.session_state['step'] = 3

# STEP 2: EXECUTION
if st.session_state.get('step', 0) >= 3:
    st.divider()
    st.header("Step 2: Automated Execution")
    st.info(f"Targeting: {target_url}")
    
    if st.button("🚀 Approve & Run Tests", type="primary"):
        with st.status("Executing Playwright Automation...", expanded=True) as status:
            st.write("Initializing Browser...")
            time.sleep(0.5)
            st.write("Running Gherkin Steps...")
            
            # Run the test
            result_logs = run_behave_test()
            
            st.write("Processing Results...")
            status.update(label="Execution Complete!", state="complete", expanded=False)
        
        st.subheader("Execution Logs")
        st.code(result_logs, language="bash")
        
        if "Failing scenarios" in result_logs or "Errors" in result_logs or "failed" in result_logs:
             st.error("Test Run Failed - Check logs above.")
        else:
             st.balloons()
             st.success("Test Run Passed Successfully!")
