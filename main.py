# Импортируем все необходимые библиотеки:
# telebot для работы телеграмм - бота;
import telebot
# types из библиотеки telebot для создания кнопок;
from telebot import types
# settings для работы бота с чужим токеном;
from setting import *
# tok_1 для приватности бота;
# from tok_1 import *
# os для создания папок;
import os
# json для хранения полученных данных;
import json

# Передаем боту токен.
bot = telebot.TeleBot(token)
# Проверяет существование папки UserData.
if os.path.exists("UserData") is False:
    # Создание папки, если таковой нет.
    os.mkdir("UserData")

# Глобальную UserDict - для сохранения id пользователя в качестве ключа и название папки и ее содержимого в качестве значения;
UserDict = dict()
# Глобальную CurrentFolder - для сохранения названия текущей папки в виде строки;
CurrentFolder = ''
# Глобальную count_notes- для вычисления количества заметок;
count_notes = 0
# Глобальную button_handler- для включения/выключения декоратора, отвечающего на call-запросы;
button_handler = True
# Глобальную is_folder_delete- для настройки кнопки на разные функции;
is_folder_delete = False


# Создаем basic_keyboard для хранения id пользователя, и названия текущей папки.
def create_basic_keyboard(UserID: int):
    # Создание InlineKeyboard.
    basic_keyboard = types.InlineKeyboardMarkup()
    # Итерация всех названий папок.
    for name_folder in UserDict[UserID].keys():
        # Создание на каждую папку из списка кнопки.
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}", callback_data=f'{name_folder}')
        # Добавление кнопки на клавиатуру.
        basic_keyboard.add(name_folder)
    # Создание и добавление кнопок 'создать папку', 'переместить заметку' на клавиатуру.
    basic_keyboard.add(types.InlineKeyboardButton(text='➕Cоздать папку', callback_data='Cоздать папку'),
                       types.InlineKeyboardButton(text='➡️Переместить заметку', callback_data='Переместить заметку'))
    # Создание и добавление кнопок 'удалить папку', 'удалить заметку' на клавиатуру.
    basic_keyboard.add(types.InlineKeyboardButton(text='❌Удалить папку', callback_data='Удалить папку'),
                       types.InlineKeyboardButton(text='🗑Удалить заметку', callback_data='Удалить заметку'))
    # Вывод клавиатуры.
    return basic_keyboard


# Создаем additional_keyboard, в отличие от основной показывает не только названия папок, но и их содержимое.
def create_additional_keyboard(UserID: int):
    # Создание InlineKeyboard.
    additional_keyboard = types.InlineKeyboardMarkup()
    # Итерация всех названий папок.
    for name_folder in UserDict[UserID].keys():
        # Создание на каждую папку из списка кнопки и отображение на кнопке названия папки и их содержимое.
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}: {' '.join(UserDict[UserID][name_folder])}",
                                                 callback_data=f'{name_folder}')
        # Добавление кнопки на клавиатуру.
        additional_keyboard.add(name_folder)
    # Создание и добавление кнопок 'создать папку', 'переместить заметку' на клавиатуру.
    additional_keyboard.add(types.InlineKeyboardButton(text='➕Cоздать папку', callback_data='Cоздать папку'),
                            types.InlineKeyboardButton(text='➡️Переместить заметку',
                                                       callback_data='Переместить заметку'))
    # Создание и добавление кнопок 'удалить папку', 'удалить заметку' на клавиатуру.
    additional_keyboard.add(types.InlineKeyboardButton(text='❌Удалить папку', callback_data='Удалить папку'),
                            types.InlineKeyboardButton(text='🗑Удалить заметку', callback_data='Удалить заметку'))
    # Вывод клавиатуры.
    return additional_keyboard


# Создаем optional_keyboard, которая показывает только названия папок.
def create_optional_keyboard(UserID: int):
    # Создание InlineKeyboard.
    optional_keyboard = types.InlineKeyboardMarkup()
    # Итерация всех названий папок.
    for name_folder in UserDict[UserID].keys():
        # Создание на каждую папку из списка кнопки.
        name_folder = types.InlineKeyboardButton(text=f"📁{name_folder}", callback_data=f'{name_folder}')
        # Добавление кнопки на клавиатуру.
        optional_keyboard.add(name_folder)
        # Вывод клавиатуры.
    return optional_keyboard


