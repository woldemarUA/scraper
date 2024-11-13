


def parse_side_configurator(side_configurator):
    pictures_list = side_configurator.find('div', class_='carousel-inner').find_all('a')
    side_benefits = side_configurator.find('ul', style="list-style-type:none")
    image_urls = []
    for picture in pictures_list:
        image_urls.append(picture.get('href'))
    return {
        'side_title': side_configurator.find('h3').get_text(strip=True),
        'side_benefits': [ li.get_text(strip=True) for li in side_benefits.find_all('li')], 
        'side_text': side_configurator.find_all('p')[1].get_text(strip = True),
        'image_urls': image_urls
    }

# product-configurator-side