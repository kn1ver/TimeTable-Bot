from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from logger import logger, set_logger
from utils import daemon, last_anns
import keyboards as markup

router = Router()
topic = None
working = False
daemon_logger = set_logger("logs/daemon.log", True)

@router.message(Command("start"))
async def start(message: Message, bot: Bot):
    try:
        await message.answer(
            text="Привет!",
            parse_mode="HTML",
            reply_markup=markup.start
        )
        # for some in message:
        #     logger.debug(some)
        topic = message.message_thread_id
 
    except Exception as e: logger.error(e, exc_info=True)

@router.callback_query(lambda c: "start_daemon" in c.data)
async def start_daemon(clbk: CallbackQuery):
    working = True
    while working:
        await daemon(clbk, daemon_logger)

@router.callback_query(lambda c: "get_last_file" in c.data)
async def send_last_file(message: Message):
    pass
