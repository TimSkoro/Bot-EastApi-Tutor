import json
from random import choice

import redis
import requests
import telebot

from config import API_KEY

database = redis.Redis(host='localhost', port=6379, db=0)
bot = telebot.TeleBot(API_KEY)

temps = ["томно", "загадочно", "громко", "уверенно", "мило", "безумно", "быстро"]


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'all_news':
        news = requests.get('http://127.0.0.1:8000/news/').json()
        print(news)
        for n in news.get('result', []):
            mess = """
            **{title}**
            ------------------------------------------
            **{description}**
            """.format(**n)
            bot.send_message(message.from_user.id, mess)

    elif message.text.split(":")[0] == 'create':
        data = {
            'title': message.text.split(":")[1],
            'description': message.text.split(":")[2],
        }
        requests.post('http://127.0.0.1:8000/news/', data=json.dumps(data)).json()
        bot.send_message(message.from_user.id, 'published')

    elif message.text[0] == "{":
        data = json.loads(message.text)
        requests.post('http://127.0.0.1:8000/news/', data=json.dumps(data)).json()
        bot.send_message(message.from_user.id, 'published')


    elif message.text.split(" ")[0] == 'cmd':
        if database.get('info'):
            bot.send_message(message.from_user.id, database.get('info'))
        else:
            bot.send_message(message.from_user.id, 'no info')
        return

    raw_user_data = database.get('users') or b"{}"
    user_data = json.loads(raw_user_data)
    user_data[message.from_user.username] = message.from_user.id

    print(f"Message: {message.text} {message.from_user.username}")
    for user_id in user_data.values():
        if user_id != message.from_user.id:
            mess = f"- {message.text} - {choice(temps)} сказал(а) {message.from_user.username}"
            bot.send_message(user_id, mess)

    database.set('users', json.dumps(user_data))


bot.polling(none_stop=True, interval=0)
