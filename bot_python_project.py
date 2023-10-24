import telebot
import requests

from datetime import datetime, timedelta

API_TOKEN = '6508905936:AAGA8M0d1nKSMjtc_ENHe_FbMqsTEr5-AoI'


bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("1 До Нового года")
    item2 = telebot.types.KeyboardButton("2 Курс биткойна")
    item3 = telebot.types.KeyboardButton("3 Погода")
    item4 = telebot.types.KeyboardButton("4 Новости")
    item5 = telebot.types.KeyboardButton("5 Информация о создателе")
    markup.row(item1, item2)
    markup.row(item3, item4)
    markup.row(item5)

    bot.send_message(message.chat.id, "Привет! Выберите раздел:", reply_markup=markup)




#Считаем сколько дней до нового года
def time_until_new_year():
    now = datetime.now()
    new_year = datetime(now.year + 1, 1, 1, 0, 0, 0)
    time_left = new_year - now
    return time_left

# Про новый год
@bot.message_handler(func=lambda message: message.text == "1 До Нового года")
def send_time_until_new_year(message):
    time_left = time_until_new_year()
    days = time_left.days
    hours, seconds = divmod(time_left.seconds, 3600)
    minutes = seconds // 60
    response = f"До Нового года осталось: {days} дней, {hours} часов, {minutes} минут."
    bot.send_message(message.chat.id, response)




@bot.message_handler(func=lambda message: message.text == "2 Курс биткойна")
def bitcoin_price(message):
    # Использую API для получения инфы  о курсе биткоина с сайта CoinGecko
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=rub")
    data = response.json()
    bitcoin_price_rub = data["bitcoin"]["rub"]
    bot.send_message(message.chat.id, f"Курс биткойна в рублях: {bitcoin_price_rub} рублей")

@bot.message_handler(func=lambda message: message.text == "3 Погода")
def weather(message):
    bot.send_message(message.chat.id, "Введите город:")
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text

    api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
    response = requests.get(api_url, headers={'X-Api-Key': 'e+oV995SWeeN3L31NZg0FA==Xf0UJY6cbFuBeu7i'})
    if response.status_code == requests.codes.ok:
        l = list(response.text.split(","))
        temperatura = l[1].split(" ")
        Vlagnost =l[3].split(" ")
        Veter = l[6].split(" ")
        tex_for_pogoda = (f"Температура {temperatura[2]}°C \n"
                          f"Влажность воздуха {Vlagnost[2]}г/м³ \n"
                          f"Ветер {Veter[2]}м/c")

        bot.send_message(message.chat.id, tex_for_pogoda)
    else:
        bot.send_message(message.chat.id, "Заново нажмите на пункт в меню '4 Погода', введя корректное название города")





# Обработчик команды "4 Новости"
@bot.message_handler(func=lambda message: message.text == "4 Новости")
def send_hse_news(message):
    try:
        # Запрос на получение новостей из России
        news_url = f'https://newsapi.org/v2/top-headlines?country=ru&apiKey=159c7d4abc88433b8dc6f6b1321abfdc'
        response = requests.get(news_url)
        news_data = response.json()

        if news_data.get('status') == 'ok' and news_data.get('totalResults') > 0:
            # Отправляем первую новость из списка
            first_news = news_data['articles'][0]
            news_text = f"{first_news['title']}\n{first_news['url']}"
            bot.send_message(message.chat.id, news_text)
        else:
            bot.send_message(message.chat.id, "Извините, новости не найдены.")

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при получении новостей.")





@bot.message_handler(func=lambda message: message.text == "5 Информация о создателе")
def creator_info(message):
    bot.send_message(message.chat.id, "Этот бот был создан Рубекиным Егором Андреевичем группа БКНАД231.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
