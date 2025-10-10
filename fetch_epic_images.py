import argparse
import urllib.parse
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils import download_image, get_filename_from_url


def fetch_epic_data(api_key):
    """Получает данные EPIC с NASA API"""
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)

    if not response.ok:
        raise RuntimeError(f"Ошибка API EPIC: {response.status_code}")

    data = response.json()
    if not data:
        raise ValueError("Нет данных EPIC.")

    return data


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
        date_only = date_str.split()[0]
        return datetime.strptime(date_only, "%Y-%m-%d")
    except Exception:
        raise ValueError(f"Не удалось распарсить дату: {date_str}")


def build_epic_image_url(item, api_key):
    """Строит URL изображения EPIC по данным item"""
    date_str = item.get("date")
    date_obj = parse_epic_date(date_str)

    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")  # две цифры с ведущим нулём
    day = date_obj.strftime("%d")

    image_name = item["image"]

    base_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
    params = {"api_key": api_key}

    # Формируем URL с GET-параметрами
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"
    return full_url

def download_epic_images(data, api_key, count=5, folder="epic_images"):
    """Скачивает изображения EPIC в указанную папку"""
    os.makedirs(folder, exist_ok=True)
    for item in data[:count]:
        try:
            image_url = build_epic_image_url(item, api_key)
        except Exception as e:
            # если дата или данные некорректны — логируем и продолжаем
            print(f"Пропущен элемент: {e}")
            continue

        filename = get_filename_from_url(image_url)
        save_path = os.path.join(folder, filename)
        try:
            download_image(image_url, save_path)
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
        data = fetch_epic_data(api_key)
        download_epic_images(data, api_key, args.count)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
