# weather.py
#
# ICS 32A Fall 2023
# Project 3: From the Faraway Nearby

'''
This module contains the functions that uses National Weather Service API 
to return information regarding weather forcast.
'''

import json
import urllib.parse
import urllib.request
from urllib.error import HTTPError
import geocoding
import os
from datetime import datetime, timedelta

BASE_NWS_URL = 'https://api.weather.gov'

# Class Api contains methods that get information directly through the NWS api.
class Api:
    def __init__(self, coordinates: tuple):
        ''' 
        Takes in the coordinate of the location that the user 
        wants to get forcast for.
        '''
        self._coordinates = coordinates

    def get_hourly_forcast(self) -> dict:
        '''
        Given the coordiates, create the hourly forcast url according to the api,
        then return the hourly forcast as a dictionary (json text).
        '''
        location = self._coordinates[0] + ',' + self._coordinates[1]
        try:
            result = _get_result(f'{BASE_NWS_URL}/points/{location}')
        except:
            print('FAILED')
            print(f'{BASE_NWS_URL}/points/{location}')
            print('NETWORK')
            exit()

        forcast_hourly = _get_result(result['properties']['forecastHourly'])

        return forcast_hourly
    

    def get_temperature(forcast: dict) -> list:
        '''
        Take in the forcast dictionary, store all the hourly temperatures (in Fahrenheit) 
        into a list and return the list.
        '''
        temperatures = []

        for item in forcast['properties']['periods']:
            temperatures.append(int(item['temperature']))

        return temperatures


    def get_humidity(forcast: dict) -> list:
        '''
        Take in the forcast dictionary, store all the hourly humidity into 
        a list and return the list.
        '''
        humidity = []
    
        for item in forcast['properties']['periods']:
            humidity.append(str(item['relativeHumidity']['value']) + '%')
    
        return humidity

    def get_wind_speed(forcast: dict) -> list:
        '''
        Take in the forcast dictionary, store all the hourly wind speed into 
        a list and return the list.
        '''
        wind_speed = []
        for item in forcast['properties']['periods']:
            wind_speed.append(item['windSpeed'])
    
        return wind_speed
    
    def get_precipitation(forcast: dict) -> list:
        '''
        Take in the forcast dictionary, store all the hourly precipitation into 
        a list and return the list.
        '''
        precipitation = []
        
        for item in forcast['properties']['periods']:
            precipitation.append(str(item['probabilityOfPrecipitation']['value']) + '%')

        return precipitation

    def get_time(forcast: dict) -> list:
        '''
        Take in the forcast dictionary, store all the time info by hour 
        into a list and return the list.
        '''
        start_times = []

        for item in forcast['properties']['periods']:
            start_times.append(item['startTime'])
        
        return start_times

    def reverse_location(forcast: dict) -> str:
        '''
        Take in the forcast dictionary, store the coordinates of the polygon of 
        forcast area (no duplicates), then average out the coordinates to get the forcast location.
        '''
        polygon_lon = []
        polygon_lat = []
        sum_lon = 0
        sum_lat = 0

        for items in forcast['geometry']['coordinates'][0]:
            polygon_lon.append(items[0])
            polygon_lat.append(items[1])
        
        polygon_lon = list(set(polygon_lon))
        polygon_lat = list(set(polygon_lat))

        for x in polygon_lat:
            sum_lat += x
        for x in polygon_lon:
            sum_lon += x

        avg_lat = sum_lat/len(polygon_lat)
        avg_lon = sum_lon/len(polygon_lon)
        coordinates = f'{avg_lat}, {avg_lon}'

        # Uses reverse_geocoding method from geocoding module to get the specific location
        # given the coordinates.
        return geocoding.reverse_geocoding(coordinates)
    

# Class File contains methods that get information directly from a file at the same directory.
class File:
    def __init__(self, file: str):
        '''
        Takes in the file name, then access the json file and store the information.
        '''

        # Raise an error when the file not .json or does not exist in the directory
        try:
            json_file = open(file)
            self._text = json.load(json_file)
        except:
            print('FAIL')
            print(os.getcwd() + f'\{file}')
            if os.path.exists(os.getcwd() + f'\{file}') == False:
                print('MISSING')
            else:
                print('FORMAT')
            exit()


    def get_coordinates(self) -> tuple:
        '''
        Take in the dictionary derived from the json file and get the coordinates.
        '''
        coordinates = (self._text[0]['lat'], self._text[0]['lon'])
        return coordinates

    def get_temperature(self) -> list:
        '''
        Get all the temperatures from the dictionary, 
        store them into a list and return the list.
        '''
        temperatures = []

        for item in self._text['properties']['periods']:
            temperatures.append(int(item['temperature']))

        return temperatures


    def get_humidity(self) -> list:
        '''
        Get all the hourly humidity from the dictionary, 
        store them into a list and return the list.
        '''
        humidity = []
    
        for item in self._text['properties']['periods']:
            humidity.append(str(item['relativeHumidity']['value']) + '%')
    
        return humidity

    def get_wind_speed(self) -> list:
        '''
        Get all the hourly wind speed from the dictionary, 
        store them into a list and return the list.
        '''
        wind_speed = []
        for item in self._text['properties']['periods']:
            wind_speed.append(item['windSpeed'])
    
        return wind_speed
    
    def get_precipitation(self) -> list:
        '''
        Get all the hourly precipitation from the dictionary, 
        store them into a list and return the list.
        '''
        precipitation = []
        
        for item in self._text['properties']['periods']:
            precipitation.append(str(item['probabilityOfPrecipitation']['value']) + '%')

        return precipitation

    def get_time(self) -> list:
        '''
        Get all the hourly time info from the dictionary, 
        store them into a list and return the list.
        '''
        start_times = []

        for item in self._text['properties']['periods']:
            start_times.append(item['startTime'])
        
        return start_times

    def reverse_location(self) -> str:
        '''
        Get the reversed location from the json file with reversed geo info.
        '''
        location = self._text['display_name']
        return(location)



