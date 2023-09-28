import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup
from locator import Locator
class Worker:
    def __init__(self,result_name,villages, region):
        self.villages = villages
        self.region = region
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.result_name = result_name

    async def fetch_url(self, session, url):
        try:
            async with session.get(url, headers=self.headers, timeout=120) as response:
                if response.status == 200:
                   
                    return await response.text()
                else:
                  
                    return None
        except asyncio.TimeoutError:
 
            return None
        except aiohttp.ClientError as e:
   
            return None
        except Exception as e:
    
            return None

    async def extract_emails(self, website, url, company_name, phone_number, address):


        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    website = await response.text()
                    soup = BeautifulSoup(website, 'html.parser')
                    found_mailto_link = False

                for a_tag in soup.find_all("a", href=True):
                    if a_tag["href"].startswith("mailto:"):
                        email = a_tag["href"][7:]
                        found_mailto_link = True
                if found_mailto_link:
                    self.write_csv([self.region,self.villages,company_name, url, address, email, phone_number])
                    print(self.region,self.villages,company_name, url, address, email, phone_number)
                else:
                    self.write_csv([self.region,self.villages,company_name, url, address, "", phone_number])
                    print(self.region,self.villages,company_name, url, address, "", phone_number)
        except Exception as e:
            print(e)
            pass
    def write_csv(self, result):
        with open("output.csv", encoding='utf-8', mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(result)
            

    async def process_feed_data(self, data):
        url = data[-1]
        print(url)
        async with aiohttp.ClientSession() as session:
            response_content = await self.fetch_url(session, url)
            if response_content:
                await self.extract_emails(response_content,url, data[0], data[1], data[2])
            else:
                print("nothing here")

    async def main(self):
        locator_data = Locator(f"{self.result_name}").locator_start()

        if locator_data is not None:
            processing_tasks = []
            for data in locator_data:
                processing_tasks.append(self.process_feed_data(data))
            await asyncio.gather(*processing_tasks)
        
    
    async def run(self):  # Make the 'run' method async
        await self.main()
