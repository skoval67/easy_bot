from telebot.types import Message

from loader import bot
#import debugpy

# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    #debugpy.breakpoint()
    bot.reply_to(message, "Я тебя не понимаю. Набери /help")
