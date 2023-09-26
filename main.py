import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def is_bitlink(token, url):
    url = urlparse(url)._replace(scheme='')
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
        headers=headers
    )
    return response.ok


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    long_url = {"long_url": url}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=long_url
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {'unit': 'month', 'units': '1'}
    link = link.replace(f'{urlparse(link).scheme}://', '', 1)
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary',
        headers=headers,
        params=params
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def main() -> None:

    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']

    parser = argparse.ArgumentParser(description='Ссылка для работы')
    parser.add_argument(
        'url',
        help='Ссылка',
        type=str
    )
    args = parser.parse_args()
    url = args.url

    try:
        if is_bitlink(bitly_token, url):
            clicks = count_clicks(bitly_token, url)
            print('Клики', clicks)
        else:
            short_link = shorten_link(bitly_token, url)
            print('Битлинк ', short_link)
    except requests.exceptions.HTTPError:
        print('Вы ввели неверную ссылку или неверный токен')


if __name__ == '__main__':
    main()
