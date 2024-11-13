from playwright.async_api import async_playwright
import asyncio


async def scrape_dynamic_content():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the target URL
        await page.goto('https://www.pixartprinting.fr/petit-format/enveloppes/enveloppes-commerciales/')
        await page.query_selector('.gallery')
        gallery = await page.query_selector('.gallery')

        
        await browser.close()

# Run the scraping function
asyncio.run(scrape_dynamic_content())
