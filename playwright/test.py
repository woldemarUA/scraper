from playwright.async_api import async_playwright
from retry_async import retry

import asyncio
import json


@retry(tries=3, delay=2, is_async=True)
async def scrape_dynamic_content (url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context  = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url) #, timeout=5000
            print('Navigated, start wating')
            await page.screenshot(path="./playwright/screenshots/start.png",full_page=True)
            await page.wait_for_selector('#footer_tc_privacy_button')
    
            await page.click('#footer_tc_privacy_button')
            print("button cookies clicked")
            await page.screenshot(path="./playwright/screenshots/clicked_consent.png",full_page=True)
            # await page.wait_for_selector('.price-grid-container', state='visible', timeout=10000)
            
            # # await page.wait_for_selector('.configuration-container', state='visible', timeout=10000)
            # print("loaded price")
            configuration_elements = await page.query_selector_all('.configuration-container')
            print(f'Configuration elements length is {len(configuration_elements)}')

           
            format_menu =  page.locator('xpath=//*[@id="product-standard-container"]/div/div[1]/div[3]/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[3]')

            data = []
            
            menu_elements = await format_menu.locator('.gallery-item').all() 
            
         
            for j, element in enumerate(menu_elements):
          
                obj = {}

                    # Wait for a specific price element to appear or change
                    # Adjust this selector based on what you expect to change
                link = element.locator('.inner')
                await link.click()
                print(j)
                # await page.wait_for_selector(".validation-overlay", state="visible")
                # await page.wait_for_selector(".validation-overlay", state="hidden")
                print( f'visible {await page.is_visible(".validation-overlay")}')
                await page.wait_for_selector('.price-grid-container .cells-row', state='visible', timeout=10000)

                print("Loaded prices.")
                   
                format = await element.inner_text()
                obj['format'] = format

                paper = await configuration_elements[0].query_selector_all('.form-group')
                for element_inner in paper:
                    header_element = await element_inner.query_selector('.feature-label-title')
                    header = await header_element.inner_text()
                    input_elements = await element_inner.query_selector_all('.custom-control-input') 
                    
                    
                    for input_element in input_elements:
                        is_checked = await input_element.is_checked()
                        
                        if is_checked:
                            obj[header] = await input_element.input_value()
                        # inner_text = await element.inner_text()
                        # print(inner_text)
                    
                color = page.locator('xpath=//*[@id="product-standard-container"]/div/div[1]/div[3]/div[1]/div/div[1]/div[5]/div/div[2]/div[1]/div/div[3]')
                obj['color'] = await color.locator('.active').inner_text()
                price_grid = await page.query_selector('.price-grid-container')
                price_quantities = await price_grid.query_selector_all('.qty-btn')
                prices = await price_grid.query_selector_all('.cells-row')
                obj['prices'] = {}
                for i, quantity in enumerate(price_quantities):
                    obj['prices'][await quantity.inner_text()] = await prices[i].inner_text()
                data.append(obj)
               
         
            
        
        # Get the count of child elements
            with open('output.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
      
    # Perform an action on the element, e.g., click or get text content
            

            # for element in configuration_elements:
            #     # await element.scroll_into_view_if_needed()
            #     inner_text  = await element.inner_text()
            #     print(inner_text)
           
            # if configuration_element:
            #     data_test_element = await configuration_element.query_selector('[data-test]')
            #     if data_test_element:
            #         await data_test_element.click()
            #         print(f'Clicked on element with data-test attribute: {await data_test_element.get_attribute("data-test")}')
            #     else:
            #         print('No child element with data-test attribute found.')
          
      
            await page.screenshot(path="./playwright/screenshots/loadedConfElement.png",full_page=True)
            # Add your scraping logic here

        except Exception as e:
            print(f"An error occurred: {e}")
            raise  # Re-raise the exception for retrying

        finally:
            await page.close()
            await context.close()
            await browser.close()


# asyncio.run(scrape_dynamic_content("https://www.pixartprinting.fr/calendriers/sous-mains/"))
# asyncio.run(scrape_dynamic_content("https://www.pixartprinting.fr/impression-revues-catalogues-livres/livres-de-recettes/"))
asyncio.run(scrape_dynamic_content("https://www.pixartprinting.fr/petit-format/enveloppes/enveloppes-commerciales/"))