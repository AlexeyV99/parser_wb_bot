import datetime
import csv
import parser
import os
from telebot import TeleBot
from dotenv import load_dotenv, find_dotenv
import logging
from logging import config
from logging_conf import dict_config


# Настройка логирования
config.dictConfig(dict_config)
logger = logging.getLogger('appLogger')

# Загрузка переменных окружения
if not find_dotenv():
    logger.error('Токен не найден')
else:
    logger.info('Токен найден')
    load_dotenv()

# Переменные окружения
API_TOKEN = os.getenv('BOT_KEY')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT')

# Объект бота
bot = TeleBot(token=API_TOKEN)

# Состояние пользователя
user_states = {}


@bot.message_handler(commands=['start'])
def bot_start(message):
    logger.info(f"Выполнена коменда [start] для id({message.from_user.id})")
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
        logger.warning("Ошибка ввода количества товаров!")
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
    # Создаем файл
    with open(uniq_file_name, 'w', newline='', encoding='cp1251') as file:
        writer = csv.writer(file)
        writer.writerow(['ссылка', 'название', "рейтинг", "цена"])
    logger.info(f'id:{message.from_user.id} file {uniq_file_name} created')
    # Парсинг
    
    logger.info(f"id:{message.from_user.id} поиск: {user_states[message.from_user.id]['product']} кол-во:{user_states[message.from_user.id]['number']}")
    parser.get_page(user_states[message.from_user.id]["file_name"],
                    user_states[message.from_user.id]["product"],
                    user_states[message.from_user.id]["number"],
                    logger
                    )
    bot.send_message(message.chat.id, "Товары собраны!!!")
    bot.send_message(ADMIN_CHAT_ID, f'Собраны товары: {user_states[message.from_user.id]["product"]}\n'
                                    f'Количество: {user_states[message.from_user.id]["number"]}\n'
                                    f'Пользователь: {message.from_user.first_name} (id:{message.from_user.id})')
    # Отправляем файл в чат
    file = open(uniq_file_name, 'rb')
    bot.send_document(message.chat.id, file)
    logger.info(f"id:{message.from_user.id} файл отправлен")
    # Удаляем файл
    os.remove(uniq_file_name)
    logger.info(f"id:{message.from_user.id} файл удален")


def main():

    logger.info('Бот запущен!')
    # Запуск бота
    bot.polling()


if __name__ == "__main__":
   main()
