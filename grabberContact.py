import asyncio
import aiohttp
from aiohttp import ClientTimeout

from bs4 import BeautifulSoup
import csv
import re
from locator import Locator
import urllib.request
from keyword_generator import keyword_loc



def writeCsv(result: list):
    print(result)
    with open("output.csv", encoding='utf-8', mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(result)



async def fetch_url(session, url):  
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers,timeout=120) as response:  # Set a timeout value
                if response.status == 200:
                    print(f"Request to {url} returned status code 200 (OK)")
                    return await response.text()
                    
                else:
                    print(f"Request to {url} returned status code {response.status}")
                    return None
                    
    except asyncio.TimeoutError:
        print(f"Request to {url} timed out")
        return None
    except aiohttp.ClientError as e:
        print(f"Request to {url} encountered an error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during the request to {url}: {e}")
        return None

async def extract_emails(website,url,company_name,phone_number,address):
    soup = BeautifulSoup(website, 'html.parser')
    found_mailto_link = False  # Flag to track if a mailto link is found

    for a_tag in soup.find_all("a", href=True):
        if a_tag["href"].startswith("mailto:"):
            email = a_tag["href"][7:]
            found_mailto_link = True
    if found_mailto_link:
        writeCsv([company_name,url,address, email, phone_number])
    else:
        writeCsv([company_name,url,address, "", phone_number])



async def process_feed_data(data):

    url = data[-1]  # Assuming the URL is the last element
    async with aiohttp.ClientSession() as session:
        response_content = await fetch_url(session, url)
        if response_content:
            await extract_emails(response_content,url,data[0],data[1],data[2])

async def main():
    # Open the .txt file in read mode
    file_path = 'citiesfeed.txt'  # Replace with the actual file path
    with open(file_path, 'r') as file:
        cities = file.readlines()


# The file will be automatically closed when you exit the 'with' block
    for city in cities:
        result_name = f"{city.strip()} Solar store"
        print(result_name)
        locator_data = Locator(f"{result_name} Solar company").locator_start()   
        if locator_data is not None:   
        # List to hold the extracted emails
            processing_tasks = [process_feed_data(data) for data in locator_data]
            await asyncio.gather(*processing_tasks)
                # Open the CSV file in append mode




    

if __name__ == "__main__":
    asyncio.run(main())


