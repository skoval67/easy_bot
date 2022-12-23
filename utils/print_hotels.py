from loader import bot
from typing import Dict
from telebot.types import InputMediaPhoto
from loader import logger


def print_hotels(chatid, hotels_info: Dict) -> None:
  try:
    for hotel in hotels_info.values():
      bot.send_message(chatid, \
       f"<a href='{hotel['url']}'>{hotel['name']}</a>\n{hotel['tag']}\n{hotel['address']}\nЦена: {hotel['price']}$\nРасстояние до центра города: {hotel['distance']}км", \
       parse_mode='html')
      if 'images' in hotel:
        medias = list()
        for i_image in hotel['images']:
          medias.append(InputMediaPhoto(i_image["image"]["url"], i_image["image"]["description"]))
        bot.send_media_group(chatid, medias)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chatid, f'Что-то пошло не так: {e}')