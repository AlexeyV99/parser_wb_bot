import datetime
import csv
from telebot import TeleBot
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import parser
import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    print('Ключ не найден')
else:
    load_dotenv()


API_TOKEN = os.getenv('BOT_KEY')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT')

# Объект бота
bot = TeleBot(token=API_TOKEN)


user_states = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = ("Привет! Это парсер WB!\nВведи наименование товара!")
    bot.send_message(message.chat.id, welcome_text)
    bot.register_next_step_handler(message, get_product_name)


def get_product_name(message):
    user_states[message.from_user.id] = {"product": message.text,
                                     "number": 0,
                                     "file_name": ""}
    bot.send_message(message.chat.id, "Сколько товаров собрать?")
    bot.register_next_step_handler(message, get_product_number)


def get_product_number(message):
    if message.text.isdigit():
        user_states[message.from_user.id]["number"] = int(message.text)
        bot.send_message(message.chat.id, "Собираем товары! Ожидайте...")
        get_result(message)
    else:
        bot.send_message(message.chat.id, "Должно быть числовой значение!",
                         reply_to_message_id=message.id, )
        get_num_error(message)


def get_num_error(message):
    bot.send_message(message.chat.id, "Сколько товаров собрать?")
    bot.register_next_step_handler(message, get_product_number)


def get_result(message):
    # Генерируем уникальное имя файла
    uniq_file_name = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
    uniq_file_name = f'parse_wb_{uniq_file_name}.csv'
    user_states[message.from_user.id]['file_name'] = uniq_file_name
    print(user_states)
    # Создаем файл
    with open(uniq_file_name, 'w', newline='', encoding='cp1251') as file:
        writer = csv.writer(file)
        writer.writerow(['ссылка', 'название', "рейтинг", "цена"])
    # Парсинг
    parser.get_page(user_states[message.from_user.id]["file_name"],
                    user_states[message.from_user.id]["product"],
                    user_states[message.from_user.id]["number"]
                    )
    bot.send_message(message.chat.id, "Товары собраны!!!")
    bot.send_message(ADMIN_CHAT_ID, f'Собраны товары: {user_states[message.from_user.id]['product']}\n'
                                    f'Количество: {user_states[message.from_user.id]['number']}\n'
                                    f'Пользователь: {message.from_user.first_name} (id:{message.from_user.id})')
    # Отправляем файл в чат
    file = open(uniq_file_name, 'rb')
    bot.send_document(message.chat.id, file)
    # Удаляем файл
    os.remove(uniq_file_name)


def main():
   print('[INFO] Бот запущен')
   bot.polling()


if __name__ == "__main__":
   main()
