import requests
import random
from typing import List, Dict
import json

# Прокси и аутентификационные данные
PROXIES = [
    'http://sashabodiul07:7UMNo7iRr6@91.124.86.145:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.99.49:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.87.70:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.84.115:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.95.74:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.98.106:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.97.133:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.92.6:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.96.5:50100',
    'http://sashabodiul07:7UMNo7iRr6@91.124.93.253:50100'
]

# Заголовки
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'Bearer correct_token'
}

def get_random_proxy() -> Dict[str, str]:
    proxy = random.choice(PROXIES)
    return {
        'http': proxy,
        'https': proxy
    }

def search_github(keyword: str, search_type: str, max_retries: int = 5) -> List[Dict[str, str]]:
    base_url = 'https://api.github.com/search/repositories'
    search_results = []

    params = {
        'q': keyword,
        'type': search_type
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, headers=HEADERS, params=params, proxies=get_random_proxy(), timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            print(f"Error fetching search results for {keyword}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying ({attempt + 1}/{max_retries})...")
            else:
                print(f"Max retries reached for {keyword}")
                return []

    if response.status_code == 200:
        response_json = response.json()
        if 'items' in response_json:
            for item in response_json['items']:
                search_results.append({'url': item['html_url']})
    else:
        print(f"Failed to retrieve search results for {keyword}: status code {response.status_code}")

    return search_results

if __name__ == '__main__':

    input_data = {
                "keywords": ["openstack", "nova", "css"],
                "type": "Repositories"
            }

    all_results = []
    for keyword in input_data["keywords"]:
        results = search_github(keyword, input_data["type"])
        all_results.extend(results)

    print(json.dumps(all_results, indent=2, ensure_ascii=False))
