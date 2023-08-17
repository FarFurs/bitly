import requests
import os
from dotenv import load_dotenv




def is_bitlink(token, url):
    url = url.strip("https://")
    headers = {
        'Authorization': f'Bearer {token}',
    }   

    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{url}', headers=headers)
    if response.status_code != 404:
        return True
    # pass


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {"long_url": url,
            "domain": "bit.ly",
            }
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=data)
    response.raise_for_status()
    return response.json()


def count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {'unit': 'month', 'units': '1'}
    # params = json.dumps(params)
    link = link.strip('https://')
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
    _BITLY_TOKEN = os.environ['BITLY_TOKEN']

    url = input('Введите ссылку: ')
    try:
        if is_bitlink(_BITLY_TOKEN, url):
            clicks = count_clicks(_BITLY_TOKEN, url)
            print('Клики', clicks)
        else:
            data = shorten_link(_BITLY_TOKEN, url)
            print('Битлинк ', data['link'])
    except requests.exceptions.HTTPError:
        print('Ошибка')


if __name__ == '__main__':
    main()
