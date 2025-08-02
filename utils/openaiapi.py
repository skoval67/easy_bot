from functools import wraps
from time import sleep
from loader import logger
from openai import OpenAI
from config_data import config


client = OpenAI(api_key=config.OPENAI_API_KEY)

def retry(exception, max_tries=None):
  """
  Декоратор для обработки ошибок сервера
  """
  def wrap_fun(func):

    def expo(base=2, factor=1, max_value=None):
      n = -4
      while True:
        a = factor * base ** n
        if max_value is None or a < max_value:
          yield a
          n += 1
        else:
          yield max_value

    @wraps(func)
    def wrapped_func(*args, **kwargs):
      tries = 0
      interval = expo()
      while True:
        try:
          tries += 1
          ret = func(*args, **kwargs)
        except exception as e:
          logger.exception(e)
          if max_tries is not None and tries == max_tries:
            raise
          sleep(next(interval))
        else:
          return ret

    return wrapped_func

  return wrap_fun

#@retry(Exception)
def bot_asks_ai(text):
  response = client.responses.create(
    model="gpt-4.1",
    input="what time is it now"
  )
  return response.output_text
