# p2app/engine/regions_engine.py
#
# ICS 33 Winter 2024
# Project 2: Learning to Fly

import sqlite3
from p2app.events import *

class Regions:
    """
    This object processes all the region-related events sent to it by the user interface,
    then generate events that are sent back to the user interface in response, into a list.
    """
    def __init__(self):
        """Initializes the regions engine"""
        pass

    def event_handler(self, connection: sqlite3.Connection, event: 'events') -> list['events']:
        """
        Returns a list of all the events that should be generated by the main module as the response,
        given the events sent to it by the user interface.
        """

        events = []
        if isinstance(event, StartRegionSearchEvent):
            statement = 'SELECT * FROM region WHERE '
            characteristics = []
            parameters = []
            if event.region_code():
                parameters.append(event.region_code())
                characteristics.append('region_code = ?')
            if event.local_code():
                parameters.append(event.local_code())
                characteristics.append('local_code = ?')
            if event.name():
                parameters.append(event.name())
                characteristics.append('name = ?')

            statement += ' AND '.join(characteristics)
            cursor = connection.execute(statement, parameters)
            results = cursor.fetchall()
            for result in results:
                region = Region(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
                events.append(RegionSearchResultEvent(region))
            cursor.close()

        if isinstance(event, LoadRegionEvent):
            statement = 'SELECT * FROM region WHERE region_id = ?;'
            parameter = (event.region_id(), )
            cursor = connection.execute(statement, parameter)
            loaded_region = cursor.fetchone()

            events.append(RegionLoadedEvent(Region(loaded_region[0], loaded_region[1], loaded_region[2], loaded_region[3], loaded_region[4], loaded_region[5], loaded_region[6], loaded_region[7])))
            cursor.close()

        if isinstance(event, SaveNewRegionEvent):
            try:
                statement = 'INSERT INTO region (region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (:region_code, :local_code, :name, :continent_id, :country_id, :wikipedia_link, :keywords);'
                new_region = event.region()

                parameters = {'region_code': new_region[1], 'local_code': new_region[2], 'name': new_region[3], 'continent_id': new_region[4], 'country_id': new_region[5], 'wikipedia_link': new_region[6], 'keywords':new_region[7]}
                cursor = connection.execute(statement, parameters)
                connection.commit()

                added_region = Region(cursor.lastrowid, new_region[1], new_region[2], new_region[3], new_region[4], new_region[5], new_region[6], new_region[7])
                events.append(RegionSavedEvent(added_region))
                cursor.close()

            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    events.append(SaveRegionFailedEvent('Duplicate region_code Not Allowed'))
                elif "FOREIGN KEY constraint failed" in str(e):
                    events.append(SaveRegionFailedEvent('Invalid continent_code or country code'))


        if isinstance(event, SaveRegionEvent):
            try:
                statement = 'UPDATE region SET region_code=?, local_code=?, name=?, continent_id=?, country_id=?, wikipedia_link=?, keywords=? WHERE region_id = ?;'
                new_region = event.region()

                parameters = (new_region[1], new_region[2], new_region[3], new_region[4], new_region[5], new_region[6], new_region[7], new_region[0])
                connection.execute(statement, parameters)
                connection.commit()

                modified_region = Region(new_region[0], new_region[1], new_region[2], new_region[3], new_region[4], new_region[5], new_region[6], new_region[7])
                events.append(RegionSavedEvent(modified_region))

            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    events.append(SaveRegionFailedEvent('Duplicate region_code Not Allowed'))
                elif "FOREIGN KEY constraint failed" in str(e):
                    events.append(SaveRegionFailedEvent('Invalid continent_code or country code'))

        return events