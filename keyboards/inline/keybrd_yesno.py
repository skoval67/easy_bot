from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

keybrd_yesno = InlineKeyboardMarkup(row_width = 2).add(InlineKeyboardButton("Да", callback_data="cb_yes"), InlineKeyboardButton("Нет", callback_data="cb_no"))
