import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

from markup import *
from database import *
from additional_functional import *

import pandas as pd
import pickle

TOKEN = "5562863703:AAFYK9UE-Dvy4jX9_vIOW8jg0cN3gzVUqng"

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)


class BotStates(StatesGroup):
    greeting = State(),
    first_question = State(),
    second_question = State(),
    third_question = State(),
    forecast = State()


def start_greeting(chat_id):
    bot.set_state(user_id=chat_id, state=BotStates.greeting, chat_id=chat_id)
    bot.send_message(chat_id=chat_id, text="Привет! Меня я бот компании Alekseev & CO.\n"
                                           "Я могу дать оценку твоему страховому тарифу, "
                                           "но для этого мне нужно узнать тебя получше, ты готов?",
                     reply_markup=start_greeting_markup())

def ask_first_question(chat_id, message_id):
    user_city = get_user_values(chat_id, ['city'])['city']
    bot.set_state(user_id=chat_id, state=BotStates.first_question, chat_id=chat_id)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="[1/3] Из какого ты города?",
                     reply_markup=first_question_markup(CITIES, user_city))

def ask_second_question(chat_id, message_id):
    user_risks = get_user_values(chat_id, ['risks'])['risks']
    bot.set_state(user_id=chat_id, state=BotStates.second_question, chat_id=chat_id)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="[2/3] Какие риски вы хотите включить?",
                     reply_markup=second_question_markup(RISKS, user_risks))


def ask_third_question(chat_id, message_id):
    bot.set_state(user_id=chat_id, state=BotStates.third_question, chat_id=chat_id)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="[3/3] Какое у вас количество клиник?",
                     reply_markup=third_question_markup())


def forecast_insurance_rate(chat_id):
    bot.set_state(user_id=chat_id, state=BotStates.forecast, chat_id=chat_id)
    user_city = get_user_values(chat_id, ['city'])['city']
    user_risks = get_user_values(chat_id, ['risks'])['risks']
    user_num_of_clinics = int(get_user_values(chat_id, ['number_of_clinics'])['number_of_clinics'])

    final_dataset = pd.read_csv('data/final_dataset.csv')

    user_city = CITY_ENCODE[user_city]
    user_risks = RISK_ENCODE[user_risks]

    clinics = final_dataset.number_of_clinics_in_progam.unique()
    num_of_clinics = min(clinics, key=lambda x: abs(x - user_num_of_clinics))

    df = final_dataset[(final_dataset.number_of_clinics_in_progam == num_of_clinics) &
                       (final_dataset.program_city_group == user_city) &
                       final_dataset.service_type_id == user_risks].mean()

    print(user_city, user_risks, num_of_clinics)

    if len(df) != 0:
        loaded_model = pickle.load(open('data/finalized_model.sav', 'rb'))
        loaded_model.predict([df[SELECTED_COLUMNS]])[0]
        score = loaded_model.predict([df[SELECTED_COLUMNS]])[0]

        bot.send_message(chat_id, f"Ваш прогнозируемый тариф: {score}")
    else:
        bot.send_message(chat_id, "Извините, для ваших данных не получается посчитать страховой тариф. "
                                  f"Обратитесь в поддержку.")




bot.add_custom_filter(custom_filters.StateFilter(bot))