import asyncio
from goodreads_session import save_session
from site_scraper import site_scraper


# asyncio.run(save_session())
next_page_url= input("Enter the Goodreads URL to scrape: ")

data = asyncio.run(site_scraper(next_page_url))
print(data)