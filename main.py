import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token="5687084993:AAHN1Mw6gHOlDobVhDcUxki7gP4eoTvGyfc")
dp = Dispatcher(bot)
db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Ви приєдналися до Just Eat bot!')


@dp.message_handler(Text(contains="/sendall"), content_types=["text", "photo", "video"])
async def sendall(message: types.Message):
    print(message)
    if message.chat.type == 'private' and int(message.from_user.id) in [320659042]:
        text = message.text[9:] if message.text else message.caption[9:]
        users = db.get_users()
        for row in users:
            try:
                if message.photo and text:
                    await bot.send_photo(chat_id=row[0], photo=message.photo[-1].file_id, caption=text)
                elif message.photo and not text:
                    await bot.send_photo(chat_id=row[0], photo=message.photo[-1].file_id)
                elif message.video and text:
                    await bot.send_video(chat_id=row[0], video=message.video.file_id, caption=text)
                elif message.video and not text:
                    await bot.send_video(chat_id=row[0], video=message.video.file_id)
                else:
                    await bot.send_message(row[0], text)
                if int(row[1]) != 1:
                    db.set_active(row[0], 1)
            except Exception as e:
                logging.error(f"{e} {row[0]} {row[0]}")
                db.set_active(row[0], 0)

        await bot.send_message(message.from_user.id, "Успішна розсилка!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
