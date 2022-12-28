from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data.config import BOT_TOKEN
import logging

logger = logging.getLogger('EasyTravelBot')
f_handler = logging.FileHandler('mybot.log')
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter(fmt='%(asctime)s,%(levelname)s,%(message)s', datefmt='%d.%m.%Y %H:%M:%S')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

bot = TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())
