import os
import requests
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv


def get_file_extension(url):
    path = urlparse(url).path
    _, ext = os.path.splitext(path)
    return ext

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    filename = unquote(filename)
    return filename

def get_latest_spacex_photos():
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url)

    if response.status_code == 200:
        launches = response.json()

        for launch in reversed(launches):
            photos = launch.get("links", {}).get("flickr", {}).get("original", [])
            if photos:
                return photos

        print("Фотографий не найдено в недавних запусках.")
        return []
    else:
        print(f"Ошибка при запросе данных: {response.status_code}")
        return []


def download_image(image_url: str, save_path: str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    response = requests.get(image_url, stream=True)

    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Изображение сохранено: {save_path}")
    else:
        print(f"Ошибка скачивания {image_url}: {response.status_code}")


def fetch_spacex_last_launch():
    photo_links = get_latest_spacex_photos()

    if photo_links:
        for photo_url in photo_links:
            filename = get_filename_from_url(photo_url)
            save_path = os.path.join("images", filename)
            download_image(photo_url, save_path)
    else:
        print("Нет доступных фото для скачивания.")

def fetch_nasa_apod(api_key, count=5):
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "count": count
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data_list = response.json()

        os.makedirs("nasa_images", exist_ok=True)

        for data in data_list:
            image_url = data.get("hdurl") or data.get("url")
            title = data.get("title")

            if image_url and data.get("media_type") == "image":
                filename = get_filename_from_url(image_url)
                save_path = os.path.join("nasa_images", filename)

                download_image(image_url, save_path)
                print(f"Фото NASA '{title}' сохранено как {save_path}")
            else:
                print(f"Пропущен элемент без изображения: {data.get('title', 'Без названия')}")
    else:
        print(f"Ошибка API NASA: {response.status_code}")

def fetch_epic_images(api_key, count=5):
    url = "https://api.nasa.gov/EPIC/api/natural"
    params = {"api_key": api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            os.makedirs("epic_images", exist_ok=True)

            for item in data[:count]:
                image_name = item['image']
                date_str = item['date']
                date_parts = date_str.split(" ")[0].split("-")

                image_url = (
                    f"https://api.nasa.gov/EPIC/archive/natural/"
                    f"{date_parts[0]}/{date_parts[1]}/{date_parts[2]}/png/"
                    f"{image_name}.png?api_key={api_key}"
                )

                filename = get_filename_from_url(image_url)
                save_path = os.path.join("epic_images", filename)

                download_image(image_url, save_path)
        else:
            print("Нет доступных фото EPIC.")
    else:
        print(f"Ошибка API EPIC: {response.status_code}")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("NASA_API_KEY")
    fetch_spacex_last_launch()
    fetch_nasa_apod(api_key, count=5)
    fetch_epic_images(api_key, count=5)