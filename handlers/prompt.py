from loader import bot
from states.polls import Prompt
from telebot.types import Message
from utils.openaiapi import bot_asks_ai
import debugpy


@bot.message_handler(commands=['prompt'])
def prompt(message: Message) -> None:
  debugpy.breakpoint()
  bot.set_state(message.from_user.id, Prompt.question, message.chat.id)
  bot.send_message(message.chat.id, f'Вопрос к <strong>ИИ</strong>', parse_mode='html')

@bot.message_handler(state = Prompt.question)
def ask_ai(message: Message) -> None:
  debugpy.breakpoint()
  bot.delete_state(message.from_user.id, message.chat.id)
  answer = bot_asks_ai(message.text)
  bot.send_message(message.chat.id, answer)