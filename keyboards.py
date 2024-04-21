from aiogram.filters import command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Callbacks.callback import MyCallback

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад")
        ]
    ], resize_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    one_time_keyboard=False
)

main_builder = InlineKeyboardBuilder()
main_builder.button(
    text="Рассчитать🧮",
    callback_data=MyCallback(foo="calculate", bar="42")  # Value can be not packed to string inplace, because builder knows what to do with callback instance
)
main_builder.button(
    text="Помощь📜",
    callback_data=MyCallback(foo="help", bar="42")  # Value can be not packed to string inplace, because builder knows what to do with callback instance
)
