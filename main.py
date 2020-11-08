import requests
from bs4 import BeautifulSoup
from settings import dictionaries
from settings import headers
import telebot
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types

# Указываем токен нашего бота
bot = telebot.TeleBot("1434135090:AAEX5YOPjOWwidXaQ3aLybcnyqMzHtmWy5E")


# Делаем декоратор для старт и хелп
@bot.message_handler(commands=["start", "help"])
def start_help(message):
    # Придумываем сообщение на старт и хелп
    msg = "Привет! Тут ты можешь набрать слово, я поищу слово в словарях и предложу их на выбор, конечно, " \
          "если найду :). Сейчас ты можешь вбить слово: "
    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, msg)


# Делаем декоратор для любого текста, то есть для слова
@bot.message_handler(content_types=["text"])
def new_word(message):
    count = 0
    keyboard = types.InlineKeyboardMarkup()
    word = str(message.text)
    for i in range(0, len(dictionaries)):
        url = dictionaries[i][0] + word[0] + '/' + word
        req = requests.get(url, headers=headers, timeout=5)
        if req.status_code == 200:
            count += 1
            keyboard.add(types.InlineKeyboardButton(text=dictionaries[i][1], callback_data=str(i) + ' ' + word))
    if count == 0:
        msg = "Упс, а слова " + word + " нет в наших словарях ¯\_(ツ)_/¯. Попробуй другое :) "
        bot.send_message(message.chat.id, msg)
    elif count > 0:
        bot.send_message(message.from_user.id, text="Ого, слово " + word + " есть в следующих словарях:",
                         reply_markup=keyboard)
        count = 0

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    cd = call.data.split(' ', maxsplit=1)
    i = int(cd[0])
    word = str(cd[1])
    url = dictionaries[i][0] + word[0] + '/' + word
    final_request = requests.get(url, headers=headers, timeout=5)
    html_doc = final_request.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    bot.send_message(call.message.chat.id, soup.p.get_text())


bot.polling(none_stop=True, interval=0)