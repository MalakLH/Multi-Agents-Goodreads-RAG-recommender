from playwright.async_api import async_playwright

# We use this script to save the Goodreads login session to a state.json file for future scraping sessions.

async def save_session():

    async with async_playwright() as p:
        
        # Launch browser headfully so you can interact with it
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to Goodreads login
        await page.goto("https://www.goodreads.com/user/sign_in")

        print("Please log in manually in the browser window...")
        print("Press ENTER in this terminal once you are fully logged in.")

        # Wait until you press ENTER in the terminal
        input()

        # Save session cookies & local storage to state.json
        await context.storage_state(path="state.json")
        print("Successfully saved login session to state.json!")

        await browser.close()

