import os
import random
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv
import telegram
from telegram.error import NetworkError, TimedOut, RetryAfter, TelegramError


def get_images(path="images"):
    """Собирает список всех картинок в папке"""
    images = [f for f in Path(path).glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
    if not images:
        raise FileNotFoundError("Нет изображений в папке images/")
    return images


def publish_images(bot, channel, images, interval_minutes, max_retries=5):
    """Публикует фото из списка с указанным интервалом"""
    while True:
        random.shuffle(images)  # перемешиваем перед циклом
        for image_path in images:
            retries = 0
            while retries < max_retries:
                try:
                    with open(image_path, "rb") as image_file:
                        bot.send_photo(chat_id=channel, photo=image_file, caption="Фото из космоса")
                    print(f"Фото опубликовано: {image_path}")
                    break  # успешно, выходим из цикла попыток
                except (NetworkError, TimedOut) as e:
                    retries += 1
                    wait_time = 5 * retries  # нарастающий интервал
                    print(f"Сетевая ошибка: {e}. Повтор через {wait_time} сек. (Попытка {retries}/{max_retries})")
                    time.sleep(wait_time)
                except RetryAfter as e:
                    # Если Telegram говорит подождать, соблюдаем задержку
                    wait_time = e.retry_after
                    print(f"Telegram запросил паузу: {wait_time} сек.")
                    time.sleep(wait_time)
                except TelegramError as e:
                    # Другие ошибки Telegram — логируем и пропускаем
                    print(f"Ошибка Telegram: {e}. Пропускаем фото {image_path}.")
                    break

            # Пауза между публикациями
            time.sleep(interval_minutes * 60)  # переводим минуты в секунды


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Telegram publisher")
    parser.add_argument("--folder", help="Папка с фотографиями", default="images")
    parser.add_argument("--interval", type=int, help="Интервал публикации (в минутах)")
    args = parser.parse_args()

    token = os.getenv("TELEGRAM_TOKEN")
    channel = os.getenv("TELEGRAM_CHAT_ID")
    interval_minutes = args.interval or int(os.getenv("TELEGRAM_INTERVAL_MINUTES", 240))

    if not token or not channel:
        print("Ошибка: TELEGRAM_TOKEN или TELEGRAM_CHAT_ID не указаны.")
        return

    bot = telegram.Bot(token=token)
    images = get_images(args.folder)
    publish_images(bot, channel, images, interval_minutes)


if __name__ == "__main__":
    main()