# Функция, ловящая команду /start- выводит basic_keyboard и ознакомительный текст, о принципах работы бота.
@bot.message_handler(commands=['start'])
def start_bot(message):
    # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
    global mssg
    # Глобальная UserDict - для сохранения id пользователя в качестве ключа и название папки и ее содержимого в качестве значения.
    global UserDict
    # Глобальная user_id - для хранения id пользователя.
    global user_id
    # Сохранение текущего id пользователя.
    user_id = message.from_user.id
    # Cоздание UserDict определенного id пользователя.
    UserDict[user_id] = dict()
    # Вывод клавиатуры после нажатия ввода /start.
    basic_keyboard = create_basic_keyboard(message.from_user.id)
    # Вывод ознакомительного текста и basic_keyboard.
    mssg = bot.send_message(message.chat.id, f'{message.from_user.username}, я бот-организатор заметок.'
                                             f' Чтобы создать заметку нажмите на кнопку создать папку, введите название папки,'
                                             f' а затем нажмите на кнопку созданной папки и введите необходимую заметку.',
                            reply_markup=basic_keyboard)


# Функция, работающая при нажатии команды contacts- и вывод текста с ссылкой для связи.
@bot.message_handler(commands=['contacts'])
def help_bot(message):
    # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
    global mssg
    # Вывод клавиатуры после нажатия ввода /contacts.
    basic_keyboard = create_basic_keyboard(message.from_user.id)
    # Вывод текста и  basic_keyboard с ссылкой для связи.
    mssg = bot.send_message(message.chat.id, "По всем вопросам обращаться https://t.me/sleep_fox789",
                            reply_markup=basic_keyboard)


