import datetime
import json
import os
import requests

from todolist.models import Weather


# Fetch Weather data
# Uses recent database data if possible, fetches from Weather API if database data is old or doesn't exist
def fetch_weather(location):
    recent_reads = Weather.objects.filter(modified_at__gte=(datetime.datetime.now() - datetime.timedelta(minutes=10)))
    if (
            # The location already has a temperature read
            hasattr(location, 'weather') and
            # The temperature read is from the last 10 minutes
            location.weather in recent_reads
    ):
        data = {
            'temp': location.weather.temperature,
            'weather': location.weather.status
        }
    else:
        # Fetch temperature read from API
        data = request_weather(location)
        # Store the new read
        if hasattr(location, 'weather'):
            # If the location already had a temperature read
            location.weather.temperature = data['temp']
            location.weather.status = data['weather']
        else:
            # If this is the first read for this location
            Weather.objects.create(location=location, temperature=data['temp'], status=data['weather'])

    return data


# Fetch weather data from weather API
def request_weather(location):
    url = (
            os.getenv('WEATHER_API') + os.getenv('WEATHER_API_ONECALL') +
            'lat=' + str(location.lat) +
            '&lon=' + str(location.lon) +
            '&appid=' + os.getenv('WEATHER_API_KEY') +
            '&units=metric'
    )

    response = requests.get(url)
    data = json.loads(response.text)
    temp = data['main']['temp']

    atmospheric_particles = parse_weather(data['weather'])
    temperature = parse_temp(temp)
    can_be_sunny = is_daytime(data)
    result = rate_weather(atmospheric_particles, temperature, can_be_sunny)

    return {
        'temp': temp,
        'weather': result
    }


# Parse weather conditions data
def parse_weather(weather):
    clouds = False
    for read in weather:
        weather_id = read['id']
        # if at least a single weather report tells it's raining then it's raining
        if 200 <= weather_id < 700:
            return 'rain'
        # update flag for cloudy weather, keep on rolling because rain trumps all
        if weather_id >= 700 and weather_id != 800:
            clouds = True

    # it's not rainy, check if there were any clouds, it's cloudy if at least one report spotted clouds
    # otherwise the sky is clear
    return ('cloudy', 'clear')[clouds]


# Parse temperature readings data
def parse_temp(temp):
    if temp < 17:
        return 'cold'
    if temp < 25:
        return 'warm'

    return 'hot'


# Parse reading time data to check whether the read was during daytime
def is_daytime(data):
    read_time = data['dt']
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']

    return sunrise <= read_time <= sunset


# Rate the weather data reads to consider what type of weather it is
def rate_weather(particles, temperature, can_be_sunny):
    # If it rains, or it's cold - it's bad
    if particles == 'rain' or temperature == 'cold':
        return 'bad'
    # If it wasn't raining, it wasn't cold, but it's cloudy or just warm - it's average
    if particles == 'cloudy' or temperature == 'warm':
        return 'average'
    # it wasn't raining, it wasn't cloudy, the temperature was not cold or just warm, so if it's day, it's a good day
    if can_be_sunny:
        return 'good'

    # not rainy, not cloudy, not cold, not just warm, but it's night, so it's not sunny
    return 'average'
