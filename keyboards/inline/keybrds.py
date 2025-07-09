import calendar
from typing import List
from datetime import date, timedelta
import locale
from keyboards.inline.filters import calendar_factory, calendar_zoom, calendar_date, city
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

locale.setlocale(locale.LC_ALL, 'ru_RU')
EMTPY_FIELD = '1'
WEEK_DAYS = [calendar.day_abbr[i] for i in range(7)]
MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]


keybrd_yesno = InlineKeyboardMarkup(row_width = 2).add(InlineKeyboardButton("Да", callback_data="cb_yes"), InlineKeyboardButton("Нет", callback_data="cb_no"))

def keybrd_specify_city(cities: List) -> InlineKeyboardMarkup:
  keyboard = InlineKeyboardMarkup(row_width = 2)
  for loc in cities:
    keyboard.add(InlineKeyboardButton(text=loc[1], callback_data=city.new(loc[0])))

  return keyboard

def generate_calendar_days(year: int, month: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=7)
    today = date.today()

    keyboard.add(
        InlineKeyboardButton(
            text=date(year=year, month=month, day=1).strftime('%b %Y'),
            callback_data=EMTPY_FIELD
        )
    )
    keyboard.add(*[
        InlineKeyboardButton(
            text=day,
            callback_data=EMTPY_FIELD
        )
        for day in WEEK_DAYS
    ])

    for week in calendar.Calendar().monthdayscalendar(year=year, month=month):
        week_buttons = []
        for day in week:
            day_name = ' '
            if day == today.day and today.year == year and today.month == month:
                day_name = '🔘'
            elif day != 0:
                day_name = str(day)
            week_buttons.append(
                InlineKeyboardButton(
                    text=day_name,
                    callback_data=calendar_date.new(year=year, month=month, day=day)
                )
            )
        keyboard.add(*week_buttons)

    previous_date = date(year=year, month=month, day=1) - timedelta(days=1)
    next_date = date(year=year, month=month, day=1) + timedelta(days=31)

    keyboard.add(
        InlineKeyboardButton(
            text='<< месяц',
            callback_data=calendar_factory.new(year=previous_date.year, month=previous_date.month)
        ),
        InlineKeyboardButton(
            text='по годам',
            callback_data=calendar_zoom.new(year=year)
        ),
        InlineKeyboardButton(
            text='месяц >>',
            callback_data=calendar_factory.new(year=next_date.year, month=next_date.month)
        ),
    )

    return keyboard


def generate_calendar_months(year: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(
            text=date(year=year, month=1, day=1).strftime('Год %Y'),
            callback_data=EMTPY_FIELD
        )
    )
    keyboard.add(*[
        InlineKeyboardButton(
            text=month,
            callback_data=calendar_factory.new(year=year, month=month_number)
        )
        for month_number, month in MONTHS
    ])
    keyboard.add(
        InlineKeyboardButton(
            text='<< год',
            callback_data=calendar_zoom.new(year=year - 1)
        ),
        InlineKeyboardButton(
            text='год >>',
            callback_data=calendar_zoom.new(year=year + 1)
        )
    )
    return keyboard
