import asyncio
from grabberContact import Worker
import concurrent.futures

class App:
    def __init__(self):
        self.tasks = []

    async def run_worker(self, worker):
        await worker.run()

    async def run(self):
        # Replace these with the actual file paths
        region_file = 'region.txt'
        maker_file = 'maker.txt'
        style_file = 'style.txt'
        villages_file = 'villages.txt'

        # Read keywords from each file
        with open(region_file, 'r') as file:
            region_keywords = file.readlines()
        print(region_keywords)

        with open(maker_file, 'r') as file:
            maker_keywords = file.readlines()

        with open(style_file, 'r') as file:
            style_keywords = file.readlines()

        with open(villages_file, 'r') as file:
            villages_keywords = file.readlines()

        # Generate result keywords
        result_keywords = []

        # Region + Maker
        for region_kw in region_keywords:
            for maker_kw in maker_keywords:
                result_keywords.append(f"{region_kw.strip()} + {maker_kw.strip()}")

        # Village + Maker
        for village_kw in villages_keywords:
            for maker_kw in maker_keywords:
                result_keywords.append(f"{village_kw.strip()} + {maker_kw.strip()}")

        # Region + Style + Maker
        for region_kw in region_keywords:
            for style_kw in style_keywords:
                for maker_kw in maker_keywords:
                    result_keywords.append(f"{region_kw.strip()} + {style_kw.strip()} + {maker_kw.strip()}")

        # Village + Style + Maker
        for village_kw in villages_keywords:
            for style_kw in style_keywords:
                for maker_kw in maker_keywords:
                    result_keywords.append(f"{village_kw.strip()} + {style_kw.strip()} + {maker_kw.strip()}")

        # Village + Style
        for village_kw in villages_keywords:
            for style_kw in style_keywords:
                result_keywords.append(f"{village_kw.strip()} + {style_kw.strip()}")
        print(result_keywords)
        for region in region_keywords:
            for keyword in result_keywords:
                result_name = f"Italy, {keyword}"
                print(result_name)
                worker = Worker(result_name, keyword, region)
                self.tasks.append(self.run_worker(worker))  # Await the coroutine here

if __name__ == "__main__":
    app = App()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run())

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(asyncio.run, task) for task in app.tasks]  # Use asyncio.run inside ThreadPoolExecutor
