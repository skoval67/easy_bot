import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "запуск бота"),
    ('help', "эта справка"),
    ('lowprice', "топ самых дешёвых отелей в городе"),
    ('highprice', "топ самых дорогих отелей в городе"),
    ('bestdeal', "топ отелей, наиболее подходящих по цене и расположению от центра"),
    ('history', "вывод истории поиска отелей")
)