def _get_result(url: str) -> dict:
    '''
    Open the given api url to access the json text, then return it as an dictionary. 
    '''
    response = None

    try:
        # Here, we open the URL and read the response, just as we did before.
        # After the third line, json_text will contain the text of the
        # response, which should be in JSON format.
        request = urllib.request.Request(
            url,
            headers = {'User-Agent': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3, mubail1@uci.edu'})

        # Raise an error when the api return a status code other than 200.
        try:
            response = urllib.request.urlopen(request)
        except HTTPError as error:
            print('FAILED')
            print(f'{error.code} {url}')
            if error.code != 200 and error.code != None:
                print('NOT 200')

            exit()        

        # Raise an error when the API returned data that had missing or misformatted content.
        try:
            json_text = response.read().decode(encoding = 'utf-8')
        except json.JSONDecodeError as error:
            print('FAILED')
            print(url)
            print('FORMAT')
            exit()

        # Given the JSON text, we can use the json.loads() function to convert
        # it to a Python object instead.
        return json.loads(json_text)


    finally:
        # We'd better not forget to close the response when we're done,
        # assuming that we successfully opened it.
        if response != None:
            response.close()


def feel_like_temperature(temps: list, humid: list, wind: list) -> list:
    '''
    Take in a list of temperatures along with the corresponding humidity and wind speed at the same time.
    Then calculate the feel like temperature and store the value into a new list, return the list.
    '''
    feel_like_temps = []
    for i in range(0, len(temps)):
        h = humid[i].split('%')
        humidity = int(h[0])
        w = wind[i].split()
        wind_sd = int(w[0])
        temp = int(temps[i])

        if temp >= 68:
            fl_temp = -42.379 + 2.04901523 * temp + 10.14333127 * humidity - 0.22475541 * temp * humidity -0.00683783 * temp ** 2 - 0.05481717 * humidity ** 2 + 0.00122874 * temp ** 2 * humidity + 0.00085282 * temp * humidity ** 2 - 0.00000199 * temp ** 2 * humidity ** 2
            feel_like_temps.append(round(fl_temp, 4))
        elif temp <= 50 and wind_sd > 3:
            fl_temp = 35.74 + 0.6215 * temp - 35.75 * wind_sd ** 0.16 + 0.4275 * temp * wind_sd ** 0.16
            feel_like_temps.append(round(fl_temp, 4))
        else:
            feel_like_temps.append(temp)
    
    return feel_like_temps

def get_percent_num(percentages: list) -> list:
    '''
    Given a list of percentages, return them as integer type.
    '''
    values = []

    for i in range(0, len(percentages)):
        p = percentages[i].split('%')
        num = int(p[0])
        values.append(num)

    return values

def get_speed_num(speeds: list) -> list:
    '''
    Given a list of wind speed with 'mph' as unit, return them as integer type.
    '''
    values = []

    for i in range(0, len(speeds)):
        s = speeds[i].split()
        num = int(s[0])
        values.append(num)

    return values


def get_max(times: list, values: list) -> str:
    '''
    Find the max value (temperature, humidity, etc.) and return the value
    with the corresponding time.
    '''
    max = -1000
    for i in range(0, len(values)):
        if values[i] > max:
            max = values[i]
            max_index = i

    # Change the time to UTC time zone and format it into ISO 8601 
    time = datetime.fromisoformat(times[max_index].rsplit('-', 1)[0])
    convert_utc = time + timedelta(hours = 8)
    formatted_time = convert_utc.isoformat()

    return f"{formatted_time}Z {format(values[max_index], '.4f')}"

def get_min(times: list, values: list) -> str:
    '''
    Find the min value (temperature, humidity, etc.) and return the value
    with the corresponding time.
    '''
    min = 1000
    for i in range(0, len(values)):
        if values[i] < min:
            min = round(values[i], 4)
            min_index = i
    
    # Change the time to UTC time zone and format it into ISO 8601 
    time = datetime.fromisoformat(times[min_index].rsplit('-', 1)[0])
    convert_utc = time + timedelta(hours = 8)
    formatted_time = convert_utc.isoformat()

    return f"{formatted_time}Z {format(values[min_index], '.4f')}"

def convert_celsius(temps: list) -> list:
    '''
    Given a list of temperatures in Fahrenheit, convert them into celsius.
    '''
    temperatures = []
    for value in temps:
        temperatures.append(round((value - 32) * 5 / 9, 4))
    
    return temperatures

def length_list(length: int, the_list: list) -> list:
    '''
    Given the desired number of elements (n) and a list,
    return the first n elements from the list.
    '''
    new_list = []
    for i in range(0, length):
        new_list.append(the_list[i])
    
    return new_list








