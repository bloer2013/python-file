import os
import telebot
import getpass
import subprocess

# Ваш токен бота Telegram
API_TOKEN = 'ВАШ_ТЕЛЕГРАМ_ТОКЕН'
CHAT_ID = 'ID_ЧАТА_ИЛИ_ПОЛЬЗОВАТЕЛЯ'

bot = telebot.TeleBot(API_TOKEN)

def find_file(file_name):
    """Функция для поиска файла по имени"""
    for root, dirs, files in os.walk('/'):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def send_file_to_telegram(file_path):
    """Функция для отправки файла в Telegram"""
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(CHAT_ID, file)
        print(f"Файл {file_path} успешно отправлен в Telegram.")
    except Exception as e:
        print(f"Ошибка при отправке файла в Telegram: {e}")

def delete_file(file_path):
    """Функция для удаления файла"""
    try:
        os.remove(file_path)
        print(f"Файл {file_path} был удалён.")
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")

def main():
    while True:
        # Получаем имя файла от пользователя
        file_name = input("Введите имя файла для поиска (или 'exit' для выхода): ")

        if file_name.lower() == 'exit':
            print("Завершение работы.")
            break

        # Ищем файл
        file_path = find_file(file_name)

        if file_path:
            print(f"Файл найден: {file_path}")

            # Отправляем файл в Telegram
            send_file_to_telegram(file_path)

            # Спрашиваем пользователя, нужно ли удалить файл
            delete_choice = input(f"Хотите удалить файл {file_path}? (y/n): ").lower()

            if delete_choice == 'y':
                delete_file(file_path)
            else:
                print("Файл не был удалён.")
        else:
            print(f"Файл с именем {file_name} не найден.")

if __name__ == "__main__":
    if getpass.getuser() != 'root':
        # Проверка на запуск от sudo
        print("Пожалуйста, запустите скрипт от имени суперпользователя (sudo).")
    else:
        main()
