import json
import datetime
import argparse

''' Reads events from json and displays the events sorted by event date
'''
class Calendar(object):

    def __init__(self, events_json_file_path):
        self.events_json_file_path = events_json_file_path

    ''' Read events json file and return events json.
    '''
    def read_events_json_file(self):
        events_json_file = None

        try:
            events_json_file = open(self.events_json_file_path)
            events_json = json.load(events_json_file)
        except json.JSONDecodeError:
            raise Exception('Error occured while parsing events json file')
        except FileNotFoundError:
            raise Exception('{} does not exist'.format(self.events_json_file_path))
        except IOError:
            raise Exception('Error occured while opening file {}'.format(self.events_json_file_path))
        finally:
            if events_json_file:
                events_json_file.close()

        return events_json

    ''' Returns list of Event objects from events json
    '''
    def parse_events_json(self):
        events = []
        try:
            events_dict = self.read_events_json_file()['events']
            for event in events_dict:
                # Check if year, month and day are int
                if not isinstance(event['year'], int) or not isinstance(event['month'], int) or \
                        not isinstance(event['day'], int):
                    raise Exception('Invalid date in json')
                events.append(Event(name=event['occasion'],
                                    invited_count=event['invited_count'],
                                    date=datetime.date(year=event['year'],
                                                       month=event['month'],
                                                       day=event['day'])))
        except ValueError:
            raise Exception('Date is invalid')
        except KeyError:
            raise Exception('Key missing from events json')
        except Exception:
            raise Exception('Error parsing events json')

        return events

    ''' Sort event list containing Event objects by date asc.
    '''
    @staticmethod
    def sort_events_by_date(events):
        return sorted(events, key=lambda x: x.date)


    ''' Display events sorted by event date in asc order
    '''
    def display_events(self):
        events = self.parse_events_json()
        if len(events) == 0:
            print('No events to display')
        else:
            events = self.sort_events_by_date(events)
            for event in events:
                if event.days_til_event < 0:
                    print("Following event was {} days ago: \n".format(abs(event.days_til_event)))
                else:
                    print("Folowing event in {} days: \n".format(event.days_til_event))
                print("Event: {}\n".format(event.name))
                print("Invited Count: {}\n".format(event.invited_count))
                print("Date: {}\n".format(event.date))
                print("-----------------------------")

''' Event object
    Properties - name:string, invited_count:int, date:date,
    days_til_event: int
'''
class Event(object):
    def __init__(self, name, invited_count, date):
        self.name = name
        self.invited_count = invited_count
        self.date = date

    @property
    def days_til_event(self):
        delta_date = self.date - datetime.date.today()
        return delta_date.days

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-customer_json_file", help="customer json file path")
    args = parser.parse_args()

    Calendar(args.customer_json_file).display_events()


if __name__ == "__main__":
    main()