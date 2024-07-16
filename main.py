import json
from crawler import search_github

def main():
    input_data = {
            "keywords": ["openstack", "nova", "css"],
            "type": "Repositories"
        }

    all_results = []
    for keyword in input_data["keywords"]:
        results = search_github(keyword, input_data["type"])
        all_results.extend(results)

    print(json.dumps(all_results, indent=2, ensure_ascii=False))
# Пример использования функции
if __name__ == '__main__':
    main()