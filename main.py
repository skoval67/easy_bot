from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from keyboards.inline.filters import bind_filters

if __name__ == '__main__':
  bot.add_custom_filter(StateFilter(bot))
  bind_filters(bot)
  set_default_commands(bot)
  bot.infinity_polling()