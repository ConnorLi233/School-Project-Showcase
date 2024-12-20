# project3.py
#
# ICS 32A Fall 2023
# Project 3: From the Faraway Nearby

'''
This program takes in the user input and respond accordingly 
by using NWS api and Nominatim api.
'''

import weather
import geocoding

def print_coordinates(coordinates: tuple) -> None:
    '''
    Take in the raw coordinates and print them in the correct format.
    '''
    lat = coordinates[0]
    lon = coordinates[1]

    if float(lat) > 0:
        lat = lat + '/N'
    elif float(lat) < 0:
        lat = str(abs(float(lat))) + '/S'
    if float(lon) > 0:
        lon = lon + '/E'
    elif float(lon) < 0:
        lon = str(abs(float(lon))) + '/W'
    
    return f'TARGET {lat} {lon}'


def run() -> None:
    '''
    Utilizes functions from weather module and geocoding module,
    ouputs information based on the user input.
    '''
    output = []
    attribution_message = []
    command = input()
    break_down_cd = command.split(' ', 2)

    # If the user input has 'NOMINATIM', call methods in class Api from the weather module.
    if break_down_cd[1] == 'NOMINATIM':
        
        coordinates = geocoding.get_coordinates(break_down_cd[2])
        output.append(print_coordinates(coordinates))
        attribution_message.append('**Forward geocoding data from OpenStreetMap')

        command = input()
        break_down_cd = command.split(' ', 2)

        if break_down_cd[1] == 'NWS':
            location = weather.Api(coordinates)
            forcast = location.get_hourly_forcast()
            attribution_message.append('**Real-time weather data from National Weather Service, United States Department of Commerce')

        # Keeps taking in queries until the user input: 'NO MORE QUERIES'
        while command != 'NO MORE QUERIES':
            command = input()
            break_down_cd = command.split()

            if break_down_cd[0] == 'TEMPERATURE':
                temps = weather.Api.get_temperature(forcast)
                times = weather.Api.get_time(forcast)
                temps = weather.length_list(int(break_down_cd[3]), temps)

                if break_down_cd[1] == 'FEELS':
                    temps = weather.feel_like_temperature(temps, weather.Api.get_humidity(forcast), weather.Api.get_wind_speed(forcast))
                if break_down_cd[2] == 'C':
                    temps = weather.convert_celsius(temps)

                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, temps))
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, temps))

            elif break_down_cd[0] == 'HUMIDITY':
                humidity = weather.Api.get_humidity(forcast)
                times = weather.Api.get_time(forcast)
                humidity = weather.length_list(int(break_down_cd[1]), humidity)

                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, weather.get_percent_num(humidity)) + '%')
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, weather.get_percent_num(humidity)) + '%')
            
            elif break_down_cd[0] == 'WIND':
                wind_speed = weather.Api.get_wind_speed(forcast)
                times = weather.Api.get_time(forcast)
                wind_speed = weather.length_list(int(break_down_cd[1]), wind_speed)
                
                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, weather.get_speed_num(wind_speed)) + ' mph')
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, weather.get_speed_num(wind_speed)) + ' mph')

            elif break_down_cd[0] == 'PRECIPITATION':
                precip = weather.Api.get_precipitation(forcast)
                times = weather.Api.get_time(forcast)
                precip = weather.length_list(int(break_down_cd[1]), precip)

                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, weather.get_percent_num(precip)) + '%')
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, weather.get_percent_num(precip)) + '%')
        
        command = input()
        break_down_cd = command.split()

        # If the user input equals 'REVERSE NOMINATIM', reverse geocode.
        if break_down_cd[0] == 'REVERSE' and break_down_cd[1] == 'NOMINATIM':
            output.insert(1, weather.Api.reverse_location(forcast))
            attribution_message.insert(1, '**Reverse geocoding data from OpenStreetMap')

    # If the user input has 'FILE', call methods in class File from the weather module.
    elif break_down_cd[1] == 'FILE':
        coordinates = weather.File(break_down_cd[2]).get_coordinates()
        output.append(print_coordinates(coordinates))

        command = input()
        break_down_cd = command.split(' ', 2)

        if break_down_cd[1] == 'FILE':
                forcast = weather.File(break_down_cd[2])

        while command != 'NO MORE QUERIES':
            command = input()
            break_down_cd = command.split()

            if break_down_cd[0] == 'TEMPERATURE':
                temps = weather.File.get_temperature(forcast)
                times = weather.File.get_time(forcast)
                temps = weather.length_list(int(break_down_cd[3]), temps)

                if break_down_cd[1] == 'FEELS':
                    temps = weather.feel_like_temperature(temps, weather.File.get_humidity(forcast), weather.File.get_wind_speed(forcast))
                if break_down_cd[2] == 'C':
                    temps = weather.convert_celsius(temps)

                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, temps))
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, temps))

            elif break_down_cd[0] == 'HUMIDITY':
                humidity = weather.File.get_humidity(forcast)
                times = weather.File.get_time(forcast)
                humidity = weather.length_list(int(break_down_cd[1]), humidity)

                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, weather.get_percent_num(humidity)) + '%')
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, weather.get_percent_num(humidity)) + '%')
            
            elif break_down_cd[0] == 'WIND':
                wind_speed = weather.File.get_wind_speed(forcast)
                times = weather.File.get_time(forcast)
                wind_speed = weather.length_list(int(break_down_cd[1]), wind_speed)
                
                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, weather.get_speed_num(wind_speed)) + ' mph')
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, weather.get_speed_num(wind_speed)) + ' mph')

            elif break_down_cd[0] == 'PRECIPITATION':
                precip = weather.File.get_precipitation(forcast)
                times = weather.File.get_time(forcast)
                precip = weather.length_list(int(break_down_cd[1]), precip)

                if break_down_cd[-1] == 'MAX':
                    output.append(weather.get_max(times, weather.get_percent_num(precip)) + '%')
                elif break_down_cd[-1] == 'MIN':
                    output.append(weather.get_min(times, weather.get_percent_num(precip)) + '%')
        
        command = input()
        break_down_cd = command.split()

        # If the user input equals 'REVERSE FILE', get the reversed location from the designated file.
        if break_down_cd[0] == 'REVERSE' and break_down_cd[1] == 'FILE':
            reverse_file = weather.File(break_down_cd[2])
            output.insert(1, weather.File.reverse_location(reverse_file))
    
    for x in output:
        print(x)
    
    if len(attribution_message) > 0:
        for x in attribution_message:
            print(x)


if __name__ == '__main__':
    run()