import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import logging

def setup_logging():
    logging.basicConfig(filename='scraped_data.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    setup_logging()

    # Setting scraper to its initial position
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("useAutomationExtension", False) 

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    URL = 'https://openai.com'
    driver.get(URL)
    
    try:
        # Locate the desired "Learn More" link
        attributes = driver.find_elements(By.XPATH, "//div[@data-slide-index='3']//a[@href]")
        if attributes:
            wanted_URL = attributes[0].get_attribute("href")
            logging.info(f"Found URL: {wanted_URL}")
            
            # Click on the link
            driver.execute_script("arguments[0].click();", attributes[0])
            time.sleep(3)  # Wait for the page to load
            
            # Fetch data from the new page (example: fetching page title)
            page_title = driver.title
            logging.info(f"Page Title: {page_title}")
            
            # You can add more code here to extract other data as needed
            
            # Save the data to the log file
            with open('scraped_data.log', 'a') as log_file:
                log_file.write(f"URL: {wanted_URL}\n")
                log_file.write(f"Page Title: {page_title}\n")
                log_file.write("\n")
        
        else:
            logging.error("No 'Learn More' link found in the specified div.")
    
    except NoSuchElementException as e:
        logging.error(f"Element not found: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
