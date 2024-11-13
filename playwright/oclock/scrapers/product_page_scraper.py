from playwright.async_api import async_playwright
from retry_async import retry

import asyncio
import json

# from parsers.product_page_parser import parse_product_page

@retry(tries=3, delay=2, is_async=True)

async def scrape_product_page_async(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context  = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(url)
            print(f'Navigated to: {url}')
            await page.wait_for_selector('#axeptio_btn_acceptAll')
            await page.click('#axeptio_btn_acceptAll')
            print("button cookies clicked")
            # # desc_elements = 
            # # Wait until all expected `.tile-inner` elements are present (for example, 6 elements)
            # await page.wait_for_selector(".tile-inner")  # Wait for at least one
       
            # content = await page.inner_html('.bg-light')
            # content = await page.inner_html('.product-configurator')
            content = await page.wait_for_selector('.table-prices')  
            # return await parse_product_page(content)
            print(await content.inner_text())

        except Exception as e:
            print(f"An error occurred: {e}")
            raise  # Re-raise the exception for retrying

        finally:
            await page.close()
            await context.close()
            await browser.close()



if __name__ == "__main__":
    asyncio.run(scrape_product_page_async("https://www.printoclock.com/carte-de-correspondance?q=100x210/350DM/R/NOSUV/NOF/NOENV/CLA&q=100x210%2F350DM%2FR%2FNOSUV%2FNOF%2FNOENV%2FCLA&inputs="))
    # asyncio.run(scrape_product_page_async("https://www.printoclock.com/cartes-de-visite-c-14.html"))
    # asyncio.run(scrape_product_page_async("https://www.printoclock.com/cartes-de-voeux"))
    # asyncio.run(scrape_product_page_async("https://www.printoclock.com/carte-de-correspondance"))   
# "https://www.printoclock.com/carte-de-correspondance?q=100x210/350DM/R/NOSUV/NOF/NOENV/CLA&q=100x210%2F350DM%2FR%2FNOSUV%2FNOF%2FNOENV%2FCLA&inputs="
# https://www.printoclock.com/carte-de-correspondance