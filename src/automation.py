from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from .handlers.shadow_dom_handler import ShadowDOMHandler
from .handlers.job_handler import JobHandler
from .handlers.search_filter_handler import SearchAndFilter

class DiceAutomation:
    def __init__(self, driver, wait, username, password, keyword, max_applications, filters=None, status_callback=None):
        self.driver = driver
        self.wait = wait
        self.username = username
        self.password = password
        self.search_keyword = keyword
        self.max_applications = max_applications
        self.filters = filters if filters is not None else {}
        self.status_callback = status_callback
        self.automation_status = {
            "status": "initializing",
            "message": "",
            "total_jobs": 0,
            "jobs_processed": 0,
            "applications_submitted": 0,
            "current_job": 0,
            "max_applications": max_applications
        }

    def update_status(self, message, status="running"):
        """Update automation status and notify UI"""
        self.automation_status["message"] = message
        self.automation_status["status"] = status
        if self.status_callback:
            self.status_callback(self.automation_status)
        print(message)

    def login(self):
        """Handle login process with improved verification."""
        try:
            self.update_status("Navigating to Dice login page...")
            self.driver.get("https://www.dice.com/dashboard/login")

            # Step 1: Wait for email input and enter username
            print("Waiting for email input field...")
            email_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Please enter your email']"))
            )
            email_input.clear()
            email_input.send_keys(self.username)
            email_input.send_keys(Keys.RETURN)
            print("Username entered successfully.")

            # Step 2: Wait for password input and enter password
            print("Waiting for password input field...")
            password_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            password_input.clear()
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            print("Password entered successfully.")

            # Step 3: Confirm successful login by checking for a unique dashboard element
            print("Checking for dashboard element to confirm successful login...")
            try:
                dashboard_element = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/profile']"))
                )
                if dashboard_element:
                    self.update_status("Login successful", "success")
                    print("Login confirmed successful.")
                    return True
            except Exception as e:
                print(f"Failed to find dashboard element: {e}")
                # Try alternative verification method
                try:
                    profile_menu = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-menu"))
                    )
                    if profile_menu:
                        self.update_status("Login successful", "success")
                        print("Login confirmed via profile menu.")
                        return True
                except:
                    pass
                
                return False

        except Exception as e:
            print(f"Login failed with error: {e}")
            self.update_status(f"Login failed: {str(e)}", "error")

            # Additional check for specific login error message
            try:
                error_element = self.driver.find_element(By.CSS_SELECTOR, "div.error-message")
                if error_element:
                    self.update_status("Invalid credentials provided.", "error")
                    print("Invalid credentials detected.")
            except:
                print("No specific error message found.")

            return False

    def get_job_listings(self):
        """Get all job listings from the current page"""
        try:
            # Wait for at least one job listing to be present
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[data-cy='card-title-link'].card-title-link")
            ))
            time.sleep(2)  # Additional wait for all listings to load
            
            # Find all job listings
            listings = self.driver.find_elements(By.CSS_SELECTOR, "a[data-cy='card-title-link'].card-title-link")
            self.automation_status["total_jobs"] = len(listings)
            self.update_status(f"Found {len(listings)} job listings")
            return listings
        except Exception as e:
            self.update_status(f"Error finding job listings: {str(e)}", "error")
            return []

    def run(self):
        """Main method to run the automation"""
        try:
            self.update_status("Starting automation...")

            # Initialize handlers
            search_filter = SearchAndFilter(self.driver, self.wait, filters=self.filters)
            shadow_dom_handler = ShadowDOMHandler(self.driver, self.wait)
            job_handler = JobHandler(self.driver, self.wait, shadow_dom_handler, self.status_callback)

            # Perform search with the keyword
            if not search_filter.perform_search(self.search_keyword):
                raise Exception("Search failed")
            print("Search completed successfully.")

            # Apply filters if specified
            if not search_filter.apply_filters():
                raise Exception("Filter application failed")
            print("Filters applied successfully.")

            applications_submitted = 0
            jobs_processed = 0
            job_index = 0

            while applications_submitted < self.max_applications and jobs_processed < 30:
                try:
                    job_listings = self.get_job_listings()
                    
                    if not job_listings or job_index >= len(job_listings):
                        self.update_status("No more jobs available to process", "completed")
                        break

                    self.automation_status["current_job"] = job_index + 1
                    self.update_status(f"Processing job {job_index + 1} of {len(job_listings)}")

                    # Click the job listing
                    listing = job_listings[job_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", listing)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", listing)
                    
                    if job_handler.apply_to_job():
                        applications_submitted += 1
                        self.automation_status["applications_submitted"] = applications_submitted
                        progress_percent = int((applications_submitted / self.max_applications) * 100)
                        self.update_status(f"Successfully applied to job {applications_submitted} of {self.max_applications} ({progress_percent}%)")
                    
                    jobs_processed += 1
                    self.automation_status["jobs_processed"] = jobs_processed
                    job_index += 1
                    time.sleep(1)
                    
                except Exception as e:
                    self.update_status(f"Error processing job: {str(e)}", "error")
                    jobs_processed += 1
                    job_index += 1
                    continue

            # Update final status
            if applications_submitted > 0:
                self.update_status(
                    f"Completed! Applied to {applications_submitted} out of {self.max_applications} target jobs",
                    "completed"
                )
            else:
                self.update_status("Completed - No applications submitted", "completed_no_applications")

            return {
                "success": True,
                "applications_submitted": applications_submitted,
                "jobs_processed": jobs_processed,
                "status": self.automation_status
            }

        except Exception as e:
            self.update_status(f"An error occurred: {str(e)}", "error")
            return {
                "success": False,
                "error": str(e),
                "status": self.automation_status
            }
