# p2app/engine/main.py
#
# ICS 33 Winter 2024
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.
from p2app.events import *
import sqlite3
from pathlib import Path
from p2app.engine.continents_engine import Continents
from p2app.engine.countries_engine import Countries
from p2app.engine.regions_engine import Regions


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self._connection = None


    def process_event(self, event) -> None:
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        try:
            if isinstance(event, OpenDatabaseEvent):
                try:
                    connection = sqlite3.connect(event.path())
                    cursor = connection.execute('SELECT airport_id FROM airport;')
                    cursor.fetchone()
                    connection.execute('PRAGMA foreign_keys = ON;')
                    self._connection = connection
                    yield DatabaseOpenedEvent(event.path())
                except sqlite3.Error as e:
                    yield DatabaseOpenFailedEvent(str(e))

            elif isinstance(event, CloseDatabaseEvent):
                yield DatabaseClosedEvent()

            elif isinstance(event, QuitInitiatedEvent):
                yield EndApplicationEvent()

            else:
                for event in Continents.event_handler(Continents(), self._connection, event):
                    yield event

                for event in Countries.event_handler(Countries(), self._connection, event):
                    yield event

                for event in Regions.event_handler(Regions(), self._connection, event):
                    yield event
        except:
            yield ErrorEvent('Unknown error')










