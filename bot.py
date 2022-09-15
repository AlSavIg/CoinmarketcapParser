from aiogram import Bot, Dispatcher, executor, types
from config import token
from aiogram.dispatcher.filters import Text
from aiofiles import os
import async_main

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Собрать данные")
    keyboard.add(button_1)
    await message.answer('Здравствуйте, для получения данных '
                         'нажмите соответствующую клавишу в меню.'
                         'Для обновления клавиатуры снова введите команду /start',
                         reply_markup=keyboard)


@dp.message_handler(Text(equals="Собрать данные"))
async def cmd_answer(message: types.Message):
    await message.answer('Пожалуйста, ожидайте, идет сбор данных')
    file = await async_main.get_data()
    await message.answer_document(open(file, 'rb'))
    await os.remove(file)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
