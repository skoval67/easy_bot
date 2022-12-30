from loader import bot, logger
from typing import Dict, Union
from telebot.types import InputMediaPhoto
from datetime import date
from telebot.apihelper import ApiTelegramException
from functools import wraps
from time import sleep
from database.core import History


def retry(exception, max_tries=None):
  """
  Декоратор для обработки ошибки: A request to the Telegram API was unsuccessful. Error code: 429.
  """
  def wrap_fun(func):

    @wraps(func)
    def wrapped_func(*args, **kwargs):
      tries = 0
      while True:
        try:
          tries += 1
          ret = func(*args, **kwargs)
        except exception as e:
          if max_tries is not None and tries == max_tries:
            raise
          seconds = int(e.result.headers._store['retry-after'][1])
          sleep(seconds)
        else:
          return ret

    return wrapped_func

  return wrap_fun


@retry(ApiTelegramException)
def send_message(id, *args, **kwargs):
  bot.send_message(id, *args, **kwargs)

@retry(ApiTelegramException)
def send_media(chatid, medias):
  bot.send_media_group(chatid, medias)


def print_hotels(chatid: Union[int, str], hotels_info: Dict) -> None:
  try:
    for id, hotel in hotels_info.items():
      send_message(chatid, '🔘')
      checkin_date = date(hotel['checkin']['year'], hotel['checkin']['month'], hotel['checkin']['day'])
      checkout_date = date(hotel['checkout']['year'], hotel['checkout']['month'], hotel['checkout']['day'])
      total = round((checkout_date - checkin_date).days * hotel['price'], 2)
      send_message(chatid, \
        str(f"<a href='https://www.hotels.com/h{id}.Hotel-Information' hreflang='EN'>{hotel['name']}</a>\n"
           f"{hotel['tag']}\n{hotel['address']}\nЦена за ночь: {hotel['price']}$\n"
           f"Стоимость за период с {checkin_date.strftime('%d.%m.%Y')} по {checkout_date.strftime('%d.%m.%Y')}: {total}$\n"
           f"Расстояние до центра города: {hotel['distance']}км"), \
       parse_mode='html', disable_web_page_preview=True)
      if 'images' in hotel:
        medias = list()
        for i_image in hotel['images']:
          medias.append(InputMediaPhoto(i_image["image"]["url"], i_image["image"]["description"]))
        send_media(chatid, medias)
    with bot.retrieve_data(chatid) as data:
      # ишем историю в базу данных
      History(user_id=chatid, command=data['command'], hotels=hotels_info).save()
  except Exception as e:
    logger.exception(e)
    bot.send_message(chatid, f'Что-то пошло не так: {e}')