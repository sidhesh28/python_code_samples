from math import radians, sin, cos, asin, sqrt
import json
import argparse

REF_LAT = 53.3381985
REF_LONG = -6.2592576
RAD_TO_KM = 6371

''' Read customer json file and return customer json.
'''
def read_customer_json_file(customer_json_file_path):
    customer_json_file = None
    try:
        customer_json_file = open(customer_json_file_path)
        customers_json = json.load(customer_json_file)
    except json.JSONDecodeError:
        raise Exception('Error occured while parsing events json file')
    except FileNotFoundError:
        raise Exception('{} does not exist'.format(customer_json_file_path))
    except IOError:
        raise Exception('Error occured while opening file {}'.format(customer_json_file_path))
    finally:
        if customer_json_file:
            customer_json_file.close()

    return customers_json

''' Returns list of Customer objects from customer json
'''
def get_customer_list(customers_json):
    customers = []
    try:
        for customer in customers_json:
            customers.append(Customer(user_id=customer['user_id'],
                                      name=customer['name'],
                                      lat=customer['latitude'],
                                      long=customer['longitude']))
    except KeyError:
        raise Exception('Key missing')

    return customers

''' Return the shortest distance between two points in km.
    Ref: https://en.wikipedia.org/wiki/Great-circle_distance
'''
def calculate_distance_in_km(ref_lat, ref_long, lat, long):
    # convert lat, long to radians
    ref_lat_rad, ref_long_rad, lat_rad, long_rad = [radians(dec) for dec in [ref_lat, ref_long, lat, long]]

    # great-circle distance formulae
    delta_lat = lat_rad - ref_lat_rad
    delta_long = long_rad - ref_long_rad
    distance_in_radians = 2 * asin(sqrt(sin(delta_lat/2)**2 + cos(delta_lat) * cos(delta_long) * sin(delta_long/2)**2))

    # convert distance to km
    distance_in_km = RAD_TO_KM * distance_in_radians

    return distance_in_km

''' Displays the list of customers that are inside the allowed distance.
'''
def filter_customer_by_distance(customers, max_allowed_distance):
    invited_customers = []
    for customer in customers:
        distance_in_km = calculate_distance_in_km(ref_lat=REF_LAT, ref_long=REF_LONG,
                                 lat=customer.lat_in_float, long=customer.long_in_float
                                 )
        # customers inside allowed_distance are invited
        if round(distance_in_km, 2) <= round(max_allowed_distance,2):
            invited_customers.append(customer)

    return invited_customers

''' Displays names of customers within max_allowed_distance of REF_LAT & REF_LONG
'''
def display_invited_customers(invited_customers):
    if len(invited_customers) >=0:
        print('Invited customer list:')
        for customer in invited_customers:
            print(customer.name + "\n")
    else:
        print('Customer invitee list empty')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-customer_json_file", help="customer json file path")
    parser.add_argument("-max_allowed_distance", help="max allowed distance to be invited to the party",
                        type=float)
    args = parser.parse_args()


    customers_json = read_customer_json_file(args.customer_json_file)
    customers = get_customer_list(customers_json)
    invited_customers = filter_customer_by_distance(customers, args.max_allowed_distance)
    display_invited_customers(invited_customers)


''' Customer object
    Properties - user_id:int, name:string, lat:string, long:string,
    lat_in_float:float & long_in_float:float.
'''
class Customer(object):
    def __init__(self, user_id, name, lat, long):
        self.user_id = user_id
        self.name = name
        self.lat = lat
        self.long = long

    @property
    def lat_in_float(self):
        return float(self.lat)

    @property
    def long_in_float(self):
        return float(self.long)

if __name__ == "__main__":
    main()


