import asyncio
import urllib.parse
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Function to build the URL with selection steps
def build_url(base_url, selection_steps):
    query_params = "&".join([f"selectionSteps%5B{step}%5D={urllib.parse.quote(value)}" for step, value in selection_steps.items()])
    return f"{base_url}?{query_params}"

# Async function to fetch page content
async def fetch_page_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        
        content = await page.content()
        await browser.close()
        return content

# Function to parse and process content
def parse_step_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    step = json.loads(soup.find('pre').get_text(strip=True))
    return step

# Main async function
async def main():

    # configi file from the parse_product_page(
    with open("../json_configs/product_data.json", 'r') as f:
        product_data = json.load(f)
    # Gather options for each step
    steps = product_data["steps"]
    selection_steps = {
        # Add your selection steps here
    }
    
    # base_url = "https://www.printoclock.com/tree-url/carte-de-correspondance"
    base_url = "https://www.printoclock.com/tree-url/cartes-de-visite-c-14.html"
    full_url = build_url(base_url, selection_steps)
    content = await fetch_page_content(full_url)
    step = parse_step_content(content)
    
    # for j, (key, value) in enumerate(step.items()):
    #     print(f'j is {j}')
    #     print(f'key {key}')
    #     print(f'value {value}')
  
    for i in range(1, len(steps)+1):
        for key in step:
            selection_steps[i]=key
    print(selection_steps)
        
    # for key in steps:
    #     selection_steps[key] = []
    # print(selection_steps)
  

# Run the async main function
asyncio.run(main())


# from playwright.async_api import async_playwright
# import urllib.parse

# async def main():
#     base_url = "https://www.printoclock.com/tree-url/carte-de-correspondance"
#     selection_steps = {
#         0: "100x210",
#         1: "250CB",
#         2: "R",
#         3: "NOSUV",
#         4: "NOF"
#     }

#     # Encode the selection steps into query parameters
#     query_params = "&".join([f"selectionSteps%5B{step}%5D={urllib.parse.quote(value)}" for step, value in selection_steps.items()])
#     full_url = f"{base_url}?{query_params}"

#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         context = await browser.new_context()
#         page = await context.new_page()
        
#         # Use Playwright’s request API to fetch the data
#         response = await context.request.get(full_url)
        
#         if response.ok:
#             # Get the content as text
#             content = await response.text()
#             print(content)  # Or save/process it as required
#         else:
#             print("Failed to fetch the data.")

#         await browser.close()

# # Run the async function
# import asyncio
# asyncio.run(main())