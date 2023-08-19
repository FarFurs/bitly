import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse




def is_bitlink(token, url):
    url = url.replace(f'{urlparse(url).scheme}://', '', 1)
    headers = {
        'Authorization': f'Bearer {token}',
    }   

    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{url}', headers=headers)
    return response.ok


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    long_url = {"long_url": url}
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=long_url)
    response.raise_for_status()
    return response.json()


def count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {'unit': 'month', 'units': '1'}
    link = link.replace(f'{urlparse(link).scheme}://', '', 1)
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary',
        headers=headers,
        params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def main() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    bitly_token = os.environ['BITLY_TOKEN']

    url = input('Введите ссылку: ')
    try:
        if is_bitlink(bitly_token, url):
            clicks = count_clicks(bitly_token, url)
            print('Клики', clicks)
        else:
            shorten_link_content = shorten_link(bitly_token, url)
            print('Битлинк ', shorten_link_content['link'])
    except requests.exceptions.HTTPError:
        print('Вы ввели неверную ссылку или неверный токен')


if __name__ == '__main__':
    main()
