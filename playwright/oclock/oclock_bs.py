
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_card(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('a', class_='card-new card-new--product')
    parsed_data = []
    for card in cards:
        
        data = {
            'title': card.find('h3', class_='card-new__title').get_text(strip=True),
            'price': card.find('span', class_='card-new__subtitle').get_text(strip=True),
            # 'tag': card.find('span', class_='card-new__tag').get_text(strip=True),
            'product_url': urljoin(url,card.get('href', '')),
            'properties': [prop.get_text(strip=True) for prop in card.find_all('div', class_='card-new__properties__property')],
            'image_url': card.find('span', class_='card-new__image').get('data-img-src')
        }
        parsed_data.append(data)
    return parsed_data
   
