from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data.config import BOT_TOKEN
import logging

logger = logging.getLogger('EasyTravelBot')
bot = TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())
