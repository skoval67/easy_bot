from loader import bot
from telebot.types import Message
from database.core import History


@bot.message_handler(commands=['history'])
def get_history(message: Message) -> None:
  history = ''
  for record in History.select().where(History.user_id == message.from_user.id):
    history += f"{record.created_at.strftime('%d.%m.%Y %H:%M:%S')}, {record.command}, найденные отели:\n\n<i>"
    for hotel in record.hotels.values():
      history += f"{hotel['name']}, {hotel['address']}\n"
    history += "</i>\n"
  if history == '':
    history = 'Ничего нет'
  bot.send_message(message.chat.id, history, parse_mode = 'html')
