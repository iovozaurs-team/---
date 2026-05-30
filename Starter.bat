@echo off
echo Создание виртуального окружения...
python -m venv venv
call venv\Scripts\activate

echo Установка библиотек...
python -m pip install --upgrade pip
pip install aiogram groq

echo Запуск бота...
python "Anti-osk.py"
pause
