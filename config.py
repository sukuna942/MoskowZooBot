import telebot
from telebot import types

BOT_TOKEN = '7111623206:AAEpmJRMq25V8larOJgL2bHEakQrUsqxFSo'

# Список вопросов и ответов викторины
questions = [
    {
        "question": "Какое животное имеет самый большой размах крыльев?",
        "answers": [
            "Альбатрос",
            "Орел",
            "Кондор"
        ],
        "correct_answer": "Альбатрос"
    },
    {
        "question": "Какое животное может прожить дольше всех?",
        "answers": [
            "Слон",
            "Черепаха",
            "Крокодил"
        ],
        "correct_answer": "Черепаха"
    },
    {
        "question": "Какое животное имеет наибольшее количество зубов?",
        "answers": [
            "Крокодил",
            "Акула",
            "Дельфин"
        ],
        "correct_answer": "Крокодил"
    },
    {
        "question": "Какое животное самое быстрое на суше?",
        "answers": [
            "Лев",
            "Гепард",
            "Тигр"
        ],
        "correct_answer": "Гепард"
    },
    {
        "question": "Какое животное имеет самый длинный язык?",
        "answers": [
            "Муравьед",
            "Хамелеон",
            "Жираф"
        ],
        "correct_answer": "Муравьед"
    }
]

# Список животных, которых может выбрать пользователь
animals = [
    {
        "name": "Альбатрос",
        "image_url": "https://example.com/albatross.png"
    },
    {
        "name": "Черепаха",
        "image_url": "https://example.com/turtle.png"
    },
    {
        "name": "Крокодил",
        "image_url": "https://example.com/crocodile.png"
    },
    {
        "name": "Гепард",
        "image_url": "https://example.com/cheetah.png"
    },
    {
        "name": "Муравьед",
        "image_url": "https://example.com/anteater.png"
    }
]

# Словарь для хранения ответов пользователя
user_answers = {}

bot = telebot.TeleBot(BOT_TOKEN)


# Приветственное сообщение
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Давай сыграем в игру и узнаем, какое животное тебе подходит!")
    ask_question(message.chat.id, 0)


# Обработка ответов на вопросы
@bot.message_handler(func=lambda message: message.chat.id in user_answers)
def handle_answers(message):
    chat_id = message.chat.id
    answer = message.text

    if answer in user_answers[chat_id]['answers']:
        user_answers[chat_id]['score'] += 1

    if user_answers[chat_id]['question_number'] < len(questions) - 1:
        ask_question(chat_id, user_answers[chat_id]['question_number'] + 1)
    else:
        get_result(chat_id)


# Запрос вопроса и вариантов ответов
def ask_question(chat_id, question_number):
    question = questions[question_number]
    user_answers[chat_id] = {
        'question_number': question_number,
        'answers': question['answers'],
        'score': 0
    }

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for answer in question['answers']:
        markup.add(types.KeyboardButton(answer))

    bot.send_message(chat_id, question['question'], reply_markup=markup)


# Получение результата викторины
def get_result(chat_id):
    score = user_answers[chat_id]['score']
    animal = animals[score]

    bot.send_message(chat_id, f"Твоё животное: {animal['name']}!")
    bot.send_photo(chat_id, animal['image_url'])

    # Информация о программе опеки
    bot.send_message(chat_id, "Хочешь стать опекуном своего животного?")

    # Кнопка для перехода на программу опеки
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Узнать больше", url="https://www.moscowzoo.ru/care"))

    bot.send_message(chat_id, "Нажми на кнопку ниже, чтобы узнать больше.", reply_markup=markup)

    # Кнопка для связи с сотрудником зоопарка
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton("Связаться с сотрудником"))

    bot.send_message(chat_id, "Если у тебя есть вопросы, нажми на кнопку ниже.", reply_markup=markup)


# Обработка запросов на связь с сотрудником
@bot.message_handler(func=lambda message: message.text == "Связаться с сотрудником")
def contact_staff(message):
    chat_id = message.chat.id

    # Формирование сообщения с данными пользователя
    message_text = f"""
    Имя: {message.from_user.first_name} {message.from_user.last_name}
    ID чата: {chat_id}
    Ответы на викторину: {user_answers[chat_id]}
    """

    # Отправка сообщения сотруднику зоопарка
    bot.send_message("имя_сотрудника_зоопарка", message_text)

    bot.send_message(chat_id, "Спасибо за обращение! Сотрудник зоопарка свяжется с тобой в ближайшее время.")


# Обработка запросов на перезапуск викторины
@bot.message_handler(func=lambda message: message.text == "Попробовать ещё раз?")
def restart_quiz(message):
    user_answers.pop(message.chat.id, None)
    ask_question(message.chat.id, 0)


# Запуск бота
bot.polling()