# Обработка call - запросы, при нажатии кнопки пользователем.
@bot.callback_query_handler(func=lambda call: button_handler)
def call_back(call):
    # Если получен отклик от кнопки.
    if call.message:
        # Глобальная is_folder_delete- для настройки кнопки на разные функции;
        global is_folder_delete
        # Если получен отклик от кнопки "создать папку".
        if call.data == "Cоздать папку":
            # Глобальная msg, в которой находится стартовое или последнее сообщение бота об итогах действия.
            global msg
            # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
            global mssg
            # Глобальная choice_handler- для разграничения выбора функции при набирании текста пользователем.
            global choice_handler
            # Глобальная UserDict - для сохранения id пользователя в качестве ключа и название папки и ее содержимого в качестве значения.
            global UserDict
            # Редактированный текст сменяется на сообщение о необходимости ввода данных.
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"Введите название папки:  ")
            # Меняем значение choice_handler на 2, для правильной обработки текста.
            choice_handler = 2
        # Если получен отклик от кнопки "переместить заметку".
        elif call.data == f"Переместить заметку":
            # Глобальная button_handler - для включения / выключения декоратора, отвечающего на call - запросы.
            global button_handler
            # Меняем button_handler на False, для блокирования нажатия кнопок.
            button_handler = False
            # Глобальная CurrentFolder- для сохранения названия текущей папки в виде строки.
            global CurrentFolder
            # Если в списке папок, 2 или более папки.
            if len(UserDict[user_id].values()) >= 2:
                # Создание additional_keyboard.
                additional_keyboard = create_additional_keyboard(call.from_user.id)
                # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=additional_keyboard,
                                            text="Введите название заметки, которую хотите переместить и через & папку,откуда переместить и через & папку"
                                                 " куда хотите переметить (пример: хлеб&фильмы&покупки): ")
                # Меняем значение choice_handler на 3, для правильной обработки текста.
                choice_handler = 3
            # Если в списке папок, папок меньше 2.
            else:
                # Создание basic_keyboard.
                basic_keyboard = create_basic_keyboard(call.from_user.id)
                # Редактированный текст сменяется на сообщение указывающее на ошибку.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=basic_keyboard,
                                            text="Перемещение невозможно/неправильно введенные данные: ")
                # Меняем button_handler на True, для активации нажатия кнопок.
                button_handler = True
        # Если получен отклик от кнопки "удалить папку".
        elif call.data == "Удалить папку":
            # Проверка: не пуст ли список с названиями папок.
            if len(UserDict[user_id]) >= 1:
                # Меняем is_folder_delete на True,  для настройки кнопки навзвания папки на удаление этой папки.
                is_folder_delete = True
                # Создание optional_keyboard.
                optional_keyboard = create_optional_keyboard(call.from_user.id)
                # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=optional_keyboard,
                                            text="Нажмите на папку, которую хотите удалить:")
            else:
                # Создание additional_keyboard.
                basic_keyboard = create_basic_keyboard(call.from_user.id)
                # Редактированный текст сменяется на сообщение указывающее на ошибку.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Невозможно удалить несуществующие папки",
                                            reply_markup=basic_keyboard)
                # Меняем button_handler на True, для активации нажатия кнопок.
                button_handler = True
        # Если получен отклик от кнопки "удалить заметку".
        elif call.data == "Удалить заметку":
            # Если количество заметок 1 и более.
            if count_notes >= 1:
                # Создание additional_keyboard.
                additional_keyboard = create_additional_keyboard(call.from_user.id)
                # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"Введите название заметки, которую хотите удалить:",
                                            reply_markup=additional_keyboard)
                # Меняем значение choice_handler на 5, для правильной обработки текста.
                choice_handler = 5
            # Если количество заметок меньше 1.
            else:
                # Создание basic_keyboard.
                basic_keyboard = create_basic_keyboard(call.from_user.id)
                # Редактированный текст сменяется на сообщение указывающее на ошибку.
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Невозможно удалить несуществующие заметки",
                                            reply_markup=basic_keyboard)
        # Если получен отклик названия папки.
        else:
            # Запоминание нажатия текущей папки.
            CurrentFolder = call.data
            # Если нужно удалить папку.
            if is_folder_delete == True:
                # Удаление папки, выбранной пользователем из словаря.
                del UserDict[user_id][CurrentFolder]
                # Создание basic_keyboard.
                basic_keyboard = create_basic_keyboard(call.from_user.id)
                # Вывод текста, отражающего успех (удаление папки) и basic_keyboard.
                mssg = bot.send_message(call.message.chat.id, "Ваши папки, после удаления:",
                                        reply_markup=basic_keyboard)
                # Удаляем  последнее сообщение, после нажатия кнопки.
                bot.delete_message(chat_id=call.message.chat.id, message_id=msg.message_id)
                # Меняем is_folder_delete на False, для создания новых заметок.
                is_folder_delete = False
            # Если нужно создать заметку.
            else:
                # Меняем значение choice_handler на 6.
                choice_handler = 6
                # Проверка: количество заметок меньше 1.
                if len(UserDict[user_id][CurrentFolder]) < 1:
                    # Редактированный текст сменяется на сообщение о необходимости ввода данных.
                    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"Выбранная папка {CurrentFolder}" + '\n' "Введите название заметки: ")
                # Если количество заметок больше 1.
                else:
                    # Редактированный текст сменяется на сообщение о вводе данных, и о заметках выбранной папки.
                    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=f"Выбранная папка {CurrentFolder}, в ней находится:"
                                                     f" {' '.join(UserDict[user_id][CurrentFolder])}"
                                                     + '\n'"Введите название заметки: ")


