# Weather Forcast

Weather forecast page with animated background for a small number of cities selectable at the top of the page.
Using "https://open-meteo.com" as weather service, but taking care not to make too manu calls, 
so the data is stored in local database and updated periodically.

The config file contains translations of weather status messages "WEATHER_CODES" in Serbian, English and Russian language. 
Default is Serbian, so to use English, just go to "en" page like "http://localhost:8000/en".
You can also provide your own translations in the config file.


To install dependencies:

    pip3 install flask flask-sqlalchemy requests

To run:

    export FLASK_APP=weather.py
    export FLASK_ENV=development
    flask run

# Animations
The video material used is freely downloaded from https://pixabay.com and uploaded to a separate repository used as a submodule.
To clone this repo, use:

    git clone https://github.com/ujagaga/weather_forcast.git
    cd weather_forcast
    git submodule update --init
    git submodule update --remote

If you wish to use other videos, just replace files in static/videos/, but make sure to keep the same names.
