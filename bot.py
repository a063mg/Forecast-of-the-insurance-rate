from callback_handler import *

@bot.message_handler(commands=['start'])
def start_bot(message):
    delete_table()
    start_greeting(message.chat.id)


bot.infinity_polling()
