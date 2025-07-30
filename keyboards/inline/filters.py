import telebot
from telebot import types, AdvancedCustomFilter, TeleBot
from telebot.callback_data import CallbackData, CallbackDataFilter

calendar_date = CallbackData("year", "month", "day", prefix="calendar_date")
calendar_factory = CallbackData("year", "month", prefix="calendar")
calendar_zoom = CallbackData("year", prefix="calendar_zoom")
city = CallbackData("city", prefix="city")


class CalendarCallbackFilter(AdvancedCustomFilter):
    key = 'calendar_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class CalendarZoomCallbackFilter(AdvancedCustomFilter):
    key = 'calendar_zoom_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class CalendarDateCallbackFilter(AdvancedCustomFilter):
    key = 'calendar_date_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)

class CityCallbackFilter(AdvancedCustomFilter):
    key = 'city_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)

def bind_filters(bot: TeleBot):
    bot.add_custom_filter(CalendarCallbackFilter())
    bot.add_custom_filter(CalendarZoomCallbackFilter())
    bot.add_custom_filter(CalendarDateCallbackFilter())
    bot.add_custom_filter(CityCallbackFilter())