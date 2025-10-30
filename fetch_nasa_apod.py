import argparse
import os
import requests
from dotenv import load_dotenv
from utils import download_image, get_filename_from_url


def get_apod_data(api_key, count=5):
    """Получает JSON-данные от NASA APOD API."""
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}
    response = requests.get(url, params=params)

    if response.status_code == 403:
        raise RuntimeError("Доступ запрещён: проверьте свой API ключ NASA (403 Forbidden)")

    if not response.ok:
        raise RuntimeError(f"Ошибка API NASA: {response.status_code}")

    return response.json()


def save_apod_images(data):
    """Сохраняет изображения APOD из полученных данных."""
    os.makedirs("nasa_images", exist_ok=True)

    for item in data:
        if item.get("media_type") != "image":
            continue

        image_url = item.get("hdurl") or item.get("url")
        if not image_url:
            continue

        title = item.get("title", "Без названия")
        filename = get_filename_from_url(image_url)
        save_path = os.path.join("nasa_images", filename)

        download_image(image_url, save_path)
        print(f"Скачано: {title}")


def fetch_nasa_apod(api_key, count=5):
    """Основная функция: получает и сохраняет изображения APOD."""
    data = get_apod_data(api_key, count)
    save_apod_images(data)


def main():
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        print("Ошибка: нет API ключа NASA.")
        return

    parser = argparse.ArgumentParser(description="Скачивание изображений NASA APOD")
    parser.add_argument("--count", type=int, default=5, help="Сколько фото скачать")
    args = parser.parse_args()

    try:
        fetch_nasa_apod(api_key, args.count)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
    except RuntimeError as e:
        print(f"Ошибка API: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()
