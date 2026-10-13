import telebot
from telebot import custom_filters
import threading
import random
import time

#TOKEN = '8911193196:AAE-YhDr7t1WMcbEXuXr8tDIYXIHVVzmbXg'
TOKEN = '8985714346:AAHTo1qAbc2o9ISoUphL_PdLs-CJJT-nTRw'
bot = telebot.TeleBot(TOKEN)

temperatura = 0
humitat = 0

aturar = threading.Event()


# FIL 1: Simula el sensor DHT11
def sensor():
    global temperatura, humitat

    while not aturar.is_set():
        temperatura = random.randrange(20, 30)
        humitat = random.randrange(50, 70)

        time.sleep(2)


# FIL 2: Bot de Telegram
@bot.message_handler(commands=['start'])
def enviar_dades(message):
    bot.send_message(message.chat.id, f'T={temperatura} H={humitat}')


def telegram():
    bot.add_custom_filter(custom_filters.ChatFilter())
    bot.polling(none_stop=True)


# Crear els fils
fil_sensor = threading.Thread(target=sensor)
fil_telegram = threading.Thread(target=telegram)

# Iniciar els fils
fil_sensor.start()
fil_telegram.start()


try:
    while not aturar.is_set():
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Aturant programa...")
    aturar.set()
    bot.stop_polling()

    fil_sensor.join()
    fil_telegram.join()

    print("Programa finalitzat")
