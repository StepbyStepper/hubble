import argparse
import urllib.parse
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils import download_image, get_filename_from_url


def fetch_epic_data(api_key):
    """Получает данные EPIC с NASA API"""
    api_url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": api_key}
    response = requests.get(api_url, params=params)

    if not response.ok:
        raise RuntimeError(f"Ошибка API EPIC: {response.status_code}")

    epic_data = response.json()
    if not epic_data:
        raise ValueError("Нет данных EPIC.")

    return epic_data


def parse_epic_date(date_str):
    """
    Парсит дату из поля item['date'].
    Несколько форматов: fromisoformat, strptime.
    Возвращает datetime.
    """
    if not date_str:
        raise ValueError("Пустая строка даты")

    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        pass

    formats = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d")
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue

    try:
        date_part = date_str.split()[0]
        return datetime.strptime(date_part, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Не удалось распарсить дату: {date_str}")


def build_epic_image_url(epic_item, api_key):
    """Строит URL изображения EPIC по данным item"""
    date_str = epic_item.get("date")
    epic_date = parse_epic_date(date_str)

    year = epic_date.strftime("%Y")
    month = epic_date.strftime("%m")  # две цифры с ведущим нулём
    day = epic_date.strftime("%d")

    epic_image_name = epic_item["image"]

    image_base_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{epic_image_name}.png"
    query_params = {"api_key": api_key}

    # Формируем URL с GET-параметрами
    query_string = urllib.parse.urlencode(query_params)
    image_full_url = f"{image_base_url}?{query_string}"
    return image_full_url

def download_epic_images(data, api_key, count=5, folder="epic_images"):
    """Скачивает изображения EPIC в указанную папку"""
    os.makedirs(folder, exist_ok=True)
    for epic_item in data[:count]:
        try:
            image_url = build_epic_image_url(epic_item, api_key)
        except Exception as e:
            # если дата или данные некорректны — логируем и продолжаем
            print(f"Пропущен элемент: {e}")
            continue

        photo_filename = get_filename_from_url(image_url)
        photo_save_path = os.path.join(folder, photo_filename)
        try:
            download_image(image_url, photo_save_path)
        except Exception as e:
            print(f"Ошибка при скачивании {image_url}: {e}")


def main():
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        print("Ошибка: нет API ключа NASA.")
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5, help="Сколько фото скачать")
    args = parser.parse_args()

    try:
        epic_data = fetch_epic_data(api_key)
        download_epic_images(epic_data, api_key, args.count)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
