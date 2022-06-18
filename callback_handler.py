from functional import *

@bot.callback_query_handler(state=BotStates.greeting, func=lambda call: call.data == "start_questioning")
def first_question(call):
    init_user_table()

    values = {
        'user_id': call.message.chat.id,
        'first_name': call.message.chat.first_name,
        'last_name': call.message.chat.last_name,
        'username': call.message.chat.username
    }
    add_user(call.message.chat.id, values)

    ask_first_question(call.message.chat.id, call.message.id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                              text="Поехали")


# City
@bot.callback_query_handler(state=BotStates.first_question, func=lambda call: call.data == "notChosen")
def no_answer(call):
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                              text="Выберете один из вариантов")


@bot.callback_query_handler(state=BotStates.first_question, func=if_choose_city)
def save_city_answer(call):
    answer = CITY_DECODE_INV[get_first_argument(call.data)]

    new_values = {
        'city': answer
    }

    result = update_user(call.message.chat.id, new_values)

    if result == "Done":
        ask_first_question(call.message.chat.id, call.message.id)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text=f"Выбран ответ {answer}")
    elif result == "Nothing changed":
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Уже выбрано")


@bot.callback_query_handler(state=BotStates.first_question, func=lambda call: call.data == "firstQuestionDone")
def first_question_done(call):
    ask_second_question(call.message.chat.id, call.message.id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                              text="Готово!")


# Risk
@bot.callback_query_handler(state=BotStates.second_question, func=lambda call: call.data == "notChosen")
def no_answer(call):
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                              text="Выберете один из вариантов")


@bot.callback_query_handler(state=BotStates.second_question, func=if_choose_risk)
def save_risk_answer(call):
    answer = RISKS_DECODE_INV[get_first_argument(call.data)]

    new_values = {
        'risks': answer
    }

    result = update_user(call.message.chat.id, new_values)

    if result == "Done":
        ask_second_question(call.message.chat.id, call.message.id)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text=f"Выбран ответ {answer}")
    elif result == "Nothing changed":
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Уже выбрано")


@bot.callback_query_handler(state=BotStates.second_question, func=lambda call: call.data == "backToFirstQuestion")
def back_to_first_question(call):
    ask_first_question(call.message.chat.id, call.message.id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Назад")


@bot.callback_query_handler(state=BotStates.second_question, func=lambda call: call.data == "secondQuestionDone")
def second_question_done(call):
    ask_third_question(call.message.chat.id, call.message.id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                              text="Готово!")


# Number of clinic
@bot.callback_query_handler(state=BotStates.third_question, func=lambda call: call.data == "backToSecondQuestion")
def back_to_second_question(call):
    ask_second_question(call.message.chat.id, call.message.id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Назад")


@bot.message_handler(state=BotStates.third_question)
def save_numclinic_answer(message):
    number_of_clinics = message.text

    if number_of_clinics.isnumeric():
        user_id = message.chat.id

        new_values = {
            'number_of_clinics': number_of_clinics
        }

        result = update_user(user_id, new_values)

        if result == "Done":
            bot.send_message(message.chat.id, f"Готово!")
            forecast_insurance_rate(user_id)
    else:
        bot.send_message(message.chat.id, f"Извините, кол-во клиник должно быть числом")

