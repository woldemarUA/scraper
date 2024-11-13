import asyncio
from urllib.parse import urljoin

from scrapers.product_page_scraper import scrape_product_page_async

async def parse_product_cards (soup, url):
    cards = soup.find_all('a', class_="product-tile")
    parsed_data = []

    # list of tasks for async parsing the pages
    tasks = []
    for card in cards:
        picture_tag = card.find('picture')
        img_tag = picture_tag.find('img') if picture_tag else None
        product_url = urljoin(url,card.get('href', ''))
        image_url = ''
        if img_tag:
            # Extract the image URL (prefer data-src if available)
            image_url = img_tag.get('data-src') or img_tag.get('src')
            
        data = {
            "title": card.find('h3', class_='product-tile__label').get_text(strip=True),
            "product_url":  product_url,
            "category_img": urljoin(url,image_url)
        }
        # Add async scraping task for the product page to the list
        tasks.append(scrape_product_page_async(product_url))
        parsed_data.append(data)
     # Await all the scraping tasks concurrently
    scraped_pages = await asyncio.gather(*tasks)
    print(scraped_pages)

    return parsed_data