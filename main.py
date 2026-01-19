import asyncio
import aiogram
import os
import json
from aiogram.types import CallbackQuery
from logger import logger
from handlers import router, start_daemon
from utils import daemon
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TEST_TOKEN")
CLBK = os.getenv("CALLBACK")
cb = CallbackQuery(**json.loads(CLBK))

async def start_bot():
    global launch_type

    """Один цикл жизни бота"""
    bot = aiogram.Bot(token=BOT_TOKEN)
    disp = aiogram.Dispatcher()
    disp.include_router(router)

    try:
        asyncio.create_task(start_daemon(callback=cb, bot=bot))
        await disp.start_polling(bot, polling_timeout=60)
    finally:
        await bot.session.close()

async def main():
    global launch_type

    """Главный перезапускающий цикл"""
    while True:
        try:
            logger.info("Бот запущен")
            await start_bot()
            launch_type = "handler"
        except Exception as e:
            logger.critical(f"Сбой в работе бота: {e}", exc_info=True)
            logger.info("Перезапускаю бота через 5 секунд…")
            await asyncio.sleep(5)
        else:
            # если polling завершился без исключения — выйти
            try:
                last_anns = {}
                with open("data.json", "r") as f:
                    data = json.load(f)
                last_anns = data['last_anns']
            except Exception as e: logger.error(e, exc_info=True)

            with open("data.json", "w") as f:
                data = {"launch_type": "autostart", "last_anns": last_anns}
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info("Бот остановлен вручную.")
            break

if __name__ == "__main__":
    asyncio.run(main())
