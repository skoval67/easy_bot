from loader import bot
from states.polls import HotelPrice
from telebot.types import Message, CallbackQuery
from utils.rapidapi import make_query
from utils.print_hotels import print_hotels
from keyboards.inline.keybrds import generate_calendar_days, generate_calendar_months
from keyboards.inline.filters import calendar_factory, calendar_zoom, calendar_date, city
from datetime import date


@bot.callback_query_handler(func=lambda call: call.data == "cb_yes")
def callback_query(call: CallbackQuery):
  with bot.retrieve_data(call.from_user.id) as data:
    data['show_photo'] = True
  bot.set_state(call.from_user.id, HotelPrice.photo_count)
  bot.send_message(call.from_user.id, 'Сколько вывести фотографий <i>[не больше 10]</i>?', parse_mode = 'html')


@bot.callback_query_handler(func=lambda call: call.data == "cb_no")
def callback_query(call: CallbackQuery):
  with bot.retrieve_data(call.from_user.id) as data:
    data['show_photo'] = False
    bot.send_message(call.from_user.id, 'Делаю поиск. Ждите...')
    success, info = make_query(data)
  if success:
    print_hotels(call.from_user.id, info)
  else:
    bot.send_message(call.from_user.id, f'Что-то пошло не так: {info}')
  bot.delete_state(call.from_user.id)


@bot.callback_query_handler(func=None, calendar_config=calendar_factory.filter())
def calendar_action_handler(call: CallbackQuery):
  callback_data: dict = calendar_factory.parse(callback_data=call.data)
  year, month = int(callback_data['year']), int(callback_data['month'])
  bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=generate_calendar_days(year=year, month=month))


@bot.callback_query_handler(func=None, calendar_zoom_config=calendar_zoom.filter())
def calendar_zoom_out_handler(call: CallbackQuery):
  callback_data: dict = calendar_zoom.parse(callback_data=call.data)
  year = int(callback_data.get('year'))
  bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=generate_calendar_months(year=year))


@bot.callback_query_handler(func=None, calendar_date_config=calendar_date.filter())
def calendar_date_handler(call: CallbackQuery):
  callback_data: dict = calendar_date.parse(callback_data=call.data)
  del callback_data['@']
  if bot.get_state(call.from_user.id) == HotelPrice.checkin_date.name:
    with bot.retrieve_data(call.from_user.id) as data:
      data['checkin'] = {k:int(v) for k, v in callback_data.items()}
    bot.set_state(call.from_user.id, HotelPrice.checkout_date)
    now = date.today()
    bot.send_message(call.from_user.id, 'Дата выезда', reply_markup = generate_calendar_days(year=now.year, month=now.month))
  else:
    with bot.retrieve_data(call.from_user.id) as data:
      data['checkout'] = {k:int(v) for k, v in callback_data.items()}
      checkin_date = date(data['checkin']['year'], data['checkin']['month'], data['checkin']['day'])
      checkout_date = date(data['checkout']['year'], data['checkout']['month'], data['checkout']['day'])
    if checkin_date < checkout_date:
      if data['command'] == '/bestdeal':
        bot.set_state(call.from_user.id, HotelPrice.price_range)
        bot.send_message(call.from_user.id, 'Укажите диапазон цен: <i>min - max</i>', parse_mode='html')
      else:
        bot.set_state(call.from_user.id, HotelPrice.hotels_count)
        bot.send_message(call.from_user.id, 'Сколько отелей показать?')
    else:
      bot.delete_state(call.from_user.id)
      bot.send_message(call.from_user.id, 'Дата выезда должна быть больше даты заезда')


@bot.callback_query_handler(func=None, city_config=city.filter())
def city_handler(call: CallbackQuery):
  callback_data: dict = city.parse(callback_data=call.data)
  with bot.retrieve_data(call.from_user.id) as data:
    data['region_id'] = callback_data['city']
    bot.set_state(call.from_user.id, HotelPrice.checkin_date)
    now = date.today()
    bot.send_message(call.from_user.id, 'Дата заезда', reply_markup = generate_calendar_days(year=now.year, month=now.month))
