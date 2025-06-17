import argparse
import os
import requests
from utils import download_image, get_filename_from_url

SPACEX_API_URL = "https://api.spacexdata.com/v5/launches"

def get_spacex_photos(launch_id=None):
    url = SPACEX_API_URL if not launch_id else f"{SPACEX_API_URL}/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if launch_id:
        photos = data.get("links", {}).get("flickr", {}).get("original", [])
        return photos
    else:
        for launch in reversed(data):
            photos = launch.get("links", {}).get("flickr", {}).get("original", [])
            if photos:
                return photos
        return []

def list_launches(limit=10):
    response = requests.get(SPACEX_API_URL)
    response.raise_for_status()
    launches = response.json()

    for launch in reversed(launches[-limit:]):
        name = launch.get("name")
        date = launch.get("date_utc", "N/A")[:10]
        launch_id = launch.get("id")
        print(f"{name} | {date} | ID: {launch_id}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch_id", help="ID запуска SpaceX")
    parser.add_argument("--list", action="store_true", help="Показать список последних запусков")
    args = parser.parse_args()

    if args.list:
        list_launches()
        return

    try:
        photos = get_spacex_photos(args.launch_id)
        if not photos:
            print("Нет фото для скачивания.")
            return

        for url in photos:
            filename = get_filename_from_url(url)
            save_path = os.path.join("images", filename)
            download_image(url, save_path)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")

if __name__ == "__main__":
    main()
