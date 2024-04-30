from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from Database import database as db
from states import Training
import markups as mks
from time import sleep
import os

async def init_trainings(dp, path):

    try:
        os.mkdir(f'{path}\Training\Trainings\Набор веса')
        os.mkdir(f'{path}\Training\Trainings\Похудение')
        os.mkdir(f'{path}\Training\Trainings\Удержание веса')

    except:
        pass

    async def start_training(training_info, callback_query, state):

        await Training.active_training.set()

        try:
            with open(f'{path}\Training\Trainings\\{training_info[0]}\\{training_info[1]}\\{training_info[2]}.txt', encoding="utf-8") as file:
                lines = file.readlines()

                await state.update_data(lines = lines, line_number = 0)

            await callback_query.message.answer('Вы готовы начать тренировку?',
                                                reply_markup=mks.start_training_menu)
        except FileNotFoundError:

            await callback_query.message.answer('Вы еще не выбрали тренировку!',
                                                reply_markup=mks.not_chosen_training)

    @dp.callback_query_handler(lambda c: c.data == 'next_exercise', state = Training.active_training)
    async def next_exercise(callback_query: CallbackQuery, state: FSMContext):

        await callback_query.message.delete()
        data = await state.get_data()
        lines = data['lines']
        line_number = data['line_number']

        try:
            line = lines[line_number].split(':')
            exercise_message = await callback_query.message.answer(
                f'Упражнение: <b>{line[0]}</b>\nКоличество подходов: <b>{line[1]}</b>\n\nВидео: <i>{line[2]}</i>',
                parse_mode='HTML',
                reply_markup=mks.active_training_menu)

        except IndexError:

            await callback_query.message.answer('🎉 Поздравляю, тренировка закончена!', reply_markup=mks.to_menu_only)

            current_training_info = db.get_training(callback_query.from_user.id)
            trainings_list = os.listdir(f'{path}\Training\Trainings\\{current_training_info[0]}\\{current_training_info[1]}')
            day = int(current_training_info[2])

            if day < len(trainings_list):

                new_day = day + 1

            else:

                new_day = 1


            db.set_training(callback_query.from_user.id, current_training_info[0], current_training_info[1], new_day)
            db.update_trainings_count(callback_query.from_user.id)

        try:

            await state.update_data(iteration=3, line=line, exercise_message=exercise_message)

        except:

            pass


    @dp.callback_query_handler(lambda c: c.data == 'next_iteration', state = Training.active_training)
    async def continue_training(callback_query: CallbackQuery, state: FSMContext):


        data = await state.get_data()
        iteration = data['iteration']
        line = data['line']
        exercise_message = data['exercise_message']
        try:

            iteration_message = data['iteration_message']
            await iteration_message.delete()

        except:

            pass


        if iteration % 2 and iteration < len(line):

            iteration_message = await callback_query.message.answer(f'Количество повторений: {line[iteration]}')
            await state.update_data(iteration_message = iteration_message)


        elif iteration % 2 == 0 and iteration < len(line):

            iteration_message = await callback_query.message.answer(f'⏳ Отдых - {line[iteration]} сек.', reply_markup=mks.active_training_skip_timer_menu)
            await exercise_message.edit_reply_markup(None)


            for seconds in range(int(line[iteration])-1, 0, -1):


                if db.check_timer(callback_query.from_user.id) == 0:
                    sleep(1)
                    await iteration_message.edit_text(f'⏳ Отдых - {seconds} сек.',
                                                      reply_markup=mks.active_training_skip_timer_menu)

                else:
                    db.default_timer(callback_query.from_user.id)
                    break

            await iteration_message.edit_text(f'⌛ Отдых закончен. Приступить к следующему подходу!')
            await exercise_message.edit_reply_markup(mks.active_training_menu)
            await state.update_data(iteration_message = iteration_message)


        else:

            await callback_query.message.answer('❗ Упражнение закончено!\nКак только будешь готов приступить к следующему, нажми на кнопку!', reply_markup=mks.start_training_menu)

            line_number = data['line_number']
            line_number += 1


            await state.update_data(line_number = line_number)
            await exercise_message.delete()


        iteration += 1
        await state.update_data(iteration = iteration)


    @dp.callback_query_handler(lambda c: c.data == 'skip_timer', state='*')
    async def skip_timer(callback_query: CallbackQuery):
        await db.skip_timer(callback_query.from_user.id)


    @dp.callback_query_handler(lambda c: c.data == 'exit_training', state=Training.active_training)
    async def exit_training(callback_query: CallbackQuery, state: FSMContext):

        await callback_query.message.delete()
        data = await state.get_data()

        try:

           iteration_message = data['iteration_message']
           await iteration_message.delete()

        except:

            pass

        await callback_query.message.answer('Прогресс этой тренировки не сохранится!', reply_markup=mks.training_warning_menu)


    @dp.callback_query_handler(lambda c: c.data == 'continue_training', state='*')
    async def continue_training(callback_query: CallbackQuery, state: FSMContext):

        training_info = db.get_training(callback_query.from_user.id)
        await callback_query.message.delete()

        await start_training(training_info, callback_query, state)


    @dp.callback_query_handler(lambda c: c.data == 'new_training', state='*')
    async def new_training(callback_query: CallbackQuery, state: FSMContext):

        await callback_query.message.delete()

        categories_of_trainings_list = os.listdir(f'{path}\Training\Trainings')
        categories_of_trainings_menu = InlineKeyboardMarkup(row_width=1)

        for category in categories_of_trainings_list:

            category_btn = InlineKeyboardButton(category, callback_data=category)
            categories_of_trainings_menu.add(category_btn)
            await show_categories(dp, category, path)

        categories_of_trainings_menu.add(mks.trainings)

        await callback_query.message.answer('Выберите категорию тренировки',
                                            reply_markup=categories_of_trainings_menu)


