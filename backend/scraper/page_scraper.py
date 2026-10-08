from playwright.async_api import async_playwright

#Script to scrape a single Goodreads page with a list of books, "read" shelf. 
#It extracts the title, author, average rating, user rating, and book URL for each book on the page.

async def page_scraper(url, page, data):
    print(f"Navigating to {url}")
    
    # Navigate to URL
    await page.goto(url, wait_until="domcontentloaded")

    # Check if redirected or blocked
    current_url = page.url
    if "sign_in" in current_url or "login" in current_url:
        print("Warning: Redirected to login page. Authentication required.")
        return data

    try:
        # Wait for either table row or empty table message
        await page.wait_for_selector("#booksBody tr.bookalike, #booksBody", timeout=30000)
    except Exception as e:
        # Save screenshot for debugging if it fails
        await page.screenshot(path="debug_timeout.png")
        print("Failed to find #booksBody. Saved debug screenshot to 'debug_timeout.png'.")
        raise e

    book_rows = page.locator("#booksBody tr.bookalike")
    count = await book_rows.count()

    print(f"Found {count} books on current page.")

    for i in range(count):
        row = book_rows.nth(i)

        # Target the main link element inside title cell
        link_el = row.locator("td.title div.value a, td.title a").first

        if await link_el.count() > 0:
            title = await link_el.inner_text()
            href = await link_el.get_attribute("href")
            book_url = f"https://www.goodreads.com{href}" if href and href.startswith("/") else href
        else:
            title = ""
            book_url = ""

        # Extract author
        author_el = row.locator("td.author div.value a, td.author a").first
        author = (
            await author_el.inner_text()
            if await author_el.count() > 0
            else ""
        )

        # Extract average rating
        rating_el = row.locator("td.avg_rating div.value, td.avg_rating").first
        if await rating_el.count() > 0:
            avg_rating = (await rating_el.inner_text()).strip()
        else:
            avg_rating = None

        # Extract User rating
        stars_el = row.locator("td.rating div.stars").first
        if await stars_el.count() > 0:
            user_rating = await stars_el.get_attribute("data-rating")
        else:
            user_rating = "0"

        user_rating = (
            str(int(float(user_rating))) if user_rating and user_rating != "0" else "0"
        )

        data.append(
            {
                "title": title.strip(),
                "author": author.strip(),
                "avg_rating": avg_rating.strip(),
                "user_rating": user_rating.strip(),
                "book_url": book_url,
            }
        )

    return data