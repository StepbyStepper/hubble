import argparse
import os
import requests
from dotenv import load_dotenv
from utils import download_image, get_filename_from_url

def fetch_nasa_apod(api_key, count=5):
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}
    response = requests.get(url, params=params)

    if not response.ok:
        print(f"Ошибка API NASA: {response.status_code}")
        return

    os.makedirs("nasa_images", exist_ok=True)
    for data in response.json():
        if data.get("media_type") != "image":
            continue
        image_url = data.get("hdurl") or data.get("url")
        title = data.get("title", "Без названия")
        filename = get_filename_from_url(image_url)
        save_path = os.path.join("nasa_images", filename)
        download_image(image_url, save_path)
        print(f"Скачано: {title}")

def main():
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        print("Ошибка: нет API ключа NASA.")
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5, help="Сколько фото скачать")
    args = parser.parse_args()

    fetch_nasa_apod(api_key, args.count)

if __name__ == "__main__":
    main()
