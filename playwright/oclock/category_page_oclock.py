from playwright.async_api import async_playwright
from retry_async import retry

import asyncio
import json

from parsers.category_page_parser import parse_category_page



@retry(tries=3, delay=2, is_async=True)
async def scrape_category_page(url):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context  = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url)
            print('Navigated, start wating')
            # coockies accept
            await page.wait_for_selector('#axeptio_btn_acceptAll')
            await page.click('#axeptio_btn_acceptAll')
            print("button cookies clicked")

            # select the main container
            await page.wait_for_selector('#page-taxon')
            products_container = await page.inner_html('#page-taxon')
            await parse_category_page(products_container, url)
            # bannerTrustpilot__container here they have description where they print 
        except Exception as e:
            print(f"An error occurred: {e}")
            raise  # Re-raise the exception for retrying

        finally:
            await page.close()
            await context.close()
            await browser.close()
 



if __name__ == "__main__":
    asyncio.run(scrape_category_page("https://www.printoclock.com/imprimerie/carterie"))

