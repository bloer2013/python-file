import os
import telebot
import subprocess
import getpass

# Ваш токен бота Telegram
API_TOKEN = 'ВАШ_ТЕЛЕГРАМ_ТОКЕН'
CHAT_ID = 'ID_ЧАТА_ИЛИ_ПОЛЬЗОВАТЕЛЯ'

bot = telebot.TeleBot(API_TOKEN)

def find_file(file_name):
    """Функция для поиска файла по имени"""
    # Начинаем поиск с корневой директории
    for root, dirs, files in os.walk('/'):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def send_file_to_telegram(file_path):
    """Функция для отправки файла в Telegram"""
    with open(file_path, 'rb') as file:
        bot.send_document(CHAT_ID, file)

def delete_file(file_path):
    """Функция для удаления файла"""
    try:
        os.remove(file_path)
        print(f"Файл {file_path} был удалён.")
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")

def main():
    # Получаем имя файла от пользователя
    file_name = input("Введите имя файла для поиска: ")

    # Ищем файл
    file_path = find_file(file_name)

    if file_path:
        print(f"Файл найден: {file_path}")

        # Отправляем файл в Telegram
        send_file_to_telegram(file_path)
        print(f"Файл {file_name} отправлен")
