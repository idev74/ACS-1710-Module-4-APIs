import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
# from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    city = request.args.get('city')
    units = request.args.get('units')

    params = {
       'appid': API_KEY,
       'q': city,
       'units': units
    }

    result_json = requests.get(API_URL, params=params).json()

    # Uncomment the line below to see the results of the API call!
    pp.pprint(result_json)

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    context = {
        'date': datetime.now(),
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': round(float(result_json['main']['temp']), 2),
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': float(datetime.fromtimestamp(result_json['sys']['sunrise']).strftime('%-H')),
        'sunset': float(datetime.fromtimestamp(result_json['sys']['sunset']).strftime('%-H')),
        'units_letter': get_letter_for_units(units)
    }

    return render_template('results.html', **context)


@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!
    city1_call = {
        'q': city1,
        'units': units,
        'appid': API_KEY
    }

    city2_call = {
        'q': city2,
        'units': units,
        'appid': API_KEY
    }

    city1_results = requests.get(API_URL, params=city1_call).json()
    city2_results = requests.get(API_URL, params=city2_call).json()
    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.

    city1_info = {
        'temp': round(float(city1_results['main']['temp']), 2),
        'humidity': round(float(city1_results['main']['humidity'])),
        'wind_speed': round(float(city1_results['wind']['speed'])),
        'sunrise': int(datetime.fromtimestamp(city1_results['sys']['sunrise']).strftime('%-H')),
        'sunset': int(datetime.fromtimestamp(city1_results['sys']['sunset']).strftime('%-H')),
    }

    city2_info = {
        'temp': round(float(city2_results['main']['temp']), 2),
        'humidity': round(float(city2_results['main']['humidity'])),
        'wind_speed': round(float(city2_results['wind']['speed'])),
        'sunrise': round(int(datetime.fromtimestamp(city2_results['sys']['sunrise']).strftime('%-H'))),
        'sunset': round(int(datetime.fromtimestamp(city2_results['sys']['sunset']).strftime('%-H'))),
    }

    context = {
        'date': datetime.now(),
        'city1': city1_results['name'],
        'city2': city2_results['name'],
        'city1_info': city1_info,
        'city2_info': city2_info,
        'units_letter': get_letter_for_units(units)
    }

    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
