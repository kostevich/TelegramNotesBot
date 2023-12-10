# TelegramNotesBot 
**TelegramNotesBot** – yчебный проект [Telegram](https://telegram.org)-бота, помогающий структурировать данные для заметок. Основные функции: менеджмент по тематикам, добавление и удаление заметок. Данные пользователя сохраняются в формате JSON.

# Порядок установки и использования
1. Загрузить репозиторий. Распаковать.
2. Установить [Python](https://www.python.org/downloads/) версии не старше 3.11. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [dublib](https://github.com/DUB1401/dublib), [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
```
pip install git+https://github.com/DUB1401/dublib
pip install pyTelegramBotAPI
```
Либо установить сразу все пакеты при помощи следующей команды, выполненной из директории скрипта.
```
pip install -r requirements.txt
```
4. Настроить бота путём редактирования [_Settings.json_](#Settings).
5. Можно добавить команды в бота, для удобства работы [(бот будет работать и без этой настройки)](#AddCommands). 
6. Запустить файл _main.py_ командой:
```
python main.py
```
7. Перейти в чат с ботом, и следовать его инструкциям.

# Settings.json
<a name="Settings"></a> 
```JSON
"token": ""
```
Сюда необходимо занести токен бота Telegram (можно получить у [BotFather](https://t.me/BotFather)).

# Добавление команд 
<a name="AddCommands"></a> 
Можно указать в настройках бота в [BotFather](https://t.me/BotFather).

start - start working.

contacts - send contact information.

# Пример работы
**Обработка команды start и contacts:**

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/6b5987fc-67ba-4a04-8db4-ac1c026b88af)

**Итог создания заметки:**

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/d1b41657-0d19-4f1e-85db-f93f311a9a3f)

**Итог создания папки:**

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/09008388-4f02-4c18-8d4f-b1b405a8c31d)

**Удаление заметки:**

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/41dfde5a-e357-4fbd-9966-5aec37d412b1)

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/c20e02dd-5d90-474b-b9f5-090c1fc67903)

**Удаление папки:**

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/ed9926b9-143f-4942-82fa-e7e4b4f31a68)

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/6c83c824-40a2-4104-8065-ab0bfa21a643)

**Перемещение заметок:**

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/a2cd3968-5322-4a97-abe9-7bbf7696652b)

![image](https://github.com/kostevich/TelegramNotesBot/assets/109979502/f9445f78-35bd-4802-a161-1c2c636db5ad)

_Copyright © Kostevich Irina. 2023._
