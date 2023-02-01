# -*- coding: utf-8 -*-

from flask import Flask, g, render_template, request
import json
from datetime import datetime
import sys
import requests
import config
import sqlite3
import os


db_path = "database.db"
application = Flask(__name__, static_url_path='/static', static_folder='static')

application.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopOqwerty'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


def init_database():
    if not os.path.isfile(db_path):
        # Database does not exist. Create one
        db = sqlite3.connect(db_path)

        sql = "create table data (data_key TEXT, data_value TEXT, timestamp INTEGER)"
        db.execute(sql)
        db.commit()

        db.close()


def query_db(db, query, args=(), one=False):
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def exec_db(query):
    g.db.execute(query)
    if not query.startswith('SELECT'):
        g.db.commit()


def read_general_data(data_key):
    data = None

    try:
        sql = "SELECT * FROM data WHERE data_key = '{}'".format(data_key)
        data = query_db(g.db, sql, one=True)
    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ERROR reading data on line {}!\n\t{}".format(exc_tb.tb_lineno, exc), flush=True)

    if data is not None:
        try:
            data_value = json.loads(data["data_value"])
        except:
            data_value = data["data_value"]

        return {"value": data_value, "timestamp": data["timestamp"]}
    else:
        return None


def update_general_data(data_key, data_value):
    try:
        data = read_general_data(data_key)

        if data is None:
            sql = f"INSERT INTO data (data_key, data_value, timestamp) " \
                  f"VALUES ('{data_key}', '{data_value}', '{int(datetime.now().timestamp())}')"
        else:
            sql = f"UPDATE data SET data_value = '{data_value}', timestamp = '{int(datetime.now().timestamp())}' " \
                  f"WHERE data_key = '{data_key}'"
        exec_db(sql)

    except Exception as exc:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("ERROR writing data to db on line {}!\n\t{}".format(exc_tb.tb_lineno, exc), flush=True)


def translate_weather_status(status_code, default_message, use_translation=config.USE_TRANSLATIONS):
    if use_translation:
        return config.WEATHER_CODES.get(status_code, default_message)
    else:
        return default_message


def translate_error_message(error_message, use_translation=config.USE_TRANSLATIONS):
    if use_translation:
        return config.ERROR_MESSAGES.get(error_message, error_message)
    else:
        return error_message


def translate_custom_message(message, use_translation=config.USE_TRANSLATIONS):
    if use_translation:
        return config.CUSTOM_LANG.get(message, message)
    else:
        return message


def get_weather_forcast(city_name: str = config.DEFAULT_CITY, max_days: int = 3, use_translation=config.USE_TRANSLATIONS) -> dict:
    city_id = config.city_ids.get(city_name.upper(), "3194360")

    url_params = {'key': config.WEATHER_API_KEY, 'city_id': city_id, 'lang': 'en'}
    r = requests.get(config.WEATHER_FORCAST_API_URL, params=url_params)
    status = "ERROR"

    try:
        if r.status_code == 200:
            json_ret_val = json.loads(r.text)
            detail = []
            for item in json_ret_val['data']:
                item_date = datetime.strptime(item["valid_date"], '%Y-%m-%d')
                days_ahead = (item_date - datetime.now()).days

                if days_ahead < max_days:
                    item_data = {
                        "date": item_date.strftime("%d.%m."),
                        "avg_temp": item["temp"],
                        "max_temp": item["high_temp"],
                        "min_temp": item["low_temp"],
                        "app_min_temp": item["app_min_temp"],
                        "app_max_temp": item["app_max_temp"],
                        "icon": item["weather"]["icon"],
                        "probabillity": item["pop"]
                    }
                    detail.append(item_data)

            status = "OK"

        else:
            status_code = r.status_code
            status_msg = r.text
            if status_code == 429:
                status_msg = translate_error_message(
                    "Daily limit reached. Try again tomorrow.", use_translation=use_translation)
            detail = {"code": status_code, "message": status_msg}
    except Exception as e:
        detail = {"code": "", "message": f"ERROR: {e}"}

    return {"status": status, "detail": detail}


