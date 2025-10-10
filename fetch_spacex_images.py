import argparse
import os
import requests
from utils import download_image, get_filename_from_url

SPACEX_API_URL = "https://api.spacexdata.com/v5/launches"

def get_spacex_photos(launch_id=None):
    api_url = SPACEX_API_URL if not launch_id else f"{SPACEX_API_URL}/{launch_id}"
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    if launch_id:
        launch_photos = data.get("links", {}).get("flickr", {}).get("original", [])
        return launch_photos
    else:
        for launch in reversed(data):
            launch_photos = launch.get("links", {}).get("flickr", {}).get("original", [])
            if launch_photos:
                return launch_photos
        return []

def list_launches(launch_limit=10):
    response = requests.get(SPACEX_API_URL)
    response.raise_for_status()
    recent_launches = response.json()

    for launch in reversed(recent_launches[-launch_limit:]):
        launch_name = launch.get("name")
        launch_date = launch.get("date_utc", "N/A")[:10]
        launch_id = launch.get("id")
        print(f"{launch_name} | {launch_date} | ID: {launch_id}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch_id", help="ID запуска SpaceX")
    parser.add_argument("--list", action="store_true", help="Показать список последних запусков")
    args = parser.parse_args()

    if args.list:
        list_launches()
        return

    try:
        photos_to_download = get_spacex_photos(args.launch_id)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")

    if not photos_to_download:
        print("Нет фото для скачивания.")
        return

    for photo_url in photos_to_download:
        photo_filename = get_filename_from_url(photo_url)
        photo_save_path = os.path.join("images", photo_filename)
        try:
            download_image(photo_url, photo_save_path)
        except requests.RequestException as e:
            print(f"Ошибка при скачивании {photo_url}: {e}")
        except OSError as e:
            print(f"Ошибка при сохранении {photo_save_path}: {e}")


if __name__ == "__main__":
    main()
