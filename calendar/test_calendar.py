from unittest import TestCase
from calendar import Calendar, Event
from datetime import date
import json
import os

class TestCalendar(TestCase):

    def mock_events_json(self):
        return {"events": [{
            "occasion": "Birthday party",
            "invited_count": 120,
            "year": 2016,
            "month": 2,
            "day": 14
        }]}

    def malformed_events_json(self):
        return {"events": [{
            "occasion": "Birthday party",
            "year": 2016,
            "month": 2
        }]}

    def invalid_date_events_json(self):
        return {"events": [{
            "occasion": "Birthday party",
            "invited_count": 120,
            "year": 2016,
            "month": 42,
            "day": 14
        }]}

    ''' Test for read_customer_json_file method
    '''
    def test_read_customer_json_file(self):
        mock_file = None
        try:
            # creating a mock json file and reading it
            mock_file = open('mock_cal.json', 'w')
            json.dump({"occasion": "Birthday party"}, mock_file)
            mock_file.close()
            mock_json = Calendar('mock_cal.json').read_events_json_file()
            self.assertEqual(mock_json['occasion'], 'Birthday party')
        except IOError:
            raise Exception('error creating mock file')
        finally:
            if mock_file:
                mock_file.close()
                os.remove('mock_cal.json')


    ''' Test read_events_json_file function raises an exception if
        input json file does not exists
    '''
    def test_read_customer_json_file_error(self):
        self.assertRaises(Exception, lambda:Calendar.read_events_json_file('mock.json'))

    ''' Test if read_events_json_file method raises exception
        if input json is not valid json.
    '''
    def test_parse_events_json(self):
        orig_method = Calendar.read_events_json_file
        try:
            Calendar.read_events_json_file = self.malformed_events_json
            self.assertRaises(Exception, lambda:Calendar('events.json').parse_events_json())
        finally:
            Calendar.read_events_json_file = orig_method

    ''' Test if read_events_json_file method raises exception
        if event date is invalid
    '''
    def test_parse_events_json(self):
        orig_method = Calendar.read_events_json_file
        try:
            Calendar.read_events_json_file = self.invalid_date_events_json
            self.assertRaises(Exception, lambda:Calendar('events.json').parse_events_json())
        finally:
            Calendar.read_events_json_file = orig_method

    ''' Test if parse_events_json parses a valid json correctly.
    '''
    def test_parse_events_json_error(self):
        orig_method = Calendar.read_events_json_file
        try:
            Calendar.read_events_json_file = self.mock_events_json
            events = Calendar('events.json').parse_events_json()
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].name, 'Birthday party')
        finally:
            Calendar.read_events_json_file = orig_method

    ''' Test if sort_events_by_date method sorts date in asc order correctly.
    '''
    def test_sort_events_by_date(self):
        events = [Event(name='event3', invited_count='1', date=date(year=2016, month=5, day=2)),
                  Event(name='event2', invited_count='100', date=date(year=2016, month=4, day=2)),
                  Event(name='event1', invited_count='10', date=date(year=2015, month=12, day=2))
                 ]
        sorted_events = Calendar.sort_events_by_date(events)
        self.assertEqual(sorted_events[0].name, 'event1')
        self.assertEqual(sorted_events[0].date, date(year=2015, month=12, day=2))

