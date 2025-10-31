import telebot
import requests
import json
from datetime import datetime

bot = telebot.TeleBot()
API = '2b53e058fbceb64260976bf6fe6b16e4'

user_cities = {}

@bot.message_handler(commands=["setcity"])
def set_city(message):
    try:   
        city = message.text.split(maxsplit=1)[1]
        user_cities[message.from_user.id] = city
        bot.reply_to(message, f"✅ Город по умолчанию сохранён: {city}")
    except IndexError:
        bot.reply_to(message, "❌ Укажи город, например:\n/setcity Алматы")

@bot.message_handler(commands=["mycity"])
def my_city(message):
    city = user_cities.get(message.from_user.id)
    if city:
        send_weather(message, city)
    else:
        bot.reply_to(message, "⚠️ У тебя ещё не сохранён город. Используй /setcity <город>")

@bot.message_handler(commands=["start"])
def start(message):

    markup = telebot.types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id,
    "Привет! 👋\n"
    "Я бот, который показывает погоду в любом городе мира. 🌍☀️🌧️\n\n"
    "Отправь мне название города.\n\n"
    "Команды:\n"
    "/start – начать работу\n"
    "/help – помощь\n"
    "/setcity «Город» – сохранить город по умолчанию\n"
    "/mycity – показать погоду в сохранённом городе\n\n"
    "Напиши город прямо сейчас!"
    )

@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(message.chat.id,
    "Вот что я умею:\n\n"
    "/start – приветствие и инструкция\n"
    "/help – список команд\n"
    "/setcity <Город> – сохранить город по умолчанию\n"
    "/mycity – показать погоду в сохранённом городе\n\n"
    "Или просто напиши название города 😉"
    )

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip()
    send_weather(message, city)

def send_weather(message, city):
    if not city:
        bot.reply_to(message, "❌ Укажи название города!")
        return

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru'
    res = requests.get(url)

    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        feels = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        speed = data['wind']['speed']
        deg = data['wind']['deg']

        weather_main = data['weather'][0]['main']
        description = data['weather'][0]['description'].capitalize()

        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧",
            "Drizzle": "🌦",
            "Thunderstorm": "⛈",
            "Snow": "❄️",
            "Mist": "🌫",
            "Fog": "🌫",
        }
        emoji = icons.get(weather_main, "🌍")
    
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"

        all_clouds = data['clouds']['all']
        visibility = data.get('visibility', 0)

        timezone_shift = data['timezone']  
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + timezone_shift).strftime('%H:%M')
        sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + timezone_shift).strftime('%H:%M')

        city_name = data['name']

        caption = (
            f"🌍 Погода в {city_name}:\n\n"
            f"🌡 Температура: {temp}°C (ощущается как {feels}°C)\n"
            f"🔻 Мин: {temp_min}°C | 🔺 Макс: {temp_max}°C\n\n"
            f"💨 Ветер: {speed} м/с, {deg}°\n"
            f"💧 Влажность: {humidity}%\n"
            f"📊 Давление: {pressure} гПа\n"
            f"☁️ Облачность: {all_clouds}%\n"
            f"👁 Видимость: {visibility} м\n"
            f"🌤 Условия: {emoji} {description}\n\n"
            f"🌅 Восход: {sunrise}\n"
            f"🌇 Закат: {sunset}"
        )

        bot.send_photo(message.chat.id, icon_url, caption=caption)

    else:
        bot.reply_to(message, "❌ Город указан неверно!")

bot.polling(none_stop=True)

