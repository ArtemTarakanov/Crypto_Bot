#python -m venv venv   
#venv\scripts\activate
#pip3 install pytelegrambotapi
#pip3 install requests 

import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Для начала введи пожалуйста всё в таком формате:\n <имя валюты>, <в какую валюту перевести>, <количество переводимой валюты>\n \
Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values)!=3:
            raise ConvertionException('Слишком много параметров, я же говорил, надо 3(')
    
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        total_base = float(total_base)
        amount = float(amount)
        text = f"Цена {amount} {quote} в {base} составляет {amount*total_base}"
        bot.send_message(message.chat.id, text)
        
bot.remove_webhook()
bot.polling(none_stop=True)
