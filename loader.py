from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
import logging

logger = logging.getLogger('EasyTravelBot')
f_handler = logging.FileHandler('mybot.log')
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
logger.warning('This is a warning')
logger.error('This is an error')

bot = TeleBot(token=config.BOT_TOKEN, state_storage=StateMemoryStorage())
