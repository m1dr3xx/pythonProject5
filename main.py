import asyncio  # Работа с асинхронностью
from random import choice

from aiogram import Bot, Dispatcher
from aiogram.filters import Command  # Фильтр для /start, /...
from aiogram.types import Message  # Тип сообщения

from config import config  # Config
from keyboards.reply import rsp_keyboard

API_TOKEN = config.token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # Менеджер бота


# dp.message - обработка сообщений
# Command(commands=['start'] Фильтр для сообщений, берём только /start
@dp.message(Command(commands=['start']))  # Берём только сообщения, являющиеся командой /start
async def start_command(message: Message):  # message - сообщение, которое прошло через фильтр
    await message.answer("Привет! Сыграем в камень, ножницы, бумага!!!!",
                         reply_markup=rsp_keyboard)  # Отвечаем на полученное сообщение


@dp.message()
async def handle_rps_game(message: Message):
    variants = ('Камень 🪨', 'Бумага 📃', 'Ножницы ✂️')
    user_choice = message.text
    if user_choice in variants:
        bots_choice = choice(variants)
        await message.answer(f'Я выбрал {bots_choice}')
        if (bots_choice == 'Бумага 📃' and user_choice == 'Камень 🪨' or
                bots_choice == 'Ножницы ✂️' and user_choice == 'Бумага 📃' or
                bots_choice == 'Камень 🪨' and user_choice == 'Ножницы ✂️'
        ):
            await message.answer('Я победил 😈')
        elif bots_choice == user_choice:
            await message.answer('Ничья 🤕')
        else:
            await message.answer('Я проиграл 😢')
    else:
        await message.answer('Вы написали кринж')


async def main():
    try:
        print('Bot Started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':  # Если мы запускаем конкретно этот файл.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
