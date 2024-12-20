# geocoding.py
#
# ICS 32A Fall 2023
# Project 3: From the Faraway Nearby

'''
This module contains the functions that uses NOMINATIM API
to perform geocoding/reverse geocoding.
'''

import json
import urllib.parse
import urllib.request
from urllib.error import HTTPError

BASE_NOMINATIM_URL = 'https://nominatim.openstreetmap.org'

def get_coordinates(location: str) -> tuple:
    '''
    Take in a free-format string representing an address, 
    geocoding to get the corresponding coordinates.
    '''
    query_parameters = [('q', location), ('format', 'json'), ('limit', 1)]
    
    search_url = f'{BASE_NOMINATIM_URL}/search?{urllib.parse.urlencode(query_parameters)}'

    # Raise an error if there's no internet connection and failed to access the content through url.
    try:
        result = _get_result(search_url)
    except:
        print('FAILED')
        print(search_url)
        print('NETWORK')
        exit()

    coordinates = (result[0]['lat'], result[0]['lon'])

    return(coordinates)

def reverse_geocoding(coordinates: str) -> str:
    '''
    Given the coordinates, reverse geocode to get the specific location corresponds to the coordinates.
    '''
    coordinates = coordinates.split(', ')
    query_parameters = [('format', 'json')]

    reverse_url = f'{BASE_NOMINATIM_URL}/reverse?lat={coordinates[0]}&lon={coordinates[1]}&{urllib.parse.urlencode(query_parameters)}'
    result = _get_result(reverse_url)
    location = result['display_name']

    return location

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
            headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/mubail1'})

        # Raise an error when the api return a status code other than 200.
        try:
            response = urllib.request.urlopen(request)
        except HTTPError as error:
            print('FAILED')
            print(f'{error.code} {url}')
            if error.code != 200:
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


