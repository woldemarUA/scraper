from playwright.sync_api import Page

async def collect_data_after_click(page: Page) -> dict:
    await page.wait_for_selector(".product-configurator")  # Example selector, adjust as needed

    title = await page.locator(".pagetitle").inner_text()
    await page.screenshot(path="./playwright/screenshots/oclock/after_title.png",full_page=True)
    await page.locator(".product-steps").all()
    print("product steps awaited")
    product_steps = await page.locator(".product-steps__item-title").all()
    #  here is the issue  - it the one element
    data = {
            "title": title,    
        }
    for i in range(len(product_steps)):
        step = product_steps[i]
        step_text = await step.inner_text()  # Get inner text of each step
        desc_elements = await page.locator(".tile-inner").all()
        print(len(desc_elements))
        # Ensure that step data is initialized as a dictionary
        if f'step{i}' not in data:
            data[f'step{i}'] = {"name": "", "data": []}  # Initialize the dictionary with default values
         # Assign the step text to the name
        data[f'step{i}']["name"] = step_text
        array = []
        for el in desc_elements:
            text = await el.inner_text()
            array.append(text)
        data[f'step{i}']["data"] = array

        # Check if it's the last step
        if i == len(product_steps) - 1:
            print(f"This is the final step: {step_text}")
            # table-prices
            return   # Skip clicking the last step and continue to the next iteration (if any)
        # For all other steps, click the first element in .tile-inner
        if desc_elements:  # Ensure that desc_elements is not empty before clicking
            await desc_elements[0].click()
       
    # for i in range(len(product_steps)):
    #     desc_elements = await page.locator(".text-secondary .short-description").all_inner_texts()
    #     print(desc_elements)
    return data