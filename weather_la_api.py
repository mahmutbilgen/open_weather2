import datetime
import json
import urllib.request


def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


def url_builder(city_id):
    user_api_key = 'bbb1a0a0dfcd60d4ed0bcc32f6cd12d1'  # Obtained from: http://openweathermap.org/
    # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    unit = 'metric'
    # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
    api = 'http://api.openweathermap.org/data/2.5/weather?id='
    '''    
        "id": 5368361,"name": "Los Angeles", "country": "US","coord": {"lon": -118.243683,"lat": 34.052231}
    '''
    full_api_url = api + str(city_id) + \
        '&mode=json&units=' + unit + '&APPID=' + user_api_key
    return full_api_url

def data_fetch(full_api_url):
    with urllib.request.urlopen(full_api_url) as url:
      return json.loads(url.read().decode('utf-8'))

def data_organizer(raw_data):
    main = raw_data.get('main')
    sys = raw_data.get('sys')
    data = dict(
        city=raw_data.get('name'),
        country=sys.get('country'),
        temp=main.get('temp'),
        temp_max=main.get('temp_max'),
        temp_min=main.get('temp_min'),
        humidity=main.get('humidity'),
        pressure=main.get('pressure'),
        sky=raw_data['weather'][0]['main'],
        sunrise=time_converter(sys.get('sunrise')),
        sunset=time_converter(sys.get('sunset')),
        wind=raw_data.get('wind').get('speed'),
        wind_deg=raw_data.get('deg'),
        dt=time_converter(raw_data.get('dt')),
        cloudiness=raw_data.get('clouds').get('all'),
        date_today = datetime.date.today()
    )
    return data

#
def data_writer(data):

    data['m_symbol'] = '\xb0' + 'C'
    s = '''---------------------------------------
Current Date : {date_today}
Current weather in: {city}, {country}:
{temp}{m_symbol} {sky}
Max: {temp_max}, Min: {temp_min}

Wind Speed: {wind}, Degree: {wind_deg}
Humidity: {humidity}
Cloud: {cloudiness}
Pressure: {pressure}
Sunrise at: {sunrise}
Sunset at: {sunset}

Last update from the server: {dt}
---------------------------------------'''
    print(s.format(**data))


if __name__ == '__main__':
    try:
        data_writer(
            data_organizer(
                data_fetch(
                    url_builder(5368361))))
    except IOError:
        print('internet connection issue')
