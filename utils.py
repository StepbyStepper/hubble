import os
import requests
from urllib.parse import urlparse, unquote

def get_file_extension(url):
    path = urlparse(url).path
    _, ext = os.path.splitext(path)
    return ext

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    return unquote(filename)

def download_image(image_url: str, save_path: str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(image_url, stream=True)

    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Сохранено: {save_path}")
    else:
        print(f"Ошибка загрузки {image_url}: {response.status_code}")
