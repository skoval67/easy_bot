from loader import bot, logger
from states.polls import HotelPrice
from telebot.types import Message
from keyboards.inline.keybrd_yesno import keybrd_yesno
from utils.rapidapi import make_query
from utils.print_hotels import print_hotels

@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
  bot.set_state(message.from_user.id, HotelPrice.location, message.chat.id)
  with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    data['sort_order'] = 'PRICE_LOW_TO_HIGH'
  bot.send_message(message.chat.id, f'Где будем искать? <i>[город]</i>', parse_mode='html')


@bot.message_handler(state = HotelPrice.location)
def get_location(message: Message) -> None:
  with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    data['location'] = message.text.lower()
  bot.set_state(message.from_user.id, HotelPrice.hotels_count, message.chat.id)
  bot.send_message(message.chat.id, 'Сколько отелей показать?')


@bot.message_handler(state = HotelPrice.hotels_count)
def hotels_count(message: Message) -> None:
  try:
    if int(message.text) <= 0:
      raise ValueError('Так мало??')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
      data['hotels_count'] = int(message.text)
    bot.send_message(message.chat.id, 'Показывать фотографии отелей?', reply_markup = keybrd_yesno)
  except Exception as e:
    bot.reply_to(message, f'Здесь какая-то ошибка: {str(e)}\nСколько отелей показать?')
    logger.error(f'{str(e)}')


@bot.message_handler(state = HotelPrice.photo_count)
def photo_count(message: Message) -> None:
  try:
    if int(message.text) <= 0:
      raise ValueError('Так мало??')
  except Exception as e:
    bot.reply_to(message, f'Здесь какая-то ошибка: {str(e)}\nСколько вывести фотографий <i>[не больше 10]</i>?', parse_mode = 'html')
    return
  with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    data['photo_count'] = int(message.text)
    bot.send_message(message.chat.id, f'Делаю запрос. Ждите...')
    success, info = make_query(data)
  bot.delete_state(message.from_user.id, message.chat.id)
  if success:
    print_hotels(message.chat.id, info)
  else:
    bot.send_message(message.chat.id, f'Что-то пошло не так: {info}')