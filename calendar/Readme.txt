Problem Statement:

Design and build an interface to display events, given information as structured below. Any solution is valid – e.g. a javascript calendar widget, a beautifully formatted web page, a command line tool.
  ```json
{
  "events": [
    {
      "occasion": "Birthday party",
      "invited_count": 120,
      "year": 2016,
      "month": 2,
      "day": 14
    },
    {
      "occasion": "Technical discussion",
      "invited_count": 23,
      "year": 2016,
      "month": 11,
      "day": 24
    },
    {
      "occasion": "Press release",
      "invited_count": 64,
      "year": 2015,
      "month": 12,
      "day": 17,
      "cancelled": true
    },
    {
      "occasion": "New year party",
      "invited_count": 55,
      "year": 2016,
      "month": 1,
      "day": 1
    }
  ]
}


Developed using python 3.5


To run: 

python calendar.py -customer_json_file=events.json

To test:

python -m unittest -v test_calendar.py 