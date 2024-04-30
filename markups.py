from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

to_menu = InlineKeyboardButton('📋Основные функции:', callback_data='main_menu')
to_menu_only = InlineKeyboardMarkup(row_width=1).add(to_menu)


trainings = InlineKeyboardButton('🏋️ Тренировки', callback_data='trainings')
feeding = InlineKeyboardButton('🍽️ Питание', callback_data='feeding')
profile = InlineKeyboardButton('🙎🏻 Профиль', callback_data='profile')
main_menu = InlineKeyboardMarkup(row_width=1).add(trainings, feeding, profile)


continue_training = InlineKeyboardButton('➡ Продолжить', callback_data='continue_training')
new_training = InlineKeyboardButton('🆕 Новая', callback_data='new_training')
trainings_menu = InlineKeyboardMarkup(row_width=1).add(continue_training, new_training, to_menu)

not_chosen_training = InlineKeyboardMarkup(row_width=2).insert(new_training)
not_chosen_training.insert(trainings)

apply_training = InlineKeyboardButton('✅ Принять', callback_data='apply_training')
deny_training = InlineKeyboardButton('↩  Назад', callback_data='trainings')
choose_training_menu = InlineKeyboardMarkup(row_width=2).insert(apply_training)
choose_training_menu.insert(deny_training)

after_creating_training_menu = InlineKeyboardMarkup(row_width=2).insert(continue_training)
after_creating_training_menu.insert(to_menu)

start_training_btn = InlineKeyboardButton('🟢 Начать', callback_data='next_exercise')
start_training_menu = InlineKeyboardMarkup(row_width=2).insert(start_training_btn)
start_training_menu.insert(to_menu)

active_training_next_btn = InlineKeyboardButton('➡ Далее', callback_data='next_iteration')
active_training_exit_btn = InlineKeyboardButton('↩ Выход', callback_data='exit_training')
active_training_menu = InlineKeyboardMarkup(row_width=2).insert(active_training_next_btn)
active_training_menu.insert(active_training_exit_btn)

active_training_skip_timer = InlineKeyboardButton('🛑 Пропустить', callback_data='skip_timer')
active_training_skip_timer_menu = InlineKeyboardMarkup(row_width=1).add(active_training_skip_timer)

training_warning_menu = InlineKeyboardMarkup(row_width=2)
training_exit_ok_btn = InlineKeyboardButton('✅ Ок', callback_data='trainings')
training_exit_abort_btn = InlineKeyboardButton('🛑 Отмена', callback_data='next_exercise')
training_warning_menu.insert(training_exit_ok_btn)
training_warning_menu.insert(training_exit_abort_btn)

body_index = InlineKeyboardButton('📊 ИМТ', callback_data='body_index')
feeding_menu = InlineKeyboardMarkup(row_width=1).add(body_index, to_menu)

add_gender = InlineKeyboardButton('Пол', callback_data='add_gender')
add_age = InlineKeyboardButton('Возраст', callback_data='add_age')
add_height = InlineKeyboardButton('Рост', callback_data='add_height')
add_weight = InlineKeyboardButton('Вес', callback_data='add_weight')
add_muscle = InlineKeyboardButton('Масса скелетной мускулатуры', callback_data='add_muscle')
add_fat = InlineKeyboardButton('Содержание жира', callback_data='add_fat')
profile_menu = InlineKeyboardMarkup(row_width=2).add(add_gender, add_age, add_height, add_weight).add(add_muscle)
profile_menu.add(add_fat).add(to_menu)