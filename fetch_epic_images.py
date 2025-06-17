import argparse
import os
import requests
from dotenv import load_dotenv
from utils import download_image, get_filename_from_url

def fetch_epic_images(api_key, count=5):
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Ошибка API EPIC: {response.status_code}")
        return

    data = response.json()
    if not data:
        print("Нет данных EPIC.")
        return

    os.makedirs("epic_images", exist_ok=True)
    for item in data[:count]:
        date = item["date"].split()[0]
        year, month, day = date.split("-")
        image_name = item["image"]

        image_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"
        )

        filename = get_filename_from_url(image_url)
        save_path = os.path.join("epic_images", filename)
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

    fetch_epic_images(api_key, args.count)

if __name__ == "__main__":
    main()
