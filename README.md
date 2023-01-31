# Weather Forcast

Weather forecast page with animated background for a single city.
Before you start, please create an account on https://www.weatherbit.io and make note of your API key. 
Then replace it in the config file. 
The config file contains translations of weather status messages "WEATHER_CODES" in Serbian language. 
If you wish to just use English as is default, set the "USE_WEATHER_CODES" variable to False. 
This is also applied when using "/en" page. 
You can also provide your own translations.
Same goes for error messages.


To install dependencies:

    pip install flask flask-sqlalchemy requests

To run:

    flask --app weather run --host 0.0.0.0 --reload

# Animations

The video material used is freely downloaded from https://www.pexels.com/. 
If you wish to use other, just replace files in static/videos/, but make sure to keep the same names.