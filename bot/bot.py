from aiogram import Bot, Dispatcher, executor, types
from parser.config import token
from aiogram.dispatcher.filters import Text
from aiofiles import os
from parser import extended_parser

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
    file = await extended_parser.get_data()
    await message.answer_document(open(file, 'rb'))
    await os.remove(file)


def activate_bot():
    executor.start_polling(dp, skip_updates=False)


if __name__ == "__main__":
    activate_bot()
