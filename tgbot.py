import telebot
from telebot import types
from parcer import find_vacancies_by_name
from database import get_vacancies_by_filter, delete_vacancies_by_user_id

import time
import os
from dotenv import load_dotenv

load_dotenv()


bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))


name = None
starting_salary = None
max_salary = None
city = None


def ask_name(message):
    global name  
    global user_id
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Какую вакансию Вы ищете?")
    bot.register_next_step_handler(message, lambda message: process_vacancy(message, user_id))


def process_vacancy(message, user_id):
    global name  
    name = message.text  
    ask_starting_salary(message)
    find_vacancies_by_name(name, user_id)


def ask_starting_salary(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('/skip'))
    bot.send_message(message.chat.id, "Какой должна быть минимальная зарплата?\nПример ответа: 100000.\nДанный вопрос можно пропустить, нажав на кнопку '/skip'", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: set_starting_salary(m) if m.text != '/skip' else ask_max_salary(m))


def set_starting_salary(message):
    global starting_salary
    starting_salary = int(message.text)
    ask_max_salary(message)


def ask_max_salary(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('/skip'))
    bot.send_message(message.chat.id, "Какой должна быть максимальная зарплата?\nПример ответа: 320000.\nДанный вопрос можно пропустить, нажав на кнопку '/skip'", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: set_max_salary(m) if m.text != '/skip' else ask_city(m))


def set_max_salary(message):
    global max_salary
    max_salary = int(message.text)
    ask_city(message)


def ask_city(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('/skip'))
    bot.send_message(message.chat.id, "В каком городе Вы ищете вакансии?\nПример ответа: Тбилиси.\nДанный вопрос можно пропустить, нажав на кнопку '/skip'", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: set_city(m) if m.text != '/skip' else process_results(m))


def set_city(message):
    global city
    city = message.text
    process_results(message)


def process_results(message):
    bot.send_message(message.chat.id, "Результаты обрабатываются, пожалуйста, дождитесь получения ответа.")
    time.sleep(5)  # Ожидание в 5 секунд нужно, чтобы все вакансии успели записаться в БД
    vacancies = send_results()
    if vacancies:
        response_message = "Вот список вакансий:\n"
        buttons = []
        for index, vacancy in enumerate(vacancies, start=1):
            vacancy_id = vacancy['id'].split('/')[-1]  # Получение только цифр из ссылки на вакансию
            response_message += f"{index}) {vacancy['vacancy_name']} - {vacancy['salary_from']}-{vacancy['salary_to']} {vacancy['currency']} - {vacancy['city']} - {vacancy_id}\n"
            buttons.append(types.KeyboardButton(str(index)))
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*buttons)
        response_message += "Выберите номер вакансии, чтобы получить подробную информацию о ней"
        bot.send_message(message.chat.id, response_message, reply_markup=markup)
        bot.register_next_step_handler(message, lambda message: handle_vacancy_choice(message, vacancies))
    else:
        bot.send_message(message.chat.id, "Подобных вакансий не было найдено")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("Попробовать ещё раз?"))
        bot.send_message(message.chat.id, "Нажмите кнопку, чтобы найти ещё вакансии", reply_markup=markup)
        bot.register_next_step_handler(message, ask_name_again)


def ask_name_again(message):
    ask_name(message)


def handle_vacancy_choice(message, vacancies):
    selected_index = int(message.text)
    if selected_index <= len(vacancies):
        selected_vacancy = vacancies[selected_index - 1]
        detailed_info = f"Подробная информация о выбранной вакансии:\n" \
                        f"Название: {selected_vacancy['vacancy_name']}\n" \
                        f"Зарплата: {selected_vacancy['salary_from']}-{selected_vacancy['salary_to']} {selected_vacancy['currency']}\n" \
                        f"Город: {selected_vacancy['city']}\n" \
                        f"Станция метро: {selected_vacancy['metro_station']}\n" \
                        f"Ссылка: {selected_vacancy['id']}\n"
        bot.send_message(message.chat.id, detailed_info)
        delete_vacancies_by_user_id(user_id)
    else:
        bot.send_message(message.chat.id, "Выберите корректный номер вакансии")


def send_results():
    vacancies = get_vacancies_by_filter(user_id, starting_salary, max_salary, city)
    return vacancies


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Информация о боте")
    button2 = types.KeyboardButton("Поиск вакансий")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Добро пожаловать! Это бот-парсер вакансий на hh.ru, выберете дальнейшее действие', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "Информация о боте":
        bot.send_message(message.chat.id, 'Данный бот создан для прохождения летней практики второго курса студентом МТУСИ.\nС его помощью можно найти информацию о доступных вакансия на сайте hh.ru.')
    elif message.text == "Поиск вакансий":
        ask_name(message)  

bot.infinity_polling()
