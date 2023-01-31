WEATHER_API_KEY = "your weatherbit.io API key here"
WEATHER_API_URL = "http://api.weatherbit.io/v2.0/current"
WEATHER_ICON_URL = "https://www.weatherbit.io/static/img/icons"
city_ids = {
    "NOVI SAD": "3194360",
    "VELIKA PLANA": "784630",
    "KIKINDA": "789518"
}
DEFAULT_CITY = "NOVI SAD"
WEATHER_NOT_READABLE_SECONDS = (60 * 30)
WEATHER_FORCAST_API_URL = "https://api.weatherbit.io/v2.0/forecast/daily"
USE_TRANSLATIONS = True

WEATHER_CODES = {
    200: "Grmljavina sa slabom kišom",
    201: "Grmljavina sa kišom",
    202: "Grmljavina sa obilnom kišom",
    230: "Grmljavina sa slabom kišom",
    231: "Grmljavina sa slabom kišom",
    232: "Grmljavina sa kišom",
    233: "Grmljavina sa gradom",
    300: "Slaba kiša",
    301: "Slaba kiša",
    302: "Obilna kiša",
    500: "Slaba kiša",
    501: "Umerena kiša",
    502: "Obilna kiša",
    511: "Ledena kiša",
    520: "Slabiji pljusak",
    521: "Pljusak",
    522: "Obilni pljusak",
    600: "Slab sneg",
    601: "Sneg",
    602: "Jak sneg",
    610: "Sneg sa kišom",
    611: "Bljuzgavica",
    612: "Obilna bljuzgavica",
    621: "Mećava",
    622: "Jaka mećava",
    623: "Jaka mećava",
    700: "Slaba magla",
    711: "Smog",
    721: "Sumaglica",
    731: "Pesak/prašina",
    741: "Magla",
    751: "Ladena magla",
    800: "Vedro",
    801: "Poneki oblak",
    802: "Rasuti oblaci",
    803: "Pretežno oblačno",
    900: "Nepoznate padavine"
}

ERROR_MESSAGES = {
    "Daily limit reached. Try again tomorrow.": "Dnevna granica dostignuta. Pokušajte sutra.",
    "Error acquiring weather data": "Greska u prikupljanju podataka"
}

CUSTOM_LANG = {
    "Feels like": "Osećaj"
}