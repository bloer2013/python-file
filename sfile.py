import os
import telebot
import getpass

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

def send_file_to_telegram(file_path, chat_id):
    """Функция для отправки файла в Telegram"""
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, file)
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

@bot.message_handler(commands=['find'])
def handle_find_command(message):
    """Обрабатывает команду /find <имя файла>"""
    try:
        # Получаем имя файла из команды
        file_name = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите имя файла. Пример: /find example.txt")
        return

    # Ищем файл
    file_path = find_file(file_name)

    if file_path:
        bot.reply_to(message, f"Файл найден: {file_path}. Отправляю файл...")
        send_file_to_telegram(file_path, message.chat.id)

        # Спрашиваем о необходимости удаления файла
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.reply_to(message, f"Хотите удалить файл {file_path}?", reply_markup=markup)
        bot.register_next_step_handler(msg, lambda m: handle_delete_confirmation(m, file_path))
    else:
        bot.reply_to(message, f"Файл с именем {file_name} не найден.")

def handle_delete_confirmation(message, file_path):
    """Обрабатывает подтверждение удаления файла"""
    if message.text.lower() == 'да':
        delete_file(file_path)
        bot.reply_to(message, f"Файл {file_path} был успешно удалён.")
    else:
        bot.reply_to(message, "Файл не был удалён.")

def main():
    if getpass.getuser() != 'root':
        print("Пожалуйста, запустите скрипт от имени суперпользователя (sudo).")
    else:
        print("Бот запущен. Ожидание команд...")
        bot.polling()

if __name__ == "__main__":
    main()
