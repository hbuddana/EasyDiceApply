<a name="top"></a>
<div align="center">
<img src="./src/img/dice_logo.png" alt="Dice Logo" style="border-radius: 15px;">

# EasyDiceApply - Automated Job Application Tool 🚀

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-green.svg?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Flask](https://img.shields.io/badge/Flask-Web_UI-red.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./MIT%20License)
[![Contributors](https://img.shields.io/github/contributors/Deeraj7/EasyDiceApply)]()

**Automate your job application process on Dice.com with an easy-to-use web interface. Streamline your job search with one-click applications, intelligent filtering, and real-time status tracking.**

</div>

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Troubleshooting](#troubleshooting)
8. [Contributors](#contributors)
9. [License](#license)
10. [Disclaimer](#disclaimer)

---

## Introduction

**EasyDiceApply** is designed to make the job application process on Dice.com more efficient and less time-consuming. By automating repetitive tasks, it allows job seekers to focus on interview preparation and skill-building rather than filling out forms repeatedly. Built with Python, Selenium, and Flask, this tool includes features such as automatic job searching, one-click application, and real-time status tracking through a user-friendly web interface.

## ✨ Features

- 🌐 **Web-Based Interface**: User-friendly UI for easy interaction
- ✅ **Automated Login to Dice.com**
- 🔍 **Customizable Job Search**: Allows searching with specific keywords and filters
- 🎯 **Intelligent Filtering**: Only applies to relevant jobs (e.g., today's job postings, non-third-party listings)
- ⚡ **"Easy Apply" Automation**: One-click application submission for jobs with Easy Apply
- 🔄 **Smart Handling of Previously Applied Jobs**: Skips jobs that you've already applied to
- 💡 **Shadow DOM Interaction**: Interacts with modern web elements, including those hidden in Shadow DOM
- 📊 **Real-Time Status**: Live tracking of application progress
- 📁 **Resume Management**: Easy resume upload and handling

---

## 📂 Project Structure

```
EasyDiceApply/
├── README.md
├── requirements.txt
├── config.py
├── main.py
├── ui/
│   ├── app.py
│   ├── static/
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   └── status.js
│   │   └── css/
│   │       └── styles.css
│   └── templates/
│       ├── index.html
│       └── status.html
└── src/
    ├── automation.py
    ├── handlers/
    │   ├── job_handler.py
    │   ├── shadow_dom_handler.py
    │   └── search_filter_handler.py
    └── utils/
        └── webdriver_setup.py
```

## 📋 Requirements

- **Python 3.x**
- **Chrome Browser**
- **ChromeDriver** matching your Chrome version
- Required Python packages listed in `requirements.txt`

## ⚙️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Deeraj7/EasyDiceApply.git
   cd EasyDiceApply
   ```

2. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**
   Create a `config.py` file with your settings:
   ```python
   SEARCH_SETTINGS = {
       "max_applications": 10
   }

   RESUME_SETTINGS = {
       "allowed_extensions": {"pdf", "doc", "docx"},
       "max_file_size": 10 * 1024 * 1024
   }

   APP_SETTINGS = {
       "headless": False,
       "wait_timeout": 20
   }
   ```

## 🚀 Usage

1. Start the web interface:
   ```bash
   python ui/app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5001
   ```

3. In the web interface:
   - Upload your resume
   - Enter your Dice.com credentials
   - Set your job search preferences
   - Start the automation

## 🛠️ Troubleshooting

1. **Login Issues**
   - Double-check your credentials
   - Ensure your ChromeDriver version matches your installed Chrome browser version

2. **Application Process Stalls**
   - If the bot fails to click "Easy Apply," ensure that the jobs being targeted have the Easy Apply option
   - Check if resume upload is successful

3. **Shadow DOM Errors**
   - Ensure the `shadow_dom_handler.py` script is functioning correctly
   - Some web elements on Dice might require specific handling

4. **Rate Limiting on Dice**
   - Dice.com might limit requests if too many actions are performed quickly
   - The script includes delays to mimic human behavior, but further customization may be needed

## 👥 Contributors

[![Contributors](https://img.shields.io/github/contributors/Deeraj7/EasyDiceApply)]()

<div align="left">
  <a href="https://github.com/Deeraj7">
    <img src="https://avatars.githubusercontent.com/Deeraj7?s=100" width="50" height="50" style="border-radius: 50%;" alt="Deeraj7 (Owner)"/>
  </a>
  <a href="https://github.com/hbuddana">
    <img src="https://avatars.githubusercontent.com/hbuddana?s=100" width="50" height="50" style="border-radius: 50%;" alt="Harsha"/>
  </a>
</div>

## 📄 License

This project is licensed under the MIT License - see the [MIT License](./MIT%20License) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with Dice.com's terms of service. The developers are not responsible for any misuse or violation of Dice.com's terms of service.

---

[Back to top 🚀](#top)
