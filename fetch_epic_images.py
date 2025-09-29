import argparse
import os
import requests
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


def build_epic_image_url(item, api_key):
    """Строит URL изображения EPIC по данным item"""
    date = item["date"].split()[0]
    year, month, day = date.split("-")
    image_name = item["image"]
    return f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"


def download_epic_images(data, api_key, count=5, folder="epic_images"):
    """Скачивает изображения EPIC в указанную папку"""
    os.makedirs(folder, exist_ok=True)
    for item in data[:count]:
        image_url = build_epic_image_url(item, api_key)
        filename = get_filename_from_url(image_url)
        save_path = os.path.join(folder, filename)
        download_image(image_url, save_path)


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