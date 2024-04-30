from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

import Database.database as db
from Training import training
from IMB import feeding
import profile

from states import Training
import markups as mks

bot = Bot(token='6831818510:AAGkfAmMLyBzFq1NcVz8ejZ7Qt5RZRl1gP4')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    await db.init_db()


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username


    await db.create_profile(user_id, username)


    await Training.default.set()


    welcomeText = (f'👋 Привет, <b>{message.from_user.first_name}</b>!\n'
                   f'🏆 Я могу помочь тебе в осуществлении твоих фитнес-целей! Со мной ты сможешь:\n'
    f'💪 Получить персонализированную программу тренировок\n'
    f'🥗 Построить здоровое питание\n'
    f'❤️ Осознанно следить за своим здоровьем')
    await bot.send_message(message.from_user.id, welcomeText, parse_mode = "HTML", reply_markup=mks.main_menu)


@dp.callback_query_handler(lambda c: c.data == 'main_menu', state='*')
async def main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    await Training.default.set()
    await callback_query.message.answer("📋Основные функции:", reply_markup=mks.main_menu)


@dp.callback_query_handler(lambda c: c.data == 'trainings', state='*')
async def trainings_menu(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    path = os.getcwd()
    await training.init_trainings(dp, path)
    await callback_query.message.answer("💪В разделе с тренировками ты найдешь разнообразные упражнения и готовые программы тренировок, а я буду следить за твоими результатами и прогрессом.\n"
                                        "👀 Если у тебя еще нет программы тренировок, не волнуйся! Я помогу её тебе составить, учитывая твои цели и уровень подготовки. 🏋️",
                                        reply_markup=mks.trainings_menu)




@dp.callback_query_handler(lambda c: c.data == 'feeding', state='*')
async def feeding_menu(callback_query: types.CallbackQuery):

    await callback_query.message.delete()

    await callback_query.message.answer("🍔 В разделе с рационом питания ты сможешь видеть свой ежедневный рацион питания, а также получать персонализированные рекомендации и меню на день или неделю.\n"
                                        "✍️ Если тебе нужно составить меню на день или неделю, обращайся ко мне! Я с удовольствием помогу тебе с этим. 🥗",
                                        reply_markup=mks.feeding_menu)

    await feeding.get_height_weight(dp)


@dp.callback_query_handler(lambda c: c.data == 'profile', state='*')
async def profile_menu(callback_query: types.CallbackQuery):

    await callback_query.message.delete()

    await profile.profile(dp, callback_query)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
