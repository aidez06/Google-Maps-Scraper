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



class Locator:

    def __init__(self, keyword) -> None:
        self.keyword = keyword
        self.url = f"https://www.google.com/maps/search/{self.keyword}"
        
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()


    def locator_start(self):
        self.driver.get(self.url)
        print(self.keyword)
        WebDriverWait(self.driver,1000).until(
            EC.presence_of_element_located((By.XPATH,'//input[@id="searchboxinput"]'))
        )
        print("start")
        try:
       
            sidebar_result = WebDriverWait(self.driver,20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,f"div[aria-label='Results for {self.keyword}']"))
            )

        
            Scrolling = True
            while(Scrolling):
                print("scrolling")
                number_scroll = 0
                for _ in range(0,5):
                    print(_)
                    sidebar_result.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.5)
                    html = self.driver.find_element(By.TAG_NAME,"html").get_attribute("outerHTML")
                    if(html.find("You've reached the end of the list")!= -1):
                        Scrolling = False
                number_scroll += 1
                print(number_scroll)
                if number_scroll >= 15:
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
            keyword_result_data = """
            async function processWineryLinks() {
                const wineryLinks = document.querySelectorAll('a.hfpxzc');
                const delay = 1000; // 1 second
                var result = [];

                for (let index = 0; index < wineryLinks.length; index++) {
                    const link = wineryLinks[index];

                    // Simulate a click on the link
                    link.click();

                    // Wait for the delay using a Promise
                    await new Promise(resolve => setTimeout(resolve, delay));

                    // Check if the parent element contains the desired text
                    const parentElement = link.parentElement;
                    if (parentElement && parentElement.textContent.includes("Solar energy company")) {
                        var innerResult = [];

                        // Extract data using query selectors
                        innerResult.push(link.getAttribute('aria-label'));

                        const anchorElement = document.querySelector('a[data-tooltip="Open website"]');
                        const buttonElement = document.querySelector('button[data-tooltip="Copy phone number"]');
                        const address = document.querySelector('button[data-tooltip="Copy address"]');

                        innerResult.push(buttonElement ? buttonElement.getAttribute('data-item-id') : "");
                        innerResult.push(address ? address.getAttribute('aria-label') : "");
                        innerResult.push(anchorElement ? anchorElement.getAttribute('href') : "");

                        result.push(innerResult);
                    }
                }

                // Logging the result array
                console.log(result);

                // Add the result array to the HTML document for debugging
                var resultElement = document.createElement('pre');
                resultElement.textContent = JSON.stringify(result, null, 2);
                document.body.appendChild(resultElement);
            }

            processWineryLinks();

            
            """

            self.driver.execute_script(webDirection_removal)
            self.driver.execute_script(ads_removal)
            self.driver.execute_script(keyword_result_data)


            #Waiting until pre tag element already exist

            results = WebDriverWait(self.driver,1000).until(
                EC.presence_of_element_located((By.TAG_NAME,'pre'))
            )
            time.sleep(5)

            data_list = json.loads(results.text)

            return data_list
        except Exception as e:
            print(e)
            print("single items only")
            try:
                company_name = self.driver.find_element(By.XPATH, "//h1[@class='DUwDvf lfPIob']").text
                website_result = None  # Initialize website_result
                address = None  # Initialize address
                phone_number = None  # Initialize phone_number
                
                try:
                    website = self.driver.find_element(By.XPATH, '//a[@data-tooltip="Open website"]')
                    website_result = website.get_attribute('href')
                except:
                    pass

                try:
                    address_element = self.driver.find_element(By.XPATH,'//button[@data-tooltip="Copy address"]')
                    address = address_element.get_attribute("aria-label")
                except:
                    pass

                try:
                    phone_element = self.driver.find_element(By.XPATH, '//button[@data-tooltip="Copy phone number"]')
                    phone_number = phone_element.get_attribute("aria-label")
                except:
                    pass
            except:
                company_name = None
                

            return [[company_name, phone_number, website_result, address]]


