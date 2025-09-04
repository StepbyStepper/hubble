import os
import random
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv
import telegram


def get_images(path="images"):
    """Собирает список всех картинок в папке"""
    images = [f for f in Path(path).glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    if not images:
        raise FileNotFoundError("Нет изображений в папке images/")
    return images


def publish_images(bot, channel, images, interval_minutes):
    """Публикует фото из списка с указанным интервалом"""
    while True:
        random.shuffle(images)  # перемешиваем перед циклом
        for image_path in images:
            with open(image_path, "rb") as image_file:
                bot.send_photo(chat_id=channel, photo=image_file, caption="📷 Фото из космоса")
            print(f"Фото опубликовано: {image_path}")
            time.sleep(interval_minutes * 60)  # переводим минуты в секунды


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Telegram publisher")
    parser.add_argument("--folder", help="Папка с фотографиями", default="images")
    parser.add_argument("--interval", type=int, help="Интервал публикации (в минутах)")
    args = parser.parse_args()

    token = os.getenv("TG_TOKEN")
    channel = os.getenv("CHANNEL_ID")
    interval_minutes = args.interval or int(os.getenv("TG_INTERVAL_MINUTES", 240))

    if not token or not channel:
        print("Ошибка: TG_TOKEN или CHANNEL_ID не указаны.")
        return

    bot = telegram.Bot(token=token)
    images = get_images(args.folder)
    publish_images(bot, channel, images, interval_minutes)


if __name__ == "__main__":
    main()
