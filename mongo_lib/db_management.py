from pymongo import MongoClient


def connect_to_mongodb():
    # Connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    # client = MongoClient('mongodb://:@flightcatalog-shard-00-00-k6roz.mongodb.net:27017,flightcatalog-shard-00-01-k6roz.mongodb.net:27017,flightcatalog-shard-00-02-k6roz.mongodb.net:27017/test?ssl=true&replicaSet=flightCatalog-shard-0&authSource=admin')
    client = MongoClient('localhost', 27017)
    return client


def create_database_collection(conn, name, col_name = ''):
    db_flight_catalog = conn[name]
    col_flights = db_flight_catalog[col_name]
    return col_flights