#!/bin/bash

# Проверяем наличие python3.13
if ! command -v python3.13 &> /dev/null; then
    echo "Python 3.13 не найден. Устанавливаю..."
    sudo apt update
    sudo apt install software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt install python3.13 python3.13-venv -y
fi

echo "Создание виртуального окружения..."
python3.13 -m venv venv
source venv/bin/activate

echo "Установка библиотек..."
pip install --upgrade pip
pip install aiogram groq

echo "Запуск бота..."
python3 Anti-osk.py
