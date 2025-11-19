from datetime import datetime, timedelta, date, time
from dotenv import load_dotenv
from logger import logger
from aiogram import Bot
from aiogram.types import CallbackQuery, FSInputFile

import os
import json
import base64
import asyncio
import aiohttp
import requests
import pathlib

BASE_DIR = pathlib.Path(__file__).parent

load_dotenv()
URL = os.getenv("URL")
API_TOKEN = os.getenv("API_TOKEN")

logger_default = logger
last_anns = {}

def save_bytes_to_file(data: bytes, path: str):
    # создаём директорию, если её нет
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # сохраняем
    with open(path, "wb") as f:
        f.write(data)

async def get_announcements():
    async with aiohttp.ClientSession() as s:
        headers = {"X-API-Token": API_TOKEN}
        async with s.get(f"{URL}/announcements", headers=headers) as r:
            r.raise_for_status()
            result = await r.json()
            logger.debug(result)
            return result

async def download_file():
    async with aiohttp.ClientSession() as s:
        headers = {"X-API-Token": API_TOKEN}
        async with s.post(f"{URL}/attachment", headers=headers) as r:
            r.raise_for_status()
            json_data = await r.json()

            return json_data


async def post_timetable(file_name: str, callback: CallbackQuery):
    logger.debug(f"Отправляю файл {file_name}")
    file = FSInputFile(f"files/{file_name}")
    await callback.message.answer_document(file)

async def daemon(callback: CallbackQuery, logger=logger_default):
    chat_id = callback.message.chat.id
    long_sleep = False
    try: last_anns[chat_id]
    except KeyError: last_anns[chat_id] = ""
    now = datetime.now().replace(microsecond=0)
    day = datetime.combine(date.today() + timedelta(1), time(0, 0, 0))

    # задаем промежутки времени работы: 6:00-8:00 и 14:00-21:00
    dt_1 = [datetime.combine(date.today(), time(14, 0, 0)), datetime.combine(date.today(), time(21, 0, 0))]
    dt_2 = [datetime.combine(date.today(), time( 6, 0, 0)), datetime.combine(date.today(), time( 8, 0, 0))]
    
    # проверяем находится ли время сейчас в одном из промежутков
    if dt_1[0] < now < dt_1[1] or dt_2[0] < now < dt_2[1]:
        # если да - опрашиваем api на наличие нового объявления с файлом
        logger.info("Опрашиваю API...")
        last_ann = await get_announcements()

        if last_ann[list(last_ann)[0]]['id'] != last_anns[chat_id]:
            last_anns[chat_id] = last_ann[list(last_ann)[0]]['id']

            json_data = await download_file()
            file_bytes = base64.b64decode(json_data['data'])
            save_bytes_to_file(file_bytes, str(BASE_DIR / "files" / json_data['name']))

            await post_timetable(json_data['name'], callback)
            long_sleep = True
        else:
            long_sleep = False
            logger.info("Засыпаю на 300 секунд")
            await asyncio.sleep(300)

    else:
        # если нет - засыпаем на время равное времени до ближайшего промежутка работы
        long_sleep = True

    if long_sleep:
        sleep_time = day - now + timedelta(hours=6) if now > dt_1[0] else dt_1[0] - now
        logger.info(f"Засыпаю на {sleep_time.total_seconds()} секунд")
        await asyncio.sleep(sleep_time.total_seconds())

if __name__ == "__main__":
    while True:
        asyncio.run(daemon())

