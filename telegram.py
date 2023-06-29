import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = ''
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Пополнение')
kb.add(b1)


with sqlite3.connect('users.db') as db:
    cursor = db.cursor()


#  Добавления пользователя в БД
def add_user(values):
    cursor.execute("INSERT INTO tg_balans(tg_id, balans) VALUES( ?, ?)", values)


# Добавление пользователя, если его еще нет в БД
def log_in(usdata, idofuser):
    cursor.execute("SELECT tg_id FROM tg_balans WHERE tg_id = ?", [idofuser])
    if cursor.fetchone() is None:
        add_user(usdata)
        db.commit()
    else:
        pass


def edit_balance(values):
    cursor.execute("UPDATE tg_balans SET balans = balans + ? WHERE (tg_id) = ?", values)
    db.commit()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id # id пользователя в тг
    data = [user_id, 0]
    log_in(data, user_id) # создание поля в БД, если пользователь не зерегистрирован
    await message.answer(f'{user_id}', reply_markup=kb)


@dp.message_handler(lambda message: message.text == "Пополнение")
async def topup(message: types.Message):
    await message.answer("Введите сумму пополнения")


@dp.message_handler(lambda message: int(message.text) > 0)
async def topup_update(message: types.Message):
    toped_balance = int(message.text)
    user_id = message.from_user.id
    edit_balance([toped_balance, user_id])
    await message.answer(f'Вы пополнили баланс на {message.text}')


if __name__ == '__main__':
    executor.start_polling(dp)