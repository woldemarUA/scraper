from playwright.async_api import async_playwright
from retry_async import retry

from price_table_parser import parse_price_table

from bs4 import BeautifulSoup

import asyncio
import json

@retry(tries=3, delay=2, is_async=True)
@retry(tries=3, delay=2, is_async=True)
async def main (url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context  = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url) #, timeout=5000
            print('Navigated, start wating')
            await page.wait_for_selector('#didomi-notice-agree-button')
            await page.click('#didomi-notice-agree-button')
            # IconsAttributeField__StyledLabel-sc-xsncyg-7
            await page.wait_for_selector('.IconsAttributeField__StyledLabel-sc-xsncyg-7')
            await page.wait_for_selector('.PriceGridTable__StyledPriceTable-sc-x9occo-2')
            html = await page.inner_html('#attribute-list-wrapper')
            parse_price_table(html)
           
          
        except Exception as e:
            print(f"An error occurred: {e}")
            raise  # Re-raise the exception for retrying

        finally:
            await page.close()
            await context.close()
            await browser.close()



# asyncio.run(main('https://www.exaprint.fr/page-data/la-carterie/carte-de-visite/page-data.json'))
asyncio.run(main('https://www.exaprint.fr/la-carterie/carte-de-visite/papier-haut-de-gamme'))
# asyncio.run(main('https://www.exaprint.fr/la-carterie/carte-de-visite/papier-classique'))
# asyncio.run(main('https://www.exaprint.fr/la-carterie/carte-de-visite'))
