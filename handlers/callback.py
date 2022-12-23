from loader import bot
from states.polls import HotelPrice
from telebot.types import Message
from utils.rapidapi import make_query
from utils.print_hotels import print_hotels

@bot.callback_query_handler(func=lambda call: call.data == "cb_yes")
def callback_query(call):
  bot.answer_callback_query(call.id, "Answer is Yes")
  with bot.retrieve_data(call.from_user.id) as data:
    data['show_photo'] = True
  bot.set_state(call.from_user.id, HotelPrice.photo_count)
  bot.send_message(call.from_user.id, 'Сколько вывести фотографий <i>[не больше 10]</i>?', parse_mode = 'html')


@bot.callback_query_handler(func=lambda call: call.data == "cb_no")
def callback_query(call):
  bot.answer_callback_query(call.id, "Answer is No")
  with bot.retrieve_data(call.from_user.id) as data:
    data['show_photo'] = False
    bot.send_message(call.from_user.id, f'Делаю запрос. Ждите...')
    success, info = make_query(data)
  bot.delete_state(call.from_user.id)
  if success:
    print_hotels(call.from_user.id, info)
  else:
    bot.send_message(call.from_user.id, f'Что-то пошло не так: {info}')