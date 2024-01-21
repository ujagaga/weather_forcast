# -*- coding: utf-8 -*-

from flask import Flask, g, render_template, request
import json
import sys
import requests
import config
import sqlite3
import os
import urllib.parse
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))

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


def read_db_data(data_key):
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


def update_db_data(data_key: str, data_value: str):
    try:
        data = read_db_data(data_key)

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


def get_weather_status(status_code, lang=config.DEFAULT_LANG):
    data = config.WEATHER_CODES.get(status_code, None)
    if data is None:
        return "ERR: No such weather code."
    else:
        return data.get(lang, "ERR: No description available.")


def get_weather_forcast(city_name: str = config.DEFAULT_CITY) -> dict:
    if city_name not in config.LOCATIONS.keys():
        city_name = config.DEFAULT_CITY
    city = config.LOCATIONS.get(city_name)
    if city is None:
        return {"status": "ERROR", "detail": "No valid city specified"}

    url_params = config.DEFAULT_PARMS
    url_params["latitude"] = city["latitude"]
    url_params["longitude"] = city["longitude"]

    payload_str = urllib.parse.urlencode(url_params, safe=',')
    r = requests.get(config.WEATHER_API_URL, params=payload_str)
    status = "ERROR"

    try:
        if r.status_code == 200:
            json_ret_val = json.loads(r.text)

            hourly_data = json_ret_val["hourly"]
            daily_data = json_ret_val["daily"]

            now = datetime.now()
            today_info = {}

            forcast_data = []

            for i in range(0, len(daily_data["time"])):
                item_date = datetime.strptime(daily_data["time"][i], '%Y-%m-%d')
                weather_code = daily_data["weathercode"][i]
                temp_min = daily_data["temperature_2m_min"][i]
                temp_max = daily_data["temperature_2m_max"][i]

                icon_name = None
                description = config.WEATHER_CODES.get(weather_code, None)

                if item_date.date() == datetime.now().date():
                    day_name = config.WEEK_DAYS[item_date.weekday()]

                    today_info = {
                        "day": day_name,
                        "temp_min": temp_min,
                        "temp_max": temp_max,
                        "sunrise": daily_data["sunrise"][i],
                        "sunset": daily_data["sunset"][i],
                    }
                else:
                    if description is not None:
                        icon_name = f"{description['icon']}d"

                    forcast_data.append({
                        "day": item_date.weekday(),
                        "date": f"{ item_date.day }.{ item_date.month }",
                        "temp_min": int(temp_min + 0.5),
                        "temp_max": int(temp_max + 0.5),
                        "icon_name": icon_name,
                    })

            today_data = []

            start_time = now - timedelta(hours=1)
            end_time = start_time + timedelta(hours=config.TODAY_MAX_HOURS)

            for i in range(0, len(hourly_data["time"])):
                item_time = datetime.strptime(hourly_data["time"][i], '%Y-%m-%dT%H:%M')
                if start_time <= item_time <= end_time:

                    temperature = hourly_data["temperature_2m"][i]
                    weather_code = hourly_data["weathercode"][i]
                    description = config.WEATHER_CODES.get(weather_code, None)
                    precipitation = hourly_data["precipitation"][i]

                    if description is not None and today_info is not None:
                        sunrise = datetime.strptime(today_info["sunrise"], '%Y-%m-%dT%H:%M')
                        sunset = datetime.strptime(today_info["sunset"], '%Y-%m-%dT%H:%M')

                        if sunrise.time() < item_time.time() < sunset.time():
                            icon_name = f"{description['icon']}d"
                        else:
                            icon_name = f"{description['icon']}n"

                        if item_time.replace(minute=0) <= now < (item_time.replace(minute=0) + timedelta(hours=1)):
                            today_info["weather_code"] = weather_code
                            today_info["icon_name"] = icon_name
                            today_info["temp"] = int(temperature + 0.5)
                        else:
                            interval_data = {
                                "hour": item_time.hour,
                                "temp": temperature,
                                "icon_name": icon_name,
                                "prec": precipitation,
                                "wc": weather_code
                            }
                            today_data.append(interval_data)

            detail = {"city_name": city_name, "today_info": today_info, "hourly": today_data, "daily": forcast_data}

            status = "OK"

        else:
            json_ret_val = json.loads(r.text)
            detail = {"code": r.status_code, "message": json_ret_val["reason"]}
    except Exception as e:
        detail = {"code": "", "message": f"ERROR: {e}"}

    return {"status": status, "detail": detail}


def translate_weekdays(lang):
    weekdays = {}
    try:
        for day_number in config.WEEK_DAYS.keys():
            day_object = config.WEEK_DAYS.get(day_number, {})
            day_name = day_object.get(lang, "")
            weekdays[day_number] = day_name
    except:
        pass

    return weekdays


def translate_forcast_message(forcast, lang):
    forcast["today_info"]["description"] = ""
    try:
        weather_code = forcast["today_info"]["weather_code"]
        description_data = config.WEATHER_CODES[weather_code]
        forcast["today_info"]["description"] = description_data[lang]
    except:
        pass

    return forcast


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
@application.route('/<lang>', methods=['GET'])
def index(lang=config.DEFAULT_LANG, city_name=config.DEFAULT_CITY):
    if lang not in config.LANGS:
        return "Not found", 404
    error_message = None

    city_name = request.args.get('city_name', city_name)

    animate = request.args.get("animate", "yes")
    if animate == "yes":
        template_name = 'weather.html'
    else:
        template_name = 'simple.html'

    db_current_weather_data = read_db_data(data_key=city_name)

    read_api_data_flag = True
    if db_current_weather_data is not None:
        if datetime.now().timestamp() - db_current_weather_data["timestamp"] < config.WEATHER_NOT_READABLE_SECONDS:
            weather = db_current_weather_data["value"]
            read_api_data_flag = False

    if read_api_data_flag:
        weather = get_weather_forcast(city_name=city_name)
        if "OK" in weather['status']:
            city_name = weather["detail"]["city_name"]
            weather_info = json.dumps(weather)
            update_db_data(data_key=city_name, data_value=weather_info)

    weather_status = weather.get("status", "ERROR")
    if "OK" in weather_status:
        forcast_data = weather["detail"]
        error_message = error_message
    else:
        print(f"ERROR reading weather forcast: {weather}")
        error_message = weather["detail"]["message"]
        forcast_data = None

    return render_template(
        template_name,
        locations=config.LOCATIONS.keys(),
        error_message=error_message,
        forcast_data=translate_forcast_message(forcast_data, lang),
        weekdays=translate_weekdays(lang)
    )
