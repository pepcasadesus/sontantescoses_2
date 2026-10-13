import telebot
from telebot import custom_filters
import random

#bot = telebot.TeleBot('8911193196:AAE-YhDr7t1WMcbEXuXr8tDIYXIHVVzmbXg')
bot = telebot.TeleBot('8985714346:AAHTo1qAbc2o9ISoUphL_PdLs-CJJT-nTRw')

@bot.message_handler(commands=['medeix'])
def enviar_dades(message):
    temperatura = random.randrange(20,30)
    humitat = random.randrange(50,70)
    bot.send_message(message.chat.id, f'T={temperatura} H={humitat}')
    

bot.add_custom_filter(custom_filters.ChatFilter())
bot.polling(none_stop=True)
