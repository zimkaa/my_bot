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


def greet_user(update, context):
    text = 'Вызван /start'
    # print(text)
    update.message.reply_text(text)


def mars(update, context):
    # print("text ", user_text)

    try:
        user_text = update.message.text.split()[-1].lower()
        planet = getattr(ephem, user_text.capitalize())
        text = f"Сегодня {user_text} в созвездии {ephem.constellation(planet(ephem.now()))[1]}"
        update.message.reply_text(text)
    except:
        text = f"Я не знаю такую планету {user_text.capitalize()}.\nПопробуй ввести другую"
        update.message.reply_text(text)

    # if user_text == "mars":
    #     # data = ephem.Mars(ephem.now())
    #     data = getattr(ephem, "Mars")
    #     text = f"Сегодня в созвездии {ephem.constellation(data(ephem.now()))[1]}"      
    #     update.message.reply_text(text)
    # elif user_text == "jupiter":
    #     # data = ephem.Jupiter(ephem.now())
    #     data = getattr(ephem, "Jupiter")
    #     text = f"Сегодня в созвездии {ephem.constellation(data(ephem.now()))[1]}"
    #     update.message.reply_text(text)
    # else:
    #     text = "У меня нет данных о данной планете. Попробуй mars или Jupiter"
    #     update.message.reply_text(text)
    

def wordcount(update, context):
    # print("text ", user_text)
    try:
        user_text = update.message.text.split()
        count_word = len(user_text) - 1
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
    if len(user_text) > 2:
        text = f"Что-то не то ввел. Води дату в таком виде \"2019-01-01\" "
        update.message.reply_text(text)
    elif len(user_text) == 0:
        text = f"Что-то пошло не так"
        update.message.reply_text(text)
    else:
        full_moon = ephem.next_full_moon(date)
        text = f"Следующее полнолуние {full_moon}"
        update.message.reply_text(text)


def talk_to_me(update, context):
    user_text = update.message.text
    # print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", mars))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
