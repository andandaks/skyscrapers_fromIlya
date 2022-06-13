import telebot
import settings
import random
from PIL import Image, ImageDraw
import requests
import urllib.request
from bs4 import BeautifulSoup as bs

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "X-Amzn-Trace-Id": "Root=1-614b72cf-3af194f55b95c13d138986c5"
}


bot = telebot.Telebot('5305839756:AAGcAim61mtdQSTKooxKfFZG9TNjtJ-xmAw')

r = requests.get('https://www.dreamstime.com/photos-images/skyscraper.html', headers = headers)
soup = bs(r.content, features="lxml")
imgs = soup.find_all('img')
photos = []
for i in imgs:
    try:
        photos.append(i['data-src'])
    except Exception:
        pass
    print(photos)

def returnphoto(message, photos):
    a = random.randint(1, len(photos) - 1)
    urllib.request.urlretrieve(
        photos[a],
        "skys.jpg")

    img = Image.open("skys.jpg")
    try:
        img.thumbnail((300, 300))
        title_text = message.text
        image_editable = ImageDraw.Draw(img)
        res = image_editable.text((100, 15), title_text, size=10, fill=(255, 0, 0))
    except Exception:
        pass

    return img


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Напиши мне название города и я скину тебе "его" фото')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_photo(message.chat.id, returnphoto(message, photos))


bot.polling(none_stop=True, interval=0)



