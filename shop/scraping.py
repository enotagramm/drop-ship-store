import re
from decimal import Decimal

import requests
from bs4 import BeautifulSoup

from main.settings import URL_SCRAPING_DOMAIN, URL_SCRAPING
from shop.models import Product


class ScrapingError(Exception):
    pass


class ScrapingTimeoutError(ScrapingError):
    pass


class ScrapingHTTPError(ScrapingError):
    pass


class ScrapingOtherError(ScrapingError):
    pass


def scraping():
    try:
        resp = requests.get(URL_SCRAPING, timeout=10.0)
    except requests.exceptions.Timeout:
        raise ScrapingTimeoutError('request timed out')
    except Exception as e:
        raise ScrapingOtherError(f'{e}')

    if resp.status_code != 200:
        raise ScrapingHTTPError(f'HTTP {resp.status_code}: {resp.text}')

    # resp = requests.get(URL_SCRAPING, timeout=10.0)
    # if resp.status_code != 200:
    #     raise Exception('HTTP ошибка входа!')

    data_list = []
    html = resp.text

    # print(f'HTML-текст имеет {len(html)} cимволов')
    # print(50 * '$')
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.select('.card-catalog-wide.pt-flex.pt-justify-between ')

    for block in blocks:
        data = {}
        name = block.select_one('.pt-typography____JqPt.pt-t-label-md-s-mid___mT510.pt-ta-left.pt-c-secondary.pt-wrap '
                                ).get_text().strip()
        data['name'] = name

        image_url = 'https:' + block.select_one('img')['src']
        data['image_url'] = image_url

        price_raw = block.select_one(".pt-price___c9u6v.pt-price-cp___tzloY ").text
        price = Decimal(''.join(re.findall(r'\d+', price_raw)))
        data['price'] = price

        unit = block.select_one('.pt-tabs-scrolled-content___dlBuU').text.strip() + ' штуку'
        data['unit'] = unit

        url_detail = block.select_one('.pt-link___JRuYu.pt-link-primary___Am9vu.pt-link-md___Yhrk7')
        url_detail = url_detail['href']
        url_detail = URL_SCRAPING_DOMAIN + url_detail

        html_detail = requests.get(url_detail).text
        soup = BeautifulSoup(html_detail, 'html.parser')
        code_block = soup.select_one(".code.pt-split-sm-xs-s").text
        code = re.findall(r'\d+', code_block)
        code = int(*code)
        data['code'] = code

        data_list.append(data)

        # print(data)

        # print(f'HTML-текс имеет {len(block.text)} символов')
        # print(80 * '=')
        # print(block.text)
        # break

    for item in data_list:
        if not Product.objects.filter(code=item['code']).exists():
            Product.objects.create(
                name=item['name'],
                code=item['code'],
                image_url=item['image_url'],
                unit=item['unit'],
                price=item['price'],
            )
    return data_list


if __name__ == '__main__':
    scraping()
