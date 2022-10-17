import re
from decimal import Decimal

import requests
from bs4 import BeautifulSoup

from main.settings import URL_SCRAPING_DOMAIN, URL_SCRAPING


"""
{
    'name': 'Труба профильная 40х20 2 мм 3м', 
    'image_url': 'https://my-website.com/30C39890-D527-427E-B573-504969456BF5.jpg', 
    'price': Decimal('493.00'), 
    'unit': 'за шт', 
    'code': '38140012'
 }
 """


def scraping():
    resp = requests.get(URL_SCRAPING, timeout=10.0)
    if resp.status_code != 200:
        raise Exception('HTTP ошибка входа!')

    data_list = []
    html = resp.text

    # print(f'HTML-текст имеет {len(html)} cимволов')
    # print(50 * '$')
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.select('.hot__item ')
    for block in blocks:
        data = {}
        name = block.select_one('.hot__item-ttl').get_text().strip()
        data['name'] = name

        image_url = URL_SCRAPING_DOMAIN + block.select_one('img')['src']
        data['image_url'] = image_url

        price_raw = block.select_one('span', itemprop="price").text.strip()
        price = Decimal(price_raw)
        data['price'] = price

        print(data)

        # print(f'HTML-текс имеет {len(block.text)} символов')
        # print(80 * '=')
        # print(block.text)
        # break


if __name__ == '__main__':
    scraping()
