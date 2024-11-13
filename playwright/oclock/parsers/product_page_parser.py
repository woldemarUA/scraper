from bs4 import BeautifulSoup
import json


from parsers.product_configurator_side__parser import parse_side_configurator


async def parse_product_page(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    side_configurator = soup.find('div', class_='product-configurator-side')
    breadcumbs_list = soup.find_all('li', class_='breadcrumb-item')
    # title_element = breadcumbs_list[len(breadcumbs_list)-1].find('span', class_='breadcrumb-link').get_text(strip=True)
    title =breadcumbs_list[len(breadcumbs_list)-1].find('span', class_='breadcrumb-link').get_text(strip=True).replace(' ', '_')

    script_tag = soup.find('script', text=lambda text: text and 'let productData =' in text)
    # Extract the content of the script and clean it
    if script_tag:
        script_content = script_tag.string.strip()
        # Extract JSON part after 'let productData ='
        product_data_str = script_content.split('let productData =', 1)[1].strip().rstrip(';')
        
        # Convert the JSON string into a Python dictionary
        product_data = json.loads(product_data_str)
        
        # Save the dictionary to a JSON file
        with open(f'json_configs/{title}_product_data.json', 'w') as json_file:
            json.dump(product_data, json_file, indent=4)
    else:
        print("Product data not found.")
   
    if side_configurator:
        side_data = parse_side_configurator(side_configurator)
    else:
        side_data = None  # Handle it gracefully, maybe return default data or l
    # print(side_data)
    return {
        'title': soup.find('h1', class_='pagetitle').get_text(strip=True),
        'side_data': side_data
    }