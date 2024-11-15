from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import RESUME_SETTINGS
import time
from selenium.webdriver.common.action_chains import ActionChains

class JobHandler:
    def __init__(self, driver, wait, shadow_dom_handler, status_callback=None):
        self.driver = driver
        self.wait = wait
        self.shadow_dom_handler = shadow_dom_handler
        self.status_callback = status_callback

    def update_status(self, message, status="running"):
        """Update status for UI"""
        if self.status_callback:
            self.status_callback({
                "message": message,
                "status": status
            })
        print(message)

    def replace_resume(self):
        """Find and click replace button, then upload new resume"""
        try:
            self.update_status("Looking for resume replace button...")
            try:
                replace_button = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//button[contains(@class, 'file-remove')]//span[text()='Replace']/.."
                )))
            except:
                try:
                    replace_button = self.wait.until(EC.element_to_be_clickable((
                        By.CSS_SELECTOR, "div.file-interactions button"
                    )))
                except:
                    replace_button = self.wait.until(EC.element_to_be_clickable((
                        By.CSS_SELECTOR, "button.file-remove"
                    )))

            self.update_status("Clicking replace button...")
            replace_button.click()
            time.sleep(2)

            # Look for file input after clicking replace
            self.update_status("Looking for file input...")
            file_input = self.wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "input[type='file']"
            )))
            
            self.update_status(f"Uploading resume from: {RESUME_SETTINGS['path']}")
            file_input.send_keys(RESUME_SETTINGS['path'])
            time.sleep(3)  # Wait for file to attach

            # Click the Upload button using the exact selector from the page 
            self.update_status("Looking for Upload button...")
            try:
                upload_button = self.wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, "span.fsp-button.fsp-button--primary.fsp-button-upload[data-e2e='upload']"
                )))
                self.update_status("Found Upload button, clicking...")
                upload_button.click()
            except:
                try:
                    # Backup method using JavaScript if the direct click fails
                    self.driver.execute_script("""
                        const uploadButton = document.querySelector('span.fsp-button-upload[data-e2e="upload"]');
                        if (uploadButton) {
                            uploadButton.click();
                            return true;
                        }
                        return false;
                    """)
                    self.update_status("Clicked Upload button using JavaScript")
                except Exception as e:
                    self.update_status(f"Failed to click Upload button: {str(e)}", "error")
                    return False

            time.sleep(3)  # Wait for upload to complete
            self.update_status("Resume replacement successful!")
            return True

        except Exception as e:
            self.update_status(f"Error replacing resume: {str(e)}", "error")
            return False

    def apply_to_job(self):
        """Handle the application process for a single job"""
        new_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_tab)
        
        try:
            self.update_status("Waiting for page to load completely...")
            time.sleep(7)
            
            if self.shadow_dom_handler.find_and_click_easy_apply():
                time.sleep(2)
                
                # Replace resume
                self.update_status("Attempting to replace resume...")
                if not self.replace_resume():
                    self.update_status("Warning: Resume replacement failed, continuing with existing resume...", "warning")
                
                # Click Next
                self.update_status("Looking for Next button...")
                next_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//span[text()='Next']")
                ))
                self.update_status("Clicking Next button...")
                next_button.click()
                time.sleep(2)
                
                # Click Submit
                self.update_status("Looking for Submit button...")
                submit_button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.seds-button-primary.btn-next")
                ))
                self.update_status("Clicking Submit button...")
                submit_button.click()
                time.sleep(2)
                
                self.update_status("Successfully applied to job!", "success")
                return True
            else:
                self.update_status("Skipping job - already applied or not available for easy apply", "skipped")
                return False
                
        except Exception as e:
            self.update_status(f"Could not process job: {str(e)}", "error")
            return False
        finally:
            self.update_status("Closing job tab...")
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)