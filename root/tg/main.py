import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramNotFound
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from dotenv import load_dotenv, find_dotenv
import os

import root.db.setup as db
import root.db.models as models

storage = MemoryStorage()

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TG_API'))
dp = Dispatcher(storage=storage)
admin_ids = {459471362, 717398944}

messages_to_broadcast = list()

builder = ReplyKeyboardBuilder()
builder.button(text='/send')
builder.button(text='/clear')


@dp.message(Command('start'))
async def start(message: types.Message):
    session = db.Session()
    try:
        # new_user = models.User(tg_id=message.from_user.id, username=message.from_user.username)
        # session.add(new_user)
        # session.commit()
        
        if message.from_user.id in admin_ids:
            await message.answer("Добро пожаловать, хозяин!", reply_markup=builder.as_markup())
        else:
            await message.answer("Ты успешно подписался на мероприятия клуба!")
    except Exception as x:
        print(x)
        await message.answer("У нас проблемы  с базой данных. Напиши мне @dimatatatarin")
    finally:
        if session.is_active:
            session.close()


@dp.message(Command('send'), F.from_user.id.in_(admin_ids))
async def send(message: types.Message):
    await message.delete()
    global messages_to_broadcast
    session = db.Session()
    try:
        all_users = session.query(models.User).all()
        for user in all_users:
            for msg in messages_to_broadcast:
                try:
                    await bot.copy_message(chat_id=user.tg_id, message_id=msg, from_chat_id=message.from_user.id,
                                           parse_mode=ParseMode.HTML)
                except Exception as x:
                    pass
        messages_to_broadcast = list()  # Clear the messages after broadcasting
        await bot.send_message(message.from_user.id, "Сообщение разослано всем участникам")
    
    except Exception as x:
        print(x)
        await message.answer("У нас проблемы  с базой данных. Напиши мне @dimatatatarin")
    
    finally:
        if session.is_active:
            session.close()
            

@dp.message(Command('clear'), F.from_user.id.in_(admin_ids))
async def clear(message: types.Message):
    await message.delete()
    global messages_to_broadcast
    messages_to_broadcast = list()
    await bot.send_message(message.from_user.id, 'История очищена')


@dp.message(F.from_user.id.in_(admin_ids))
async def admin(message: types.Message):
    global messages_to_broadcast
    messages_to_broadcast.append(message.message_id)
    await bot.send_message(message.from_user.id, "Сообщение записано и готово к отправке")


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
