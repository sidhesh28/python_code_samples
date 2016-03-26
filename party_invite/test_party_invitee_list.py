from unittest import TestCase
from party_invitee_list import get_customer_list, calculate_distance_in_km,\
    Customer, filter_customer_by_distance, read_customer_json_file
from datetime import date
import json
import os


class TestPartyInviteeList(TestCase):

    def mock_customer_json(self):
        return [{"latitude": "52.986375", "user_id": 12, "name": "Christina McArdle", "longitude": "-6.043701"},
         {"latitude": "51.92893", "user_id": 1, "name": "Alice Cahill", "longitude": "-10.27699"},
         {"latitude": "51.8856167", "user_id": 2, "name": "Ian McArdle", "longitude": "-10.4240951"},
         {"latitude": "52.3191841", "user_id": 3, "name": "Jack Enright", "longitude": "-8.5072391"}]

    def test_read_customer_json_file_(self):
        mock_file = None
        try:
            mock_file = open('mock.json', 'w')
            json.dump({"name": "Christina"}, mock_file)
            mock_file.close()
            mock_json = read_customer_json_file('mock.json')
            self.assertEqual(mock_json['name'], 'Christina')
        except IOError:
            raise Exception('error creating mock file')
        finally:
            if mock_file:
                mock_file.close()
                os.remove('mock.json')


    ''' Test read_customer_json_file function raises an exception if
        input json file does not exists
    '''
    def test_read_customer_json_file_error(self):
        self.assertRaises(Exception, lambda:read_customer_json_file('mock.json'))

    ''' Test get_customer_list method
    '''
    def test_get_customer_list(self):
        customers = get_customer_list(self.mock_customer_json())
        self.assertEqual(len(customers), 4)
        self.assertEqual(customers[0].name, 'Christina McArdle')

    ''' Test calculate_distance_in_km method
    '''
    def test_calculate_distance_in_km(self):
        self.assertEqual(round(calculate_distance_in_km(53.3381985,-6.2592576, 53.3381985,-6.2592576), 2)
                         , 0.00)
        self.assertEqual(round(calculate_distance_in_km(41.507483,-99.436554, 38.504048, -98.315949), 2)
                         , 356.43)
        self.assertEqual(round(calculate_distance_in_km(53.3381985, -6.2592576, 53.8483, -7), 2)
                         , 100)

    ''' Test filter_customer_by_distance method
    '''
    def test_filter_customer_by_distance(self):
        # test mock customer json
        customers = get_customer_list(self.mock_customer_json())
        invited_customers = filter_customer_by_distance(customers, 100)
        self.assertEqual(len(invited_customers), 1)
        self.assertEqual(invited_customers[0].name, 'Christina McArdle')

        # test empty customer json
        customers = get_customer_list([])
        invited_customers = filter_customer_by_distance(customers, 100)
        self.assertEqual(len(invited_customers), 0)



