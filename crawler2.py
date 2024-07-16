import aiohttp
import random
import json
import asyncio
from typing import List, Dict

# Your PROXIES and HEADERS definitions here

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

HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'Bearer correct_token'
}

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_repository_info(session, owner, repo_name):
    url = f'https://api.github.com/repos/{owner}/{repo_name}'
    try:
        async with session.get(url, headers=HEADERS, proxy=random.choice(PROXIES)) as response:
            response_json = await response.json()
            if 'language' in response_json:
                return {
                    'owner': owner,
                    'language_stats': response_json['language']
                }
            else:
                return None
    except aiohttp.ClientError as e:
        print(f"Error fetching repository info for {owner}/{repo_name}: {e}")
        return None

async def search_github(keywords: List[str], proxies: List[str], search_type: str) -> List[Dict[str, any]]:
    base_url = 'https://api.github.com/search/repositories'
    search_results = []

    async with aiohttp.ClientSession() as session:
        for keyword in keywords:
            params = {
                'q': keyword,
                'type': search_type
            }

            try:
                async with session.get(base_url, headers=HEADERS, params=params, proxy=random.choice(proxies)) as response:
                    response_json = await response.json()
                    if 'items' in response_json:
                        tasks = []
                        for item in response_json['items']:
                            owner = item['owner']['login']
                            repo_name = item['name']
                            tasks.append(get_repository_info(session, owner, repo_name))

                        results = await asyncio.gather(*tasks)
                        for result in results:
                            if result:
                                search_results.append({
                                    'url': f"https://github.com/{result['owner']}/{repo_name}",
                                    'extra': result
                                })
            except aiohttp.ClientError as e:
                print(f"Error fetching search results for {keyword}: {e}")

    return search_results

if __name__ == '__main__':
    input_data = {
        "keywords": ["python", "django-rest-framework", "jwt"],
        "proxies": ["http://sashabodiul07:7UMNo7iRr6@91.124.86.145:50100", "http://sashabodiul07:7UMNo7iRr6@91.124.87.70:50100"],
        "type": "Repositories"
    }

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(search_github(input_data["keywords"], input_data["proxies"], input_data["type"]))
        print(json.dumps(results, indent=2, ensure_ascii=False))
    finally:
        loop.close()