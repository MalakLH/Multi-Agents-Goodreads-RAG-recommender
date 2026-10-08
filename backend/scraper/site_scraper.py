import asyncio
from playwright.async_api import async_playwright
from backend.scraper.page_scraper import page_scraper

#web scraper for the entire Goodreads "read" shelf, which may span multiple pages. 
# It uses the page_scraper function to scrape each page and aggregates the results.

async def site_scraper(next_page_url):
    data = []
    last_page = False

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set headless=False if you want to watch the browser

        # Load saved session state
        context = await browser.new_context(storage_state="state.json")
        page = await context.new_page()

        # Keep the loop INSIDE the browser context
        while not last_page:
            # Use 'await' here instead of asyncio.run()
            await page_scraper(next_page_url, page, data)

            next_button = page.locator("a.next_page[href]").first

            if await next_button.count() > 0:
                next_href = await next_button.get_attribute("href")
                next_page_url = f"https://www.goodreads.com{next_href}"
            else:
                last_page = True

        await browser.close()

    print(f"Scraper finished! Total books scraped: {len(data)}")
    return data