async def show_categories(dp, category, path):

    @dp.callback_query_handler(lambda c: c.data == category, state = '*')
    async def categories(callback_query: CallbackQuery, state: FSMContext):

        await callback_query.message.delete()

        trainings_list = os.listdir(f'{path}\Training\Trainings\\{category}')
        trainings_list_menu = InlineKeyboardMarkup(row_width=1)

        for training in trainings_list:

            training_btn = InlineKeyboardButton(training, callback_data=training)
            trainings_list_menu.add(training_btn)
            await show_trainings(dp, training, category, path)

        trainings_list_menu.add(mks.trainings)

        await callback_query.message.answer('Выберите тренировку',
                                            reply_markup=trainings_list_menu)


async def show_trainings(dp, training, category, path):

    @dp.callback_query_handler(lambda c: c.data == training, state='*')
    async def categories(callback_query: CallbackQuery, state: FSMContext):

        await callback_query.message.delete()

        training_info = ''

        days_list = os.listdir(f'{path}\Training\Trainings\\{category}\\{training}')

        for day in days_list:

            training_info += (f'\n\n<b>День цикла <u>№{day.split(".")[0]}</u></b>\n\n')
            with open(f'{path}\Training\Trainings\\{category}\\{training}\\{day}',  encoding="utf-8") as day_of_training:

                excercises = day_of_training.readlines()

                for exercise in excercises:
                    exercise_info = exercise.split(":")
                    training_info += (f'<b>{exercise_info[0]}</b>, количество подходов - {exercise_info[1]}\n')


        await callback_query.message.answer(f'<b>{training}</b>\n{training_info}',
                                            parse_mode="HTML",
                                            reply_markup=mks.choose_training_menu)


    @dp.callback_query_handler(lambda c: c.data == 'apply_training', state='*')
    async def categories(callback_query: CallbackQuery, state: FSMContext):

        db.set_training(callback_query.from_user.id, category, training, '1')

        await callback_query.message.delete()

        await callback_query.message.answer(f'✅ Вы выбрали тренировку - <b>{training}</b>\n',
                                            parse_mode="HTML",
                                            reply_markup=mks.after_creating_training_menu)