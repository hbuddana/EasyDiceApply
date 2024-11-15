# Job search default settings
SEARCH_SETTINGS = {
    "max_applications": 10,  # Default maximum applications
}

# Resume settings
RESUME_SETTINGS = {
    "allowed_extensions": {"pdf", "doc", "docx"},
    "max_file_size": 10 * 1024 * 1024,  # 10MB in bytes
    "upload_folder": "ui/uploads"    # Folder for uploaded resumes
}

# UI Configuration
UI_SETTINGS = {
    "port": 5000,
    "host": "localhost",
    "debug": True
}

# Application settings
APP_SETTINGS = {
    "headless": False,               # Run browser in headless mode
    "wait_timeout": 20,              # Default timeout for WebDriver wait
    "log_level": "INFO"             # Logging level
}

# Status messages
STATUS_MESSAGES = {
    "initializing": "Starting automation...",
    "login_success": "Successfully logged in",
    "login_failed": "Login failed",
    "search_failed": "Search failed",
    "filter_failed": "Failed to apply filters",
    "completed": "Automation completed successfully",
    "error": "An error occurred during automation"
}