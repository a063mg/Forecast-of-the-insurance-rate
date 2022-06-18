from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from additional_functional import *

SELECTED = {True: '✅', False: ''}


def start_greeting_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton("Хочу получить страховой тариф", callback_data="start_questioning",
                                           resize_keyboard=True)
    markup.add(start_button)
    return markup

def first_question_markup(CITIES, user_city):
    markup = InlineKeyboardMarkup(row_width=2)
    button_list = []

    for city in CITIES:
        option_key = CITY_DECODE[city]
        selected = SELECTED[city == user_city]
        workplace_button = InlineKeyboardButton(f"{selected} {city}", callback_data=f"chooseCity-{option_key}",
                                                resize_keyboard=True)
        button_list.append(workplace_button)

    if user_city is None or user_city == []:
        done_button = InlineKeyboardButton("❌ Готово", callback_data="notChosen", resize_keyboard=True)
    else:
        done_button = InlineKeyboardButton("Готово", callback_data="firstQuestionDone", resize_keyboard=True)

    markup.add(*button_list)
    markup.add(done_button)
    return markup


def second_question_markup(RISKS, user_risks):
    markup = InlineKeyboardMarkup(row_width=2)
    button_list = []

    for risk in RISKS:
        option_key = RISKS_DECODE[risk]
        selected = SELECTED[risk == user_risks]
        workplace_button = InlineKeyboardButton(f"{selected} {risk}", callback_data=f"chooseRisk-{option_key}",
                                                resize_keyboard=True)
        button_list.append(workplace_button)

    back_button = InlineKeyboardButton("Назад", callback_data="backToFirstQuestion", resize_keyboard=True)
    if user_risks is None or user_risks == []:
        done_button = InlineKeyboardButton("❌ Готово", callback_data="notChosen", resize_keyboard=True)
    else:
        done_button = InlineKeyboardButton("Готово", callback_data="secondQuestionDone", resize_keyboard=True)

    markup.add(*button_list)
    markup.add(back_button, done_button)
    return markup

def third_question_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton("Назад", callback_data="backToSecondQuestion", resize_keyboard=True)
    markup.add(back_button)
    return markup