from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Start daemon", callback_data="start_daemon")]
    ]
)
