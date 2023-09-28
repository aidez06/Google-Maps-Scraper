import csv
import json
import time
from urllib.parse import urlparse
import urllib.request
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



class Locator:

    def __init__(self, keyword) -> None:
        self.keyword = keyword
        self.url = f"https://www.google.com/maps/search/{self.keyword}"

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def keywords(self):
        # Open the .txt file in read mode
        file_path = 'keywords.txt'  # Replace with the actual file path
        with open(file_path, 'r') as file:
            keywords = file.readlines()
            return keywords

    def locator_start(self):
        information = []
        self.driver.get(self.url)
        search_box = WebDriverWait(self.driver,1000).until(
            EC.presence_of_element_located((By.XPATH,'//input[@id="searchboxinput"]'))
        )
        for _ in range(0,4):
            search_box.click()
            search_box.send_keys(Keys.RETURN)
   
        time.sleep(15)

        try:
            self.driver.find_element(By.XPATH,'//*[contains(text(), "Google Maps can\'t find")]')
            pass
        except:
            try:
                try:
                    sidebar_result = WebDriverWait(self.driver,1000).until(
                        EC.presence_of_element_located((By.XPATH,f"//div[@role='main']//div[@aria-label][1]"))
                    )
                except:
                    pass
                # Create an ActionChains object to perform the hover action and scroll
                try:
                    hover_element = self.driver.find_element(By.CSS_SELECTOR,"a.hfpxzc")
                    actions = ActionChains(self.driver)
                    actions.move_to_element(hover_element).perform()
                except:
                    pass
                Scrolling = True
                number_scroll = 0
                
                while Scrolling:
                    self.driver.execute_script("window.scrollTo(0, window.scrollY + 200);")

                    self.driver.execute_script("arguments[0].scrollIntoView();", sidebar_result)
                    for _ in range(0,5):
                        sidebar_result.send_keys(Keys.PAGE_DOWN)
                        time.sleep(0.5)
                        html = self.driver.find_element(By.TAG_NAME,"html").get_attribute("outerHTML")
                        if(html.find("You've reached the end of the list")!= -1):
                            Scrolling = False
                    number_scroll += 1
                    
                    if number_scroll >= 10:
                        self.driver.refresh()

                



        
                webDirection_removal = """
                    const direction_content =  document.querySelectorAll('div.Rwjeuc');
                    direction_content.forEach(element =>{
                        element.remove();
                    });
                """

                ads_removal = """
                const ads = document.querySelectorAll('a.bm892c');
                    ads.forEach(element => {
                        element.remove();
                    });
                """
                self.driver.execute_script(webDirection_removal)
                self.driver.execute_script(ads_removal)
                
                print("entering")
                for google_map in self.driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc'):
                    self.driver.execute_script(f"window.open('{google_map.get_attribute('href')}', '_blank');")
                    # Switch to the new tab (the last tab in the list)
                    window_handles = self.driver.window_handles
                    new_tab_handle = window_handles[-1]
                    self.driver.switch_to.window(new_tab_handle)
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'h1.lfPIob'))
                    )
                    try:
                        # Use a JavaScript snippet to extract data from the page
                        getInfo = """
                            const companyName = document.querySelector('h1.lfPIob') ? document.querySelector('h1.lfPIob').textContent : '';
                            const addressButton = document.querySelector('button[data-item-id="address"]');
                            const address = addressButton ? addressButton.getAttribute('aria-label') : '';
                            const websiteLink = document.querySelector('a[data-item-id="authority"]');
                            const websiteUrl = websiteLink ? websiteLink.getAttribute('href') : '';
                            const phoneButton = document.querySelector('button[data-item-id^="phone:"]');
                            const phoneNumber = phoneButton ? phoneButton.getAttribute('aria-label') : '';
                            return [companyName, address,phoneNumber, websiteUrl];
                        """
                        
                        data = self.driver.execute_script(getInfo)
                        information.append(data)
                    except Exception as e:
                        # Handle exceptions if the extraction fails for any reason
                        print(f"Error: {e}")
                    
                    self.driver.close()
                    mainWindow = self.driver.window_handles[0]
                    self.driver.switch_to.window(mainWindow)


             

                # keyword_checks = " || ".join([f'parentElement.textContent.includes("{keyword.strip()}")' for keyword in self.keywords()])

                # full_keyword_result_data = keyword_result_data % keyword_checks




                
            except Exception as e:
                pass
        return information



