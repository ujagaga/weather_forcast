WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
LOCATIONS = {
    "Novi Sad": {"latitude": "45.26", "longitude": "19.82"},
    "Velika Plana": {"latitude": "44.33", "longitude": "21.07"},
    "Kikinda": {"latitude": "45.83", "longitude": "20.48"},
    "Beograd": {"latitude": "44.78", "longitude": "20.47"},
}
DEFAULT_CITY = "Novi Sad"
WEATHER_NOT_READABLE_SECONDS = (60 * 30)
TODAY_MAX_HOURS = 25     # 24 hours max display plus current hour
DEFAULT_PARMS = {
    "latitude": "45.26",
    "longitude": "19.82",
    "hourly": "temperature_2m,weathercode,precipitation",
    "timezone": "auto",
    "daily": 'weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset'
}

LANGS = ["en", "sr", "ru"]
DEFAULT_LANG = "sr"

WEATHER_CODES = {
    0: {"en": "Clear sky", "sr": "Vedro", "ru": "Ясно", "icon": "c01"},
    1: {"en": "Mainly clear", "sr": "Uglavnom vedro", "ru": "Преимущественно ясное", "icon": "c02"},
    2: {"en": "Partly cloudy", "sr": "Delimično oblačno", "ru": "Переменная облачность", "icon": "c03"},
    3: {"en": "Overcast", "sr": "Oblačno", "ru": "Пасмурно", "icon": "c04"},
    45: {"en": "Fog", "sr": "Magla", "ru": "Туман", "icon": "a01"},
    48: {"en": "Depositing rime fog", "sr": "Taloženje magle", "ru": "Изморось", "icon": "a01"},
    51: {"en": "Light drizzle", "sr": "Slaba kiša", "ru": "Легкая морось", "icon": "d01"},
    53: {"en": "Moderate drizzle", "sr": "Umerena kiša", "ru": "Умеренная морось", "icon": "d01"},
    55: {"en": "Dense drizzle", "sr": "Gusta kiša", "ru": "Густая морось", "icon": "d01"},
    56: {"en": "Light freezing drizzle", "sr": "Slaba ledena kiša", "ru": "Легкая ледяная морось", "icon": "d01"},
    57: {"en": "Dense freezing drizzle", "sr": "Gusta ledena kiša", "ru": "Густая ледяная морось", "icon": "d01"},
    61: {"en": "Slight rain", "sr": "Slaba kiša", "ru": "Слабый дождь", "icon": "r01"},
    63: {"en": "Moderate rain", "sr": "Umerena kiša", "ru": "Умеренный дождь", "icon": "r01"},
    65: {"en": "Heavy rain", "sr": "Jaka kiša", "ru": "Сильный дождь", "icon": "r01"},
    66: {"en": "Light freezing rain", "sr": "Slaba ledena kiša", "ru": "Слабый ледяной дождь", "icon": "f01"},
    67: {"en": "Heavy freezing rain", "sr": "Jaka ledena kiša", "ru": "Сильный ледяной дождь", "icon": "f01"},
    71: {"en": "Slight snow", "sr": "Slab sneg", "ru": "Небольшой снег", "icon": "s01"},
    73: {"en": "Moderate snow", "sr": "Umeren sneg", "ru": "Умеренный снег", "icon": "s01"},
    75: {"en": "Heavy snow", "sr": "Gust sneg", "ru": "Сильный снег", "icon": "s01"},
    77: {"en": "Snow grains", "sr": "Ledeni sneg", "ru": "Снежная крупа", "icon": "s01"},
    80: {"en": "Slight rain showers", "sr": "Laki pljuskovi", "ru": "Слабые ливневые дожди", "icon": "r01"},
    81: {"en": "Moderate rain showers", "sr": "Umereni pljuskovi", "ru": "Умеренные ливневые дожди", "icon": "r01"},
    82: {"en": "Violent rain showers", "sr": "Jaki pljuskovi", "ru": "Сильные ливневые дожди", "icon": "r02"},
    85: {"en": "Slight snow showers", "sr": "Slab sneg", "ru": "Слабый ливневый снег", "icon": "s01"},
    86: {"en": "Heavy snow showers", "sr": "Jak sneg", "ru": "Сильный ливневый снег", "icon": "s01"},
    95: {"en": "Thunderstorm", "sr": "Grmljavina", "ru": "Гроза", "icon": "t01"},
    96: {"en": "Thunderstorm with slight hail", "sr": "Grmljavina sa slabim gradom", "ru": "Гроза с небольшим градом", "icon": "t02"},
    99: {"en": "Thunderstorm with heavy hail", "sr": "Grmljavina sa jakim gradom", "ru": "Гроза с сильным градом", "icon": "t02"},
}

WEEK_DAYS = {
    0: {"en": "Monday", "sr": "Ponedeljak", "ru": "Понедельник"},
    1: {"en": "Tuesday", "sr": "Utorak", "ru": "Вторник"},
    2: {"en": "Wednesday", "sr": "Sreda", "ru": "Среда"},
    3: {"en": "Thursday", "sr": "Četvrtak", "ru": "Четверг"},
    4: {"en": "Friday", "sr": "Petak", "ru": "Пятница"},
    5: {"en": "Saturday", "sr": "Subota", "ru": "Суббота"},
    6: {"en": "Sunday", "sr": "Nedelja", "ru": "Воскресенье"}
}
