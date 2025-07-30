from telebot.handler_backends import State, StatesGroup

class HotelPrice(StatesGroup):
  location = State()        # местность для поиска отелей
  checkin_date = State()    # дата заезда
  checkout_date = State()   # дата выезда
  price_range = State()     # диапазон цен
  distance_range = State()  # диапазон расстояний
  hotels_count = State()    # количество отелей для вывода за один поиск
  show_photo = State()      # включать фотографии в результат поиска?
  photo_count = State()     # если включать, то сколько

class Prompt(StatesGroup):
  question = State()        # Текст запроса к ИИ
