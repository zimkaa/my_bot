"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging
import ephem
import settings
from datetime import datetime
# from city import list_sity

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}

list_sity = []
with open("cities.txt", 'r', encoding="utf-8") as cities:
    for city in cities:
        list_sity.append(city.replace('\n', ''))


def greet_user(update, context):
    text = 'Вызван /start'
    update.message.reply_text(text)


def mars(update, context):
    try:
        user_text = update.message.text.split()[-1]
        planet = getattr(ephem, user_text.capitalize())
        text = f"Сегодня {user_text} в созвездии {ephem.constellation(planet(ephem.now()))[1]}"
        update.message.reply_text(text)
    except AttributeError:
        text = f"Я не знаю такую планету {user_text.capitalize()}.\nПопробуй ввести другую"
        update.message.reply_text(text)


def talk_to_me(update, context):
    user_text = update.message.text
    # print(user_text)
    update.message.reply_text(user_text)


def wordcount(update, context):
    try:
        user_text = update.message.text.split()
        count_word = len(user_text) - 1
        # тут считаются всё и придлоги тоже относятся к словам
        # так же нужно вводить пробел после команды /wordcount
        if count_word == 0:
            text = f"нечего считать"
            update.message.reply_text(text)
        else:
            text = f"{count_word} слов(а)"
            update.message.reply_text(text)
    except:
        text = f"Что-то пошло не так"
        update.message.reply_text(text)


def next_full_moon(update, context):
    user_text = update.message.text.split()
    date = user_text[-1]
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
        full_moon = ephem.next_full_moon(date)
        text = f"Следующее полнолуние {full_moon}"
        update.message.reply_text(text)
    except ValueError:
        text = f"Что-то не то ввел. Вводи дату в формате гггг-мм-дд пример: \"2019-01-01\""
        update.message.reply_text(text)

# осталось доработать многопользовательский режим
def cities_game(update, context):
    user_text = update.message.text.split()[-1]
    # print(update.message.username)
    user_city = user_text.capitalize()
    last_letter = user_city[-1]
    if user_city in list_sity:
        list_sity.remove(user_city)
        length = len(list_sity)
        count = 0
        for index in list_sity:
            if last_letter == index[0].lower():
                update.message.reply_text(f"{index}, ваш ход.")
                list_sity.remove(index)
                break
            else:
                count += 1
        if count >= length:
            update.message.reply_text(f"Я больше не знаю городов на букву {last_letter}. Ты победил!")
    else:            
        update.message.reply_text(f"Такой город уже был. Ты проиграл.")


def calculation(value1, value2, operation):
    string = str(value1 + operation + value2)
    return string

def calc(update, context):
    user_text = update.message.text
    expression = user_text.replace("/calc ", '')
    minus = '-'
    values = expression.split(minus)
    if len(expression.split(minus)) == 2:
        val1 = float(values[0])
        val2 = float(values[-1])
        text = val1 - val2
        update.message.reply_text(text)
        print(calculation(val1, val2, minus))
    elif len(expression.split('+')) == 2:
        pass
    elif len(expression.split('*')) == 2:
        pass
    elif len(expression.split('/')) == 2:
        pass
    else:
        update.message.reply_text(f"Что-то пошло не так")


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", mars))

    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    
    dp.add_handler(CommandHandler("cities", cities_game))
    dp.add_handler(CommandHandler("calc", calc))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал!")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
