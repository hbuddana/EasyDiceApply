from src.automation import DiceAutomation
from src.utils.webdriver_setup import setup_driver

def main(username, password, keyword, max_applications):
    driver = None
    try:
        # Setup WebDriver
        driver, wait = setup_driver()
        
        # Create automation instance
        automation = DiceAutomation(
            driver=driver,
            wait=wait,
            username=username,
            password=password,
            keyword=keyword,
            max_applications=max_applications
        )
        
        # Run the automation
        automation.run()
        
        print("\nPress Enter to close the browser...")
        input()
        
    except Exception as e:
        print(f"\nScript failed with error: {str(e)}")
    finally:
        if driver:
            driver.quit()
