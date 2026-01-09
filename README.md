# 🎯 NTT DATA - AI-Powered BDD Testing Platform

A modern web application that combines **AI-generated test scenarios** with **automated browser testing** using Behavior-Driven Development (BDD) principles.

![NTT DATA](https://img.shields.io/badge/NTT%20DATA-Platform-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Web%20App-green?style=for-the-badge)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?style=for-the-badge)

---

## 🚀 Features

- **🔐 Secure Login Portal**: Modern authentication interface with NTT DATA branding
- **🤖 AI Scenario Generation**: Convert business requirements into Gherkin test scenarios
- **🎭 Automated Testing**: Execute tests using Playwright and Behave
- **🎨 Modern UI**: Dark theme with glassmorphism effects and smooth animations
- **☁️ Cloud-Ready**: Optimized for Vercel deployment

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for deployment)

---

## 🛠️ Local Development

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/vasanthbanoth/NTT-DATA-TASK.git
cd NTT-DATA-TASK
\`\`\`

### 2. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
playwright install
\`\`\`

### 3. Run the Application

\`\`\`bash
python app.py
\`\`\`


---

## 🌐 Vercel Deployment

### Quick Deploy

1. **Push to GitHub**:
   \`\`\`bash
   git add .
   git commit -m "Deploy to Vercel"
   git push origin main
   \`\`\`

2. **Connect to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will automatically detect the configuration from `vercel.json`
   - Click "Deploy"

### Environment Configuration

The application is configured for Vercel deployment with:
- **Build Command**: Automatic (handled by `@vercel/python`)
- **Output Directory**: `.vercel`
- **Install Command**: `pip install -r requirements.txt`

> **Note**: Playwright browser automation may have limitations on serverless platforms. For full testing capabilities, consider deploying to a platform with persistent runtimes.

---

## 📁 Project Structure

\`\`\`
NTT_Task/
├── app.py                    # Flask application (WSGI entry point)
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel deployment configuration
├── static/                  # Static assets (images, logos)
│   ├── background.png
│   └── ntt_logo.png
├── templates/               # HTML templates
│   ├── login.html
│   └── dashboard.html
└── features/                # BDD test scenarios
    └── steps/
\`\`\`

---

## 🔧 Tech Stack

- **Backend**: Flask (Python Web Framework)
- **Testing**: Behave (BDD) + Playwright (Browser Automation)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel (Serverless Functions)
- **Version Control**: Git + GitHub

---

## 📸 Screenshots

### Login Page
Modern authentication portal with NTT DATA branding and secure entry point.

### Dashboard
AI-powered test generation interface with real-time scenario execution.

---

## 🔗 Links

- **Live Demo**: [Deploy to see your URL]
- **Repository**: [https://github.com/vasanthbanoth/NTT-DATA-TASK](https://github.com/vasanthbanoth/NTT-DATA-TASK)
- **Documentation**: See this README

---

## 👨‍💻 Development

### Running Tests Locally

\`\`\`bash
# Install Playwright browsers
playwright install

# Run behave tests
behave features/
\`\`\`

### Debugging

The Flask app runs with debug mode enabled locally. Check console output for errors.

---

## 📝 License

This project is part of NTT DATA's technical assessment.

---

## 👤 Author

**Vasanth Banoth**

- GitHub: [@vasanthbanoth](https://github.com/vasanthbanoth)
- Repository: [NTT-DATA-TASK](https://github.com/vasanthbanoth/NTT-DATA-TASK)

---

## 🙏 Acknowledgments

Built for NTT DATA technical assessment, showcasing AI-powered testing automation and modern web development practices.

---

*Created with ❤️ by Vasanth Banoth*
