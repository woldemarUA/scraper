from playwright.async_api import async_playwright
from retry_async import retry

import asyncio
import json


from oclock.oclock_bs import parse_card

@retry(tries=3, delay=2, is_async=True)
async def scrape_dynamic_content (url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context  = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url) #, timeout=5000
            print('Navigated, start wating')
            await page.screenshot(path="./playwright/screenshots/oclock/start.png",full_page=True)
            # Handle overlays (e.g., cookie consent)
            await page.wait_for_selector('#axeptio_btn_acceptAll')
            
            await page.click('#axeptio_btn_acceptAll')
            print("button cookies clicked")
            await page.screenshot(path="./playwright/screenshots/oclock/clicked_consent.png",full_page=True)
            
            data = []
            product_list_element = await page.query_selector_all(".card-new--product")
            cards = await page.inner_html(".productList__list")
            parsed_cards = parse_card(cards, url)
            print(parsed_cards)
            # for element in product_list_element:
            # for i  in range(len(product_list_element)):

            #     cards = await page.inner_html(".productList__list")
            #     parse_card(cards)
            #     element_data = {}
            #     cards = await page.query_selector_all(".card-new--product")
            #     element = cards[i]
                
            #     title_element = await element.query_selector(".card-new__title")
            #     element_data["title"] = await title_element.inner_text()

            #     featured_price_element = await element.query_selector(".card-new__subtitle")
            #     featured_price = await featured_price_element.inner_text()
            #     featured_price_text = featured_price.split("HT")
            #     element_data["featured_price"] = featured_price_text[0]
            #     element_data["unit"] = featured_price_text[1]
            #     if await page.is_visible(".card-new__tag--purple"):
            #         promo_element = await element.query_selector(".card-new__tag--purple")
            #         element_data["promo"] = await promo_element.inner_text()
            #     properties_elements = await element.query_selector_all(".card-new__properties__property")
            #     element_data["properties"] =[]
            #     for property_element in properties_elements:
            #         element_data["properties"].append(await property_element.inner_text())
                
            #     await element.click()
            #     await page.wait_for_load_state("networkidle")

            #     detail_info = await collect_data_after_click(page)
            #     element_data["detail_info"] = detail_info

            #     data.append(element_data)

            #     # Navigate back to the main page
            #     await page.go_back()
            #     await page.wait_for_load_state("networkidle")  # Ensure the main page is fully reloaded
                

            
        
        # Get the count of child elements
            # with open('oclock.json', 'w') as json_file:
            #     json.dump(data, json_file, indent=4)
      
 
      
            await page.screenshot(path="./playwright/screenshots/oclock/loadedConfElement.png",full_page=True)
            # Add your scraping logic here

        except Exception as e:
            print(f"An error occurred: {e}")
            raise  # Re-raise the exception for retrying

        finally:
            await page.close()
            await context.close()
            await browser.close()



asyncio.run(scrape_dynamic_content("https://www.printoclock.com/imprimerie"))
# asyncio.run(scrape_dynamic_content("https://www.printoclock.com/"))






# https://www.printoclock.com/