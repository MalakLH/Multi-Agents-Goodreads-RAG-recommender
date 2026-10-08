import asyncio
from playwright.async_api import async_playwright

# WEB SCRAPER FOR INDIVIDUAL GOODREADS BOOK PAGE
# WE USE IT TO SCRAPE THE BOOK'S TITLE, AUTHOR, DESCRIPTION, GENRES, AND REVIEWS

async def book_scraper(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(
            url=url,
            wait_until="domcontentloaded",
        )

        # Wait for the main title element to load
        title_locator = page.locator(
            'h1[data-testid="bookTitle"], div.BookPageTitleSection__title h1'
        ).first
        await title_locator.wait_for(timeout=15000)

        # 1. Extract Title
        title = (
            await title_locator.inner_text()
            if await title_locator.count() > 0
            else ""
        )

        # 2. Extract Author
        author_locator = page.locator(
            'span[data-testid="name"], span.ContributorLink__name'
        ).first
        author = (
            await author_locator.inner_text()
            if await author_locator.count() > 0
            else ""
        )

        # 3. Extract Description
        description_locator = page.locator(
            'div[data-testid="description"] .Formatted, div.BookPageMetadataSection__description .Formatted'
        ).first
        description = (
            await description_locator.inner_text()
            if await description_locator.count() > 0
            else ""
        )

        # 4. Extract Genres List
        genre_elements = page.locator(
            'span.BookPageMetadataSection__genreButton a span.Button__labelItem, ul.CollapsableList[aria-label*="genres"] span.BookPageMetadataSection__genreButton span.Button__labelItem'
        )
        genre_count = await genre_elements.count()

        genres = []
        for i in range(genre_count):
            genre_name = await genre_elements.nth(i).inner_text()
            if genre_name.strip():
                genres.append(genre_name.strip())

        # 5. Extract Reviews
        # Expand "Show more" buttons on reviews if present
        show_more_buttons = page.locator('article.ReviewCard button span:has-text("Show more")')
        show_more_count = await show_more_buttons.count()
        for i in range(show_more_count):
            try:
                await show_more_buttons.nth(i).click(timeout=2000)
            except Exception:
                pass  # Skip if click fails or button disappears

        review_cards = page.locator('article.ReviewCard')
        reviews_count = await review_cards.count()

        reviews = []
        for i in range(reviews_count):
            card = review_cards.nth(i)

            # Review Text
            text_loc = card.locator('section.ReviewText .Formatted').first
            review_text = (await text_loc.inner_text()).strip() if await text_loc.count() > 0 else ""

            reviews.append(
                review_text
            )

        await browser.close()

        return {
            "title": title.strip(),
            "author": author.replace("\xa0", " ").strip(),
            "description": description.strip(),
            "genres": genres,
            "reviews": reviews,
            "book_url": url,
        }

