from mongo_lib import db_management as db_mgm
from pprint import pprint
import random


def get_imaginary_flight(date, city_orig, city_dest, company, amount):
    """
    :param date:
    :param city_orig:
    :param city_dest:
    :param company:
    :param amount:
    :return:
    """
    amount_child = amount * 0.5
    flight = {
        "depD": date,
        "arrD": date,
        "orig": city_orig,
        "dest": city_dest,
        "comp": company,
        "prices": {
            "adt": amount,
            "chd": amount_child,
            "inf": amount_child
        }
    }
    return flight


def create_flights(col_flights):
    """
    :param col_flights:
    :return:
    """
    how_many = 0
    for month in range(1, 12):
        for day_of_month in range(1, 29):

            how_many_flights_in_day = random.randint(2, 20)
            for repetitions in range(1, how_many_flights_in_day):
                how_many += 1

                str_end_day = str(day_of_month).zfill(2)
                date = "2018-" + str(month).zfill(2) + "-" + str_end_day

                cities_of_spain = ['BCN', 'GIR', 'MAD', 'VAL', 'OVD', 'ALI', 'GRA', 'STG', 'SEV', 'SAN']
                city_orig = random.choice(cities_of_spain)
                cities_of_spain.remove(city_orig)
                city_dest = random.choice(cities_of_spain)

                companies = ['KLM', 'VY', 'AF', 'LTH', 'IBE', 'QTR']
                company = random.choice(companies)


                amount = random.randint(50, 350)
                # Summer is most expensive season:
                if (month == 7 or month == 8):
                    amount = amount*1.5
                elif (month == 2 or month == 11):
                    amount = amount * 0.7
                # Vueling is cheaper than the rest:
                if (company == 'VY'):
                    amount = amount * 0.5
                else:
                    amount = amount * 1.2

                post_flight_id = col_flights.insert_one(get_imaginary_flight(date, city_orig, city_dest, company, amount)).inserted_id
                pprint(post_flight_id)

    return how_many


col_flights = db_mgm.create_database_collection(db_mgm.connect_to_mongodb(), 'flight_catalog', 'flights')
if  not col_flights:
    raise NameError('Database or collection not found or could not be created')


number_of_flights = create_flights(col_flights)
print str(number_of_flights) + ' flights created'