# Обработка текстовых сообщений от пользователя.
@bot.message_handler(content_types=["text"])
def add_note(message):
    # Сохранение текущего id пользователя.
    user_id = message.from_user.id
    # Глобальная choice_handler- для разграничения выбора функции при набирании текста пользователем.
    global choice_handler
    # Глобальная msg, в которой находится стартовое или последнее сообщение бота об итогах произведенного действия.
    global msg
    # Глобальная mssg, в которой находится cообщения, которые необходимо удалить при ошибке написания текста.
    global mssg
    # Глобальная button_handler - для включения / выключения декоратора, отвечающего на call - запросы.
    global button_handler
    # Глобальная count_notes- для вычисления количества заметок.
    global count_notes
    # Глобальная is_folder_delete- для настройки кнопки на разные функции;
    global is_folder_delete
    # Глобальная UserDict - для сохранения id пользователя в качестве ключа и название папки и ее содержимого в качестве значения.
    global UserDict
    # Если отправлен текст, смена choice_handler не происходила и не выбрана функция (избежание ошибки).
    if choice_handler == 1:
        # Удаляем стартовое или любое предыдущее сообщение, после нажатия кнопки.
        bot.delete_message(chat_id=message.chat.id, message_id=mssg.message_id)
        # Создание start_keyboard.
        basic_keyboard = create_basic_keyboard(message.from_user.id)
        # Вывод текста, отражающего результат предыдущих действий (ошибка) и start_keyboard.
        mssg = bot.send_message(message.chat.id,
                                f'{message.from_user.username}, повторите попытку (нажмите кнопку папки для создания заметки,'
                                f' или кнопку с действием которое выхотите совершить).',
                                reply_markup=basic_keyboard)
        # Удаляем введенное пользователем сообщение.
        bot.delete_message(message.chat.id, message.message_id)
    # Если пользователь нажал кнопку "создать папку" и произошла сменa choice_handler на 2.
    elif choice_handler == 2:
        # Локальная переменная - есть ли идентичные папки(1 - есть, 0 - нет).
        identical_folders = 0
        # Итерация всех названий папок.
        for name_folder in UserDict[message.from_user.id].keys():
            # Проверка: не пытается ли пользователь создать идентичные папки.
            if name_folder == message.text:
                identical_folders = 1
        if identical_folders > 1:
            # Создание basic_keyboard.
            basic_keyboard = create_basic_keyboard(message.from_user.id)
            # Вывод текста, отражающего результат предыдущих действий (идентичные папки) и basic_keyboard.
            mssg = bot.send_message(message.chat.id, "Такая папка уже есть: ", reply_markup=basic_keyboard)

        # Если идентичных папок нет, и список не пуст.
        else:
            # Добавление названия папки в словарь.
            UserDict[message.from_user.id][message.text] = list()
            # Открытие JSON-файла, для каждого пользователя отдельного, для хранения базы данных.
            with open(f"UserData/{message.from_user.id}.json", "w", encoding="utf-8") as write_file:
                json.dump(UserDict[user_id], write_file, ensure_ascii=False, indent=2, separators=(',', ': '))
            # Создание basic_keyboard.
            basic_keyboard = create_basic_keyboard(message.from_user.id)
            # Вывод текста, отражающего успех (создание папки) и start_keyboard.
            mssg = bot.send_message(message.chat.id, "Ваши папки:", reply_markup=basic_keyboard)
        # Удаляем последнее сообщение, после нажатия кнопки.
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        # Удаляем введенное пользователем сообщение.
        bot.delete_message(message.chat.id, message.message_id)
        # Меняем choice_handler на 1, для отклика на кнопки.
        choice_handler = 1
        # Переключаем количество идентичных папок на 0, для правильной работы бота.
        identical_folders = 0
    # Если пользователь нажал кнопку "переместить заметку" и произошла сменa choice_handler на 3.
    elif choice_handler == 3:
        # Локальная переменная для обработки количества перемещенных папок.
        moved_folders = 0
        # Проверка: есть ли в тексте пользователя 1 символ &.
        if message.text.count('&') == 2:
            # Итерируем значения в значениях словаря.
            for value in UserDict[user_id].values():
                # Разделяем заметку и папку введенные пользователем с клавиатуры по символу &.
                message.text1, message.text2, message.text3 = message.text.split('&')
                # Если заметка из сообщения имеется в значениях словаря, и ее нет в папке куда, надо переместить ее.
                if message.text1 in value and message.text1 not in UserDict[user_id][message.text3]:
                    # Удаление заметки из папки, где она находится.
                    UserDict[user_id][message.text2].remove(message.text1)
                    # Добавление заметки в словарь в новую папку.
                    UserDict[user_id][message.text3].append(message.text1)
                    # Локальная переменная для обработки количества перемещенных папок.
                    moved_folders = +1
                    # Проверка: количество папок больше 1.
                    if moved_folders >= 1:
                        # Создание additional_keyboard.
                        additional_keyboard = create_additional_keyboard(message.from_user.id)
                        # Вывод текста, отражающего успех (перемещение заметки) и additional_keyboard.
                        mssg = bot.send_message(message.chat.id, "Ваши заметки, после перемещения:",
                                                reply_markup=additional_keyboard)
                        # Выход, если перемещение произошло.
                        break
                else:
                    # Создание additional_keyboard.
                    additional_keyboard = create_additional_keyboard(message.from_user.id)
                    # Вывод текста, отражающего результат предыдущих действий (ошибка) и additional_keyboard.
                    mssg = bot.send_message(message.chat.id,
                                            "Перемещения не произошло, попробуйте заново"
                                            " (проверьте правильность написания/присутствие заметок):",
                                            reply_markup=additional_keyboard)
                    # Выход, если перемещения не произошло.
                    break
        # Если заметка сообщения не имеется в значениях словаря, или она есть в папке для перемещения.
        else:
            # Создание additional_keyboard.
            additional_keyboard = create_additional_keyboard(message.from_user.id)
            # Вывод текста, отражающего результат предыдущих действий (ошибка) и additional_keyboard.
            mssg = bot.send_message(message.chat.id,
                                    "Перемещения не произошло, попробуйте заново"
                                    " (проверьте правильность написания/присутствие заметок):",
                                    reply_markup=additional_keyboard)
        # Удаляем последнее сообщение, после нажатия кнопки.
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        # Удаляем введенное пользователем сообщение.
        bot.delete_message(message.chat.id, message.message_id)
        # Меняем choice_handler на 1, для отклика на кнопки.
        choice_handler = 1
        # Меняем button_handler на True, для активации нажатия кнопок.
        button_handler = True
        # Локальная переменная для обработки количества перемещенных папок.
        moved_folders = 0
    # Если пользователь нажал кнопку "удалить заметку" и произошла сменa choice_handler на 5.
    elif choice_handler == 5:
        # Локальная переменная для обработки количества удаленных папок.
        deleted_notes = 0
        # Итерируем значения в значениях словаря.
        for value in UserDict[user_id].values():
            # Проверка: есть ли в значениях словаря заметки, идентичной тексту, введенному пользователем.
            while message.text in value:
                # Удаление заметки из папки, где она находится.
                value.remove(message.text)
                # Вычисление количества заметок после удаления.
                count_notes -= 1
                # Локальная переменная для обработки количества удаленных папок.
                deleted_notes += 1
        # Проверка: если количество удаленных заметок больше 1.
        if deleted_notes > 0:
            # Создание additional_keyboard.
            additional_keyboard = create_additional_keyboard(message.from_user.id)
            # Вывод текста, отражающего успех (удаление заметки) и additional_keyboard.
            mssg = bot.send_message(message.chat.id, "Ваши заметки, после удаления:",
                                    reply_markup=additional_keyboard)
        # Если нет в значениях словаря заметки, идентичной тексту, введенному пользователем.
        else:
            # Создание additional_keyboard.
            additional_keyboard = create_additional_keyboard(message.from_user.id)
            # Вывод текста, отражающего результат предыдущих действий (ошибка) и additional_keyboard.
            mssg = bot.send_message(message.chat.id,
                                    "Заметки с таким именем не существует: проверьте написание):",
                                    reply_markup=additional_keyboard)
        # Удаляем  последнее сообщение, после нажатия кнопки.
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        # Удаляем введенное пользователем сообщение.
        bot.delete_message(message.chat.id, message.message_id)
        # Меняем choice_handler на 1, для отклика на кнопки.
        choice_handler = 1
    # Если пользователь отправил текст, после того как нажал на название папки и произошла сменa choice_handler на 6.
    else:
        # Добавление заметки в значения словаря в виде списка.
        UserDict[user_id][CurrentFolder].append(message.text)
        # Открытие JSON-файла, для каждого пользователя отдельного, для хранения базы данных.
        with open(f"UserData/{message.from_user.id}.json", "w", encoding="utf-8") as write_file:
            json.dump(UserDict[user_id], write_file, ensure_ascii=False, indent=2, separators=(',', ': '))
        # Создание basic_keyboard.
        basic_keyboard = create_basic_keyboard(message.from_user.id)
        # Вывод текста, отражающего успех (создание заметки) и basic_keyboard.
        mssg = bot.send_message(message.chat.id,
                                text=f"Заметки из папки {CurrentFolder}: {' '.join(UserDict[user_id][CurrentFolder])}",
                                reply_markup=basic_keyboard)
        # При каждом создании заметки вычисление количества заметок.
        count_notes += 1
        # Удаляем  последнее сообщение, после нажатия кнопки.
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        # Удаляем введенное пользователем сообщение.
        bot.delete_message(message.chat.id, message.message_id)
        # Меняем choice_handler на 1, для отклика на кнопки.
        choice_handler = 1


# Запуск работы кода.
if __name__ == "__main__":
    # Опрос серверов Telegram на предмет новых сообщений.
    bot.polling(none_stop=True)
