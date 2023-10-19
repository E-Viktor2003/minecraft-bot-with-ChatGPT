# Minecraft бот с ChatGPT
[RU](https://github.com/E-Viktor2003/minecraft-bot-with-ChatGPT/blob/main/README_RU.md)  [EN](https://github.com/E-Viktor2003/minecraft-bot-with-ChatGPT/blob/main/README.md)    
Minecraft бот с ChatGPT может выполнять команды Minecraft, запоминать определенную информацию и помнить предыдущий диалог.

## Установка:

1. Установите Python
   - [Скачать Python](https://www.python.org/)
2. Установите Node.js
   - [Скачать Node.js](https://nodejs.org/ru)
3. Установите библиотеку Mineflayer для Node.js
   - Выполните в терминале команду:
     `npm i mineflayer`
4. Установите библиотеку JavaScript и g4f для Python
   - Выполните в терминале команду:
     `pip install javascript g4f`
5. Клонируйте репозиторий
    - `git clone https://github.com/E-Viktor2003/minecraft-bot-with-ChatGPT.git`

### Настройка и запуск

1. Откройте файл config.py и измените значения на необходимые
   ```
   - minecraft_version - Версия Minecraft
   - host - хост сервера
   - port - порт сервера, если порта нет, то установите значение 25565
   - username - имя бота
   ```
3. Запустите скрипт Bot.py
    - Команда:
      `python Bot.py`
4. Подождите, пока бот зайдет на сервер
    - После того как бот зашел на сервер, напишите в чат любое сообщение и подождите ответ.
