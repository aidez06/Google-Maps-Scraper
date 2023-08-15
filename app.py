import asyncio
from grabberContact import Worker
import concurrent.futures

class App:
    def __init__(self):
        self.tasks = []

    async def run_worker(self, worker):
        await worker.run()

    async def run(self):
        # Open the .txt file in read mode
        file_path = 'places.txt'  # Replace with the actual file path
        with open(file_path, 'r') as file:
            cities = file.readlines()
        cities.reverse()
        # Read keywords from file
        keywords_path = 'keywords.txt'
        with open(keywords_path, 'r') as file_keyword:
            keywords_feed = file_keyword.readlines()

        keywords_feed.reverse()

        # The file will be automatically closed when you exit the 'with' block
        for city in cities:
            city = city.strip()  # Remove newline characters

            for keyword in keywords_feed:
                if keyword.strip() == "Negociant":
                    result_name = f"{keyword} {city}"
                    
                else:
                    result_name = f"{city} {keyword}"
                worker = Worker(result_name, f"{city}  {keyword}")
                self.tasks.append(self.run_worker(worker))  # Await the coroutine here

if __name__ == "__main__":
    app = App()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run())

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(asyncio.run, task) for task in app.tasks]  # Use asyncio.run inside ThreadPoolExecutor
