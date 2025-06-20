import telegram
import os
import random
from dotenv import load_dotenv


def get_random_image(path="images"):
    images = [f for f in os.listdir(path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not images:
        raise FileNotFoundError("Нет изображений в папке images/")
    return os.path.join(path, random.choice(images))

def main():
    load_dotenv()
    token = os.getenv("TG_TOKEN")
    channel = os.getenv("CHANNEL_ID")

    if not token or not channel:
        print("Ошибка: TG_TOKEN или TG_CHANNEL не указаны.")
        return

    bot = telegram.Bot(token=token)
    image_path = get_random_image()

    with open(image_path, "rb") as image_file:
        bot.send_photo(chat_id=channel, photo=image_file, caption="📷 Фото из космоса")

    print(f"Фото опубликовано: {image_path}")


if __name__ == "__main__":
    main()