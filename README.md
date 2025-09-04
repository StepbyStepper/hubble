# Hubble Project

# Загрузка космических изображений с NASA и SpaceX

Набор Python-скриптов для автоматической загрузки изображений с публичных API NASA и SpaceX.  
Каждый источник оформлен отдельным скриптом, все общие функции — в модуле `utils.py`.

## Установка

1. Клонируйте репозиторий или скачайте файлы.
2. Установите зависимости командой:

 ```bash
 pip install -r requirements.txt
 ```

3. Создайте файл `.env` в корне проекта и добавьте в него ваш NASA API ключ:
 ```bash
    NASA_API_KEY=ваш_ключ_от_nasa
    TG_TOKEN=ваш_api_токен_бота
    CHANNEL_ID=@имя_вашего_канала
    TG_INTERVAL_MINUTES=240 (интервал публикации в минутах (по умолчанию — 240 = 4 часа))
```

API ключ можно получить бесплатно на [https://api.nasa.gov/](https://api.nasa.gov/).

## Структура проекта

- `fetch_spacex_images.py` — скачивает фото запуска SpaceX по ID (через аргумент) или последнего запуска с фото, если ID не указан.
- `fetch_nasa_apod.py` — скачивает случайные APOD-фото NASA, количество задаётся параметром.
- `fetch_epic_images.py` — скачивает фото с камеры EPIC NASA, количество задаётся параметром.
- `utils.py` — общие вспомогательные функции для скачивания и обработки URL.
- `.env` — файл с переменными окружения.
- `requirements.txt` — список зависимостей.

## Использование

### SpaceX фотографии
```bash
python fetch_spacex_images.py                  # Скачать фото последнего запуска с фотографиями
python fetch_spacex_images.py --launch_id <ID> # Скачать фото по конкретному ID запуска
python fetch_spacex_images.py --list           # Показать список последних запусков (с ID)
```

### NASA APOD фотографии
```bash
python fetch_nasa_apod.py                       # Скачать 5 случайных APOD-фотографий (по умолчанию)
python fetch_nasa_apod.py --count 10            # Скачать 10 случайных APOD-фотографий
```

### NASA EPIC фотографии
```bash
python fetch_epic_images.py                      # Скачать 5 EPIC-фотографий (по умолчанию)
python fetch_epic_images.py --count 3            # Скачать 3 EPIC-фотографии
```

## Где сохраняются фотографии:
- SpaceX: папка images/
- NASA APOD: папка nasa_images/
- NASA EPIC: папка epic_images/


### Запуск скрипта автопостинга hubble_posting_bot.py
```bash
python hubble_posting_bot.py --folder images --interval 60

--folder — папка с фотографиями (по умолчанию images/).
--interval — интервал публикации в минутах. Если не указан, берётся из .env.
```