# Bug Report AI Assistant 🐞⚡
An intelligent, AI-powered system designed to streamline bug tracking, triage, and root-cause analysis. By leveraging natural language processing and modern LLM workflows, this assistant transforms unstructured bug reports and error logs into structured, actionable developer insights in seconds.

# 🌟 Key Features
🤖 Automated Bug Analysis: Parses raw bug descriptions, tracebacks, and error logs to identify core issues instantly.

🏷️ Smart Categorization & Tagging: Automatically assigns priority levels (e.g., Critical, High, Low), component tags, and issue types.

🔎 Root-Cause Suggestion: Highlights likely root causes and provides initial debugging steps for engineering teams.

⚡ Glassmorphism / Sleek UI: Clean, modern interface optimized for seamless user interaction and rapid issue reporting.

🔗 Developer Framework Ready: Easy integration into existing API pipelines, CI/CD workflows, or project management systems.

🏗️ Architecture Overview

                       User / Client UI
                            |
                      FastAPI Backend     
            --------------|        |-------------- 
            |                                    |
    LLM & Prompt Chains               Context & Data Store  
  (LangChain / APIs)                    (Structured JSON/DB) 


# 🛠️ Tech Stack
Frontend: HTML5, CSS3 / Modern Glassmorphism UI, JavaScript

Backend Framework: Python / FastAPI (or Flask)

AI & Orchestration: LangChain / LLM APIs / Prompt Engineering Pipelines

Environment & Version Control: Git, Python Virtual Environment (venv)

# 🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

Prerequisites
Python: 3.9 or higher

Git: Installed on your system

An active API key (e.g., OpenAI, Groq, or Gemini API depending on your configured provider)

# Installation & Setup
1. Clone the Repository
   git clone https://github.com/TheMaryamIsmail/Bug-Report-AI-Assistant.git
   cd Bug-Report-AI-Assistant
2. Create & Activate Virtual Environment
   1. On Windows:
      python -m venv venv
      venv\Scripts\activate
   2. On macOS/Linux
      python3 -m venv venv
      source venv/bin/activate
3. Install Dependencies
   pip install -r requirements.txt
4. Environment Configuration
   Create a .env file in the root directory and add your API credentials:
   API_KEY=your_llm_api_key_here
   PORT=8000
5. Run the Application

  Bash
  python main.py
  or
  uvicorn main:app --reload
6. Access the Web Interface
  Open your browser and navigate to:
 

# 📖 Usage Guide
Submit Bug Details: Paste the raw error log, terminal output, or a user-reported bug description into the input interface.

Analyze Issue: Click Analyze Bug to initiate the AI processing chain.

Review Output: Receive a structured breakdown containing:

Issue Title & Summary

Severity Level

Affected System Component

Recommended Fix / Next Steps

# 🛣️ Roadmap & Future Enhancements
[ ] Add direct integration with GitHub Issues & Jira APIs.

[ ] Implement multi-file code snippet context analysis.

[ ] Support vector-based similarity search for duplicate bug detection.

[ ] Expand multi-language exception parsing.

# 🤝 Contributing
Contributions, issues, and feature requests are welcome!

Fork the project repository.

Create your feature branch: git checkout -b feature/AmazingFeature

Commit your changes: git commit -m 'Add some AmazingFeature'

Push to the branch: git push origin feature/AmazingFeature

Open a Pull Request.

# 📜 License
Distributed under the MIT License. See LICENSE for more information.

# 👩‍💻 Author
## Maryam Ismail

# GitHub: @TheMaryamIsmail
  
