SELECTED_COLUMNS = ['cpr_max', 'cpr_mean', 'cpr_median', 'analysis_copro_avg_max',
       'analysis_copro_avg_min', 'massage_avg_mean', 'usound_ginec_avg_mean',
       'usound_shield_avg_max', 'visit_gastr_avg_mean', 'visit_lor_avg_max',
       'visit_lor_avg_mean', 'visit_neur_avg_max', 'visit_neur_avg_mean',
       'visit_neuro_avg_max', 'visit_oft_avg_max', 'visit_oft_avg_mean']

CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Краснодар", "Нижний-Новгород", "Воронеж"]
CITY_DECODE = {"Москва": "Moscow", "Санкт-Петербург": "SaintP", "Новосибирск": "Novosib",
               "Краснодар": "Redcity", "Нижний-Новгород": "Downewcity", "Воронеж": "Voronezh"}

RISKS = ["Поликлиника", "Стоматология"]
RISKS_DECODE = {"Поликлиника": "polyclinic", "Стоматология": "Dentist"}

CITY_ENCODE = {"Москва": 2., "Санкт-Петербург": 1.6, "Новосибирск": 1.8, "Краснодар": 1.4, "Нижний-Новгород": 1.2, "Воронеж": 1.}
RISK_ENCODE = {"Поликлиника": 1, "Стоматология": 2}

def inverse_dict(my_map):
    return {v: k for k, v in my_map.items()}


CITY_DECODE_INV = inverse_dict(CITY_DECODE)
RISKS_DECODE_INV = inverse_dict(RISKS_DECODE)

def if_choose_city(query):
    return query.data.startswith("chooseCity")

def if_choose_risk(query):
    return query.data.startswith("chooseRisk")

def get_first_argument(data):
    return data.split("-")[1]