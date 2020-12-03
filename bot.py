import logging
import ephem
import settings
from datetime import datetime

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

user_list_sity = {}
def read_txt():
    list_sity = []
    with open("cities.txt", 'r', encoding="utf-8") as cities:
        for city in cities:
            list_sity.append(city.replace('\n', ''))
    return list_sity

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
    update.message.reply_text(user_text)


def wordcount(update, context):
    try:
        user_text = update.message.text.split()
        count_word = len(user_text) - 1
        # тут считаются всё и предлоги тоже относятся к словам
        if count_word == 0:
            text = f"Нечего считать"
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


def cities_game(update, context):
    user_text = update.message.text.split()[-1]
    user_city = user_text.capitalize()
    user_chat = update.message.chat_id
    text = engine_game(user_city, user_chat)
    update.message.reply_text(text)


def engine_game(city, chat_id):
    last_letter = city[-1]

    if user_list_sity.get(chat_id) is None:
        user_list_sity[chat_id] = read_txt()
        cities = user_list_sity.get(chat_id)

    else:
        cities = user_list_sity.get(chat_id)

    if city in cities:

        cities.remove(city)
        user_list_sity[chat_id] = cities
        length = len(cities)
        count = 0

        for index in cities:

            if last_letter == index[0].lower():
                cities.remove(index)
                user_list_sity[chat_id] = cities
                return f"{index}, ваш ход."

            else:
                count += 1

        if count >= length:
            return f"Я больше не знаю городов на букву {last_letter}. Ты победил!"

    else:            
        return f"Такой город уже был. Ты проиграл."


# def calculator(string):
#     string = string.replace(" ", "")
#     try:

#         if len(string.split("+")) == 2:
#             parts = string.split("+")
#             return sum(map(float, parts))

#         if len(string.split('-')) == 2:
#             parts = string.split("-")
#             return float(parts[0]) - float(parts[-1])

#         if len(string.split('*')) == 2:
#             parts = string.split("*")
#             return float(parts[0]) * float(parts[1])

#         if len(string.split('/')) == 2:
#             parts = string.split("/")
#             return float(parts[0]) / float(parts[1])

#     except ValueError:
#         return "Вводи пожалуйста числа!"

#     except ZeroDivisionError:
#         return "На 0 делить нельзя!"


def calculator(string):
    try:
        string = string.replace(" ", "")
        parts = string.split("+")

        for index_part in range(len(parts)):
            if "-" in parts[index_part]:
                parts[index_part] = parts[index_part].split("-")

        for index_part in range(len(parts)):
            parts[index_part] = precalc(parts[index_part])
        return sum(parts)

    except ValueError:
        return "Вводи пожалуйста числа!"

    except ZeroDivisionError:
        return "На 0 делить нельзя!"


def precalc(part):
    if type(part) is str:

        if "*" in part:
            parts = list(map(precalc, part.split("*")))
            result = 1
            for subpart in parts:
                result *= subpart

            return result

        elif "/" in part:
            parts = list(map(precalc, part.split("/")))
            result = parts[0]

            for subpart in parts[1:]:
                result /= subpart

            return result

        else:
            return float(part)

    elif type(part) is list:

        for index_part in range(len(part)):
            part[index_part] = precalc(part[index_part])
        
        return part[0] - sum(part[1:])

    return part


def calc(update, context):
    user_text = update.message.text
    expression = str(user_text.replace("/calc ", ''))
    # print(calculator("3/2 +(10-5+2) / 3*2.5- 4+1/2"))
    text = calculator(expression)
    update.message.reply_text(text)


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
