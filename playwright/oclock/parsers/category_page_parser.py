from bs4 import BeautifulSoup


from parsers.product_cards_parser import parse_product_cards

async def parse_category_page (html, url):
   products = extract_product_container(html)
   description = extract_category_description_container(html)

   await parse_product_cards(products,url)
  
   return products
    # .row all products
    # .cms-content .taxon-description
  


def extract_product_container (html):
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup.find('div', class_="row")

def extract_category_description_container(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('div', class_='taxon-description')