def get_current_weather(city_name: str = config.DEFAULT_CITY, use_translation=config.USE_TRANSLATIONS) -> dict:
    city_id = config.city_ids.get(city_name.upper(), "3194360")

    url_params = {'key': config.WEATHER_API_KEY, 'city_id': city_id, 'lang': 'en'}
    r = requests.get(config.WEATHER_API_URL, params=url_params)
    status = "ERROR"
    try:
        if r.status_code == 200:
            json_ret_val = json.loads(r.text)
            data = json_ret_val['data'][0]
            temp = data['temp']
            weather = data['weather']
            # description = translate_weather_status(status_code=weather['code'], default_message=weather['description'], use_translation=use_translation)
            description = weather['description']
            weather_code = weather['code']
            temp_str = f"{temp}".replace('.', ',')
            status = "OK"

            detail = {
                "city": data["city_name"],
                "weather": description,
                "temp": temp_str,
                "wind_spd": data["wind_spd"],
                "temp_feel": data["app_temp"],
                "cloud_coverage": data["clouds"],
                "part_of_day": data["pod"],
                "time": data["ob_time"],
                "weather_code": weather_code,
                "weather_icon": weather['icon']
            }

        else:
            status_code = r.status_code
            status_msg = r.text
            if status_code == 429:
                status_msg = translate_error_message(
                    "Daily limit reached. Try again tomorrow.", use_translation=use_translation)
            detail = {"code": status_code, "message": status_msg}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        detail = {"code": "", "message": f"ERROR: {e}. LINE:{exc_tb.tb_lineno}"}

    return {"status": status, "detail": detail}


@application.before_request
def before_request():
    if not os.path.isfile(db_path):
        init_database()

    g.db = sqlite3.connect(db_path)


@application.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@application.route('/', methods=['GET'])
def index(use_translation=config.USE_TRANSLATIONS):

    weather_msg = translate_error_message("Error acquiring weather data", use_translation=use_translation)
    display_temp = ""
    temperature = ""
    icon = ""
    icon_location = config.WEATHER_ICON_URL
    city = config.DEFAULT_CITY
    db_current_weather_data = read_general_data(data_key="current_weather")

    proceed = True
    if db_current_weather_data is not None:
        if datetime.now().timestamp() - db_current_weather_data["timestamp"] < config.WEATHER_NOT_READABLE_SECONDS:
            proceed = False
        else:
            status = db_current_weather_data["value"]["status"]
            if "ERR" in status:
                proceed = False

    if proceed:
        weather = get_current_weather(city_name=config.DEFAULT_CITY)
        update_general_data(data_key="current_weather", data_value=json.dumps(weather))
    else:
        weather = db_current_weather_data["value"]

    current_weather_status = weather.get("status", "ERR")
    if "OK" in current_weather_status:
        try:
            data = weather["detail"]
            city = data["city"]
            weather_msg = translate_weather_status(status_code=data['weather_code'], default_message=data['weather'], use_translation=use_translation)
            display_temp = data['temp']
            temperature = f"{translate_custom_message('Feels like', use_translation=use_translation)}: " \
                          f"{data['temp_feel']}{chr(176)}C"
            icon = data["weather_icon"]

        except Exception as e:
            print(f"ERROR parsing weather data: {e}", flush=True)
    else:
        print(f"ERROR reading weather data: {weather}")
        weather_msg = weather["detail"]["message"]

    # Weather forcast
    db_weather_forcast_data = read_general_data(data_key="future_weather")
    proceed = True
    if db_weather_forcast_data is not None:
        if datetime.now().timestamp() - db_weather_forcast_data["timestamp"] < config.WEATHER_NOT_READABLE_SECONDS:
            proceed = False
        else:
            status = db_weather_forcast_data["value"]["status"]
            if "ERR" in status:
                proceed = False

    if proceed:
        weather_forcast = get_weather_forcast(city_name=config.DEFAULT_CITY)
        update_general_data(data_key="future_weather", data_value=json.dumps(weather_forcast))
    else:
        weather_forcast = db_weather_forcast_data["value"]

    forcast_weather_status = weather_forcast.get("status", "ERR")
    if "OK" in forcast_weather_status:
        forcast_data = weather_forcast["detail"]
        weather_forcast_msg = None
    else:
        print(f"ERROR reading weather forcast: {weather_forcast}")
        weather_forcast_msg = weather_forcast["detail"]["message"]
        forcast_data = []

    return render_template(
        'weather.html',
        city=city,
        weather_msg=weather_msg,
        display_temp=display_temp,
        temperature=temperature,
        icon=icon,
        icon_location=icon_location,
        weather_forcast_msg=weather_forcast_msg,
        forcast_data=forcast_data
    )


@application.route('/en', methods=['GET'])
def index_en():
    return index(use_translation=False)
