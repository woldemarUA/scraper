import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

import json

async def scrape_with_playwright_async():
    async with async_playwright() as p:
        # Launch the browser in headful mode to mimic a real user
        browser = await p.chromium.launch(headless=False)
        
        # Configure the browser context with a realistic user agent and viewport
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        # Open a new page in the context
        page = await context.new_page()
        
        # Apply stealth techniques to the page
        await stealth_async(page)
        
        try:
            url = "https://www.printoclock.com/carte-de-correspondance?q=100x210/350DM/R/NOSUV/NOF/NOENV/CLA&q=100x210%2F350DM%2FR%2FNOSUV%2FNOF%2FNOENV%2FCLA&inputs="
            # url= "https://www.printoclock.com/tree-url/carte-de-correspondance?selectionSteps%5B0%5D=100x210&selectionSteps%5B1%5D=350DM&selectionSteps%5B2%5D=R&selectionSteps%5B3%5D=NOSUV&selectionSteps%5B4%5D=NOF&selectionSteps%5B5%5D=NOENV&selectionSteps%5B6%5D=CLA"
           
        #    url = "https://www.printoclock.com/tree-url/carte-de-correspondance?selectionSteps%5B0%5D=100x210"
            
            await page.wait_for_selector('.table-prices')  # Wait until the table is visible
            # Navigate to the URL with extra timeout for Cloudflare
            await page.goto(url, wait_until="load", timeout=60000)
            
            # Wait for a few seconds to let any Cloudflare challenges complete
            await page.wait_for_timeout(5000)


            
            # Extract and print the page content
            content = await page.content()
            print(content)  # Use the content as needed (parse, save, etc.)
            with open(f'product_data_content.html', 'w', encoding='utf-8') as html_file:
                html_file.write(content)
        except Exception as e:
            print(f"Failed to load page: {e}")
        finally:
            await browser.close()

# Run the async function
asyncio.run(scrape_with_playwright_async())
