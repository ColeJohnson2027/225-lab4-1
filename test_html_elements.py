from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import unittest

class TestH5Tag(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Ensures the browser window does not open
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_header_exists(self):
        driver = self.driver
        driver.get("http://10.48.229.168")

        header = driver.find_element(By.TAG_NAME, "h2").text
        
        self.assertIn("Add Contact", header)
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
