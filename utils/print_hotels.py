from loader import bot
from typing import Dict, Union
from telebot.types import InputMediaPhoto
from loader import logger
from datetime import date


def print_hotels(chatid: Union[int, str], hotels_info: Dict) -> None:
  try:
    for hotel in hotels_info.values():
      bot.send_message(chatid, '🔘')
      checkin_date = date(hotel['checkin']['year'], hotel['checkin']['month'], hotel['checkin']['day'])
      checkout_date = date(hotel['checkout']['year'], hotel['checkout']['month'], hotel['checkout']['day'])
      total = round((checkout_date - checkin_date).days * hotel['price'], 2)
      bot.send_message(chatid, \
       f"<a href='{hotel['url']}'>{hotel['name']}</a>\n{hotel['tag']}\n{hotel['address']}\nЦена за ночь: {hotel['price']}$\nСтоимость за период с {checkin_date.strftime('%d.%m.%Y')} по {checkout_date.strftime('%d.%m.%Y')}: {total}$\nРасстояние до центра города: {hotel['distance']}км", \
       parse_mode='html')
      if 'images' in hotel:
        medias = list()
        for i_image in hotel['images']:
          medias.append(InputMediaPhoto(i_image["image"]["url"], i_image["image"]["description"]))
        bot.send_media_group(chatid, medias)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chatid, f'Что-то пошло не так: {e}')