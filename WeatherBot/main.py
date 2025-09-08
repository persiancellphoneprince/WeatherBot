import telebot
import requests
import json
bot = telebot.TeleBot('7500717957:AAEk_FthUI1QzomiT-qqPaRjCEj_OL_efOM')
API = ''


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напишите название города!')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
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
        description = data['weather'][0]['description']
        all = data['clouds']['all']
        visibility = data['visibility']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']

        bot.reply_to(message, f'Погода сейчас: {temp}°C\nОщущается как: {feels}°C\nМинимальная температура: {temp_min}°C\nМаксимальная температура: {temp_max}°C\nДавление: {pressure} гПа\nВлажность: {humidity}%\nСкорость ветра: {speed} м/с\nНаправление ветра: {deg}°\nПогодные условия: {description}\nОблачность: {all}%\nВидимость: {visibility} м\nВосход солнца: {sunrise} UTC\nЗакат солнца: {sunset} UTC')

    else:
        bot.reply_to(message, f"Город указан не верно!")

bot.polling(none_stop=True)
