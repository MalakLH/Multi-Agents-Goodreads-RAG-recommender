import asyncio
from playwright.async_api import async_playwright

# WEB SCRAPER FOR GOODREADS RECOMMENDATION CAROUSEL, For "Readers also enjoyed" section on a book page

async def scrape_goodreads_carousel(url: str):

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"Navigating to {url}")
        await page.goto(url, wait_until="domcontentloaded")

        # 1. Scope to the primary recommendations carousel container
        # "Readers also enjoyed" carousel container:
        carousel_container = page.locator('div.BookPage__relatedTopContent, ul.CarouselGroup').first
        
        # 2. Scroll the container itself into view to trigger initial lazy render
        await carousel_container.scroll_into_view_if_needed()
        await page.wait_for_timeout(150000)

        # 3. Target ONLY book cards inside this specific container
        cards = carousel_container.locator('[data-testid="book-card"]')
        count = await cards.count()
        print(f"Found {count} cards in target carousel. Extracting data...")

        books_data = []

        for i in range(count):
            card = cards.nth(i)

            # Use inner_text() directly without scrolling each hidden card
            title_loc = card.locator('[data-testid="title"]').first
            author_loc = card.locator('[data-testid="author"]').first
            rating_loc = card.locator('[data-testid="ratingValue"]').first
            link_loc = card.locator('a[href*="/book/show/"]').first

            # Extract available details
            name = await title_loc.inner_text() if await title_loc.count() > 0 else None
            author = await author_loc.inner_text() if await author_loc.count() > 0 else None
            rating = await rating_loc.inner_text() if await rating_loc.count() > 0 else None
            href = await link_loc.get_attribute("href") if await link_loc.count() > 0 else None

            # Format URL
            book_url = f"https://www.goodreads.com{href}" if href and href.startswith("/") else href

            parsed_rating = None
            if rating:
                try:
                    parsed_rating = float(rating.strip())
                except ValueError:
                    parsed_rating = rating.strip()

            books_data.append({
                "name": name.strip() if name else None,
                "author": author.strip() if author else None,
                "rating": parsed_rating,
                "book_url": book_url
            })

        await browser.close()
        return books_data


if __name__ == "__main__":
    target_url = input("Enter the Goodreads carousel URL to scrape: ").strip()
    books = asyncio.run(scrape_goodreads_carousel(target_url))
    
    print("\n--- Scraped Results ---")
    for b in books:
        print(b)