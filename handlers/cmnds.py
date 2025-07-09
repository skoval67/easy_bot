from loader import bot, logger
from states.polls import HotelPrice
from telebot.types import Message, CallbackQuery, InlineKeyboardButton
from keyboards.inline.keybrds import generate_calendar_days, generate_calendar_months, keybrd_yesno, keybrd_specify_city
from keyboards.inline.filters import calendar_factory, calendar_zoom, calendar_date
from utils.rapidapi import get_regions_id, make_query
from utils.print_hotels import print_hotels
from datetime import date


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_price(message: Message) -> None:
  bot.set_state(message.from_user.id, HotelPrice.location, message.chat.id)
  with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    if message.text == '/bestdeal':
      data['sort_order'] = 'DISTANCE'
    else:
      data['sort_order'] = 'PRICE_LOW_TO_HIGH'
    if message.text == '/highprice':
      data['min_price'] = 1
      data['max_price'] = 1000000
    data['command'] = message.text
  bot.send_message(message.chat.id, f'Где будем искать? <i>[город]</i>', parse_mode='html')


@bot.message_handler(state = HotelPrice.location)
def get_location(message: Message) -> None:
  success, info = get_regions_id(message.text.lower())
  if len(info) == 0:
    success = False
    info = 'Город не найден'
  if success:
    if len(info) > 1:
      bot.send_message(message.chat.id, 'Уточните расположение', reply_markup = keybrd_specify_city(info))
      return
  else:
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, f'Что-то пошло не так: {info}')
    return
  with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    data['region_id'] = info[0][0]
  bot.set_state(message.from_user.id, HotelPrice.checkin_date, message.chat.id)
  now = date.today()
  bot.send_message(message.chat.id, 'Дата заезда', reply_markup = generate_calendar_days(year=now.year, month=now.month))


@bot.message_handler(state = HotelPrice.hotels_count)
def hotels_count(message: Message) -> None:
  try:
    if int(message.text) <= 0:
      raise ValueError('Так мало??')
  except Exception as e:
    logger.exception(e)
    bot.reply_to(message, f'Здесь какая-то ошибка: {str(e)}\nСколько отелей показать?')
    return
  with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    data['hotels_count'] = int(message.text)
  bot.send_message(message.chat.id, 'Показывать фотографии отелей?', reply_markup = keybrd_yesno)


@bot.message_handler(state = HotelPrice.photo_count)
def photo_count(message: Message) -> None:
  try:
    if int(message.text) <= 0:
      raise ValueError('Так мало??')
  except Exception as e:
    logger.exception(e)
    bot.reply_to(message, f'Здесь какая-то ошибка: {str(e)}\nСколько вывести фотографий <i>[не больше 10]</i>?', parse_mode = 'html')
    return
  with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    data['photo_count'] = min(10, int(message.text))
    bot.send_message(message.chat.id, 'Делаю запрос. Ждите...')
    success, info = make_query(data)
    if success:
      print_hotels(message.chat.id, info)
    else:
      bot.send_message(message.chat.id, f'Что-то пошло не так: {info}')
  bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state = HotelPrice.price_range)
def get_price_range(message: Message) -> None:
  try:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
      data['min_price'], data['max_price'] = map(float, message.text.split('-'))
      if data['min_price'] < 1:
        data['min_price'] = 1       # поиск по цене меньше 1 вызывает ошибку
    bot.set_state(message.from_user.id, HotelPrice.distance_range, message.chat.id)
    bot.send_message(message.chat.id, 'Укажите диапазон расстояний в км: <i>min - max</i>', parse_mode='html')
  except Exception as e:
    logger.exception(e)
    bot.reply_to(message, f'Здесь какая-то ошибка: {str(e)}\nУкажите диапазон цен: <i>min - max</i>', parse_mode='html')


@bot.message_handler(state = HotelPrice.distance_range)
def get_dustance_range(message: Message) -> None:
  try:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
      data['min_distance'], data['max_distance'] = map(lambda x: float(x)/1.60934, message.text.split('-'))   # пределы расстояний сразу преобразовываем в мили
    bot.set_state(message.from_user.id, HotelPrice.hotels_count, message.chat.id)
    bot.send_message(message.chat.id, 'Сколько отелей показать?')
  except Exception as e:
    logger.exception(e)
    bot.reply_to(message, f'Здесь какая-то ошибка: {str(e)}\nУкажите диапазон расстояний в км: <i>min - max</i>', parse_mode='html')