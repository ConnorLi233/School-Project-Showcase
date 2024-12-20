# p2app/engine/continents_engine.py
#
# ICS 33 Winter 2024
# Project 2: Learning to Fly

import sqlite3
from p2app.events import *

class Continents:
    """
    This object processes all the continent-related events sent to it by the user interface,
    then generate events that are sent back to the user interface in response, into a list.
    """

    def __init__(self):
        """Initializes the continents engine"""
        pass

    def event_handler(self, connection: sqlite3.Connection, event: 'events') -> list['events']:
        """
        Returns a list of all the events that should be generated by the main module as the response,
        given the events sent to it by the user interface.
        """
        events = []
        if isinstance(event, StartContinentSearchEvent):
            if not event.continent_code():
                statement = 'SELECT * FROM continent WHERE name = ?;'
                parameters = (event.name(), )
            elif not event.name():
                statement = 'SELECT * FROM continent WHERE continent_code = ?;'
                parameters = (event.continent_code(), )
            else:
                statement = 'SELECT * FROM continent WHERE continent_code = ? AND name = ?;'
                parameters = (event.continent_code(), event.name())

            cursor = connection.execute(statement, parameters)
            results = cursor.fetchall()
            for result in results:
                continent = Continent(result[0], result[1], result[2])
                events.append(ContinentSearchResultEvent(continent))
            cursor.close()

        if isinstance(event, LoadContinentEvent):
            statement = 'SELECT * FROM continent WHERE continent_id = ?;'
            parameter = (event.continent_id(), )
            cursor = connection.execute(statement, parameter)
            loaded_continent = cursor.fetchone()

            events.append(ContinentLoadedEvent(Continent(loaded_continent[0], loaded_continent[1], loaded_continent[2])))
            cursor.close()

        if isinstance(event, SaveNewContinentEvent):
            try:
                statement = 'INSERT INTO continent (continent_code, name) VALUES (:continent_code, :name);'
                parameters = {'continent_code': event.continent()[1], 'name': event.continent()[2]}
                cursor = connection.execute(statement, parameters)
                connection.commit()

                added_continent = Continent(cursor.lastrowid, event.continent()[1], event.continent()[2])
                events.append(ContinentSavedEvent(added_continent))
                cursor.close()

            except sqlite3.IntegrityError:
                events.append(SaveContinentFailedEvent('Duplicate continent_code Not Allowed'))

        if isinstance(event, SaveContinentEvent):
            try:
                statement = 'UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?;'
                parameters = (event.continent()[1], event.continent()[2], event.continent()[0])
                connection.execute(statement, parameters)
                connection.commit()

                modified_continent = Continent(event.continent()[0], event.continent()[1], event.continent()[2])
                events.append(ContinentSavedEvent(modified_continent))

            except sqlite3.IntegrityError:
                events.append(SaveContinentFailedEvent('Duplicate continent_code Not Allowed'))

        return events




