import telebot
import requests
import datetime

bot = telebot.TeleBot("6260432849:AAEFDQaAU8Z21VGMCiBNpra5WJnb4Neq3RY")

def now_time_func(timezone):
    return datetime.datetime.utcnow() + datetime.timedelta(seconds=timezone)

def time_func(sunrise, sunset, timezone):
  now = datetime.datetime.utcnow()
  epoch = datetime.datetime(1970, 1, 1)
  elapsed = now - epoch
  now_seconds = int(elapsed.total_seconds())
  sunrise_delta = datetime.timedelta(seconds=(now_seconds - sunrise - timezone))
  sunset_delta = datetime.timedelta(seconds=(now_seconds - sunset - timezone))
  sunrise_time = now - sunrise_delta
  sunset_time = now - sunset_delta
  return "Восход: " + sunrise_time.strftime('%H:%M') + " | Закат: " + sunset_time.strftime('%H:%M')

def func(city):
  url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
  try:
    weather_data = requests.get(url).json()
    weather = weather_data['weather'][0]['description']
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    temp = str(round(weather_data['main']['temp']))
    humidity = str(weather_data['main']['humidity'])
    pressure = str(weather_data['main']['pressure'])
    wind_speed = str(weather_data['wind']['speed'])
    wind_deg = str(weather_data['wind']['deg'])
    sun = time_func(weather_data['sys']['sunrise'], weather_data['sys']['sunset'], weather_data['timezone'])
    visibility = weather_data['visibility']
    clouds = weather_data['clouds']['all']
    time = now_time_func(weather_data['timezone']).strftime('%H:%M')

    result = f'''Город {weather_data['name']} | Время {time}
Погода: {weather}
Температура: {temp}°C
Давление: {pressure} hPa | Влажность: {humidity}%
Облачность: {clouds}% | Видимость: {visibility} м.
Скорость ветра: {wind_speed} м/с
Направление ветра: {wind_deg}°
Широта {lat} Долгота {lon}
{sun}'''
    return result
  except:
    return "Город не найден"

@bot.message_handler(commands=['help', 'start'])
def start_message(message):
	bot.send_message(message.chat.id,'Введите город, чтобы узнать погоду.')

@bot.message_handler(content_types=["text"])
def text_messages(message):
    bot.send_message(message.chat.id, func(message.text))

bot.polling()
