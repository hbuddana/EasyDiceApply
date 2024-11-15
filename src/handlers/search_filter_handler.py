from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class SearchAndFilter:
    def __init__(self, driver, wait, filters=None):
        self.driver = driver
        self.wait = wait
        # Initialize filters with user preferences or empty dict
        self.filters = filters if filters is not None else {}

    def perform_search(self, keyword):
        """Check for search box, reveal if needed, and perform search"""
        print("Checking for search box...")
        search_input = None
        
        try:
            # First try to find the search input directly
            try:
                search_input = self.wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    "input[placeholder='Job title, Keywords, Company']"
                )))
                print("Search box found directly")
            except Exception:
                print("Search box not immediately visible")
                try:
                    # Try direct navigation to jobs page
                    print("Navigating to jobs page...")
                    self.driver.get("https://www.dice.com/jobs")
                    time.sleep(3)
                    
                    # Wait for search input with exact selector
                    print("Waiting for search box to appear...")
                    search_input = self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        "input#typeaheadInput[data-cy='typeahead-input']"
                    )))
                    print("Search box found after navigation")
                    
                except Exception:
                    # If direct navigation fails, try shadow DOM approach
                    print("Trying shadow DOM navigation...")
                    self.driver.execute_script("""
                        const header = document.querySelector('dhi-seds-nav-header');
                        const shadowRoot1 = header.shadowRoot;
                        const technologist = shadowRoot1.querySelector('dhi-seds-nav-header-technologist');
                        const shadowRoot2 = technologist.shadowRoot;
                        const display = shadowRoot2.querySelector('dhi-seds-nav-header-display');
                        const shadowRoot3 = display.shadowRoot;
                        const searchLink = shadowRoot3.querySelector('a[href*="/jobs"]');
                        if (searchLink) {
                            searchLink.click();
                            return true;
                        }
                        return false;
                    """)
                    
                    print("Clicked Search Jobs link, waiting for page load...")
                    time.sleep(5)
                    
                    search_input = self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        "input#typeaheadInput[data-cy='typeahead-input']"
                    )))
            
            if search_input:
                # Perform the search
                print(f"Entering search keyword: {keyword}")
                search_input.clear()
                time.sleep(1)
                
                # Type the keyword character by character
                for char in keyword:
                    search_input.send_keys(char)
                    time.sleep(0.1)
                
                time.sleep(1)
                search_input.send_keys(Keys.RETURN)
                time.sleep(3)
                
                # Wait for results to load
                try:
                    self.wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        "a[data-cy='card-title-link']"
                    )))
                except Exception:
                    # Additional wait if needed
                    time.sleep(5)
                
                print("Search initiated successfully")
                return True
            else:
                print("Failed to find search input")
                return False
            
        except Exception as e:
            print(f"Error during search: {str(e)}")
            return False

    def apply_filters(self):
        """Apply filters based on user preferences"""
        try:
            print(f"Applying filters: {self.filters}")  # Debug: Show filter contents
            filters_applied = False

            # Apply Today filter only if selected
            if self.filters.get('today_only', False):
                print("Applying Today filter...")
                try:
                    today_button = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//button[@role='radio' and contains(text(), 'Today')]"
                    )))
                    self.driver.execute_script("arguments[0].click();", today_button)
                    time.sleep(2)
                    filters_applied = True
                    print("Today filter applied successfully")
                except Exception as e:
                    print(f"Error applying Today filter: {str(e)}")
            else:
                print("Today filter not selected, skipping...")

            # Apply Third Party filter only if selected
            if self.filters.get('third_party', False):
                print("Applying Third Party filter...")
                try:
                    third_party_button = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//button[@role='checkbox' and @aria-label='Filter Search Results by Third Party']"
                    )))
                    self.driver.execute_script("arguments[0].click();", third_party_button)
                    time.sleep(2)
                    filters_applied = True
                    print("Third Party filter applied successfully")
                except Exception as e:
                    print(f"Error applying Third Party filter: {str(e)}")
            else:
                print("Third Party filter not selected, skipping...")

            if not self.filters:
                print("No filters selected, continuing without filters")
                return True

            return filters_applied or not self.filters
            
        except Exception as e:
            print(f"Error applying filters: {str(e)}")
            return False