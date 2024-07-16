# GitHub Crawler

## Описание

Этот скрипт реализует краулер для поиска по GitHub, который возвращает все ссылки из результатов поиска. Скрипт поддерживает прокси и аутентификацию.

## Требования

- Python 3.12
- requests
- beautifulsoup4
- aiohttp
- json

## Установка

Установите необходимые связи:
```bash
pyenv install 3.12
pyenv local 3.12
poetry shell
poetry install