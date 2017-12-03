from mongo_lib import db_management as db_mgm
from pprint import pprint
from bson.code import Code


col_flights = db_mgm.create_database_collection(db_mgm.connect_to_mongodb(), 'flight_catalog', 'flights')
if  not col_flights:
    raise NameError('Database or collection not found or could not be created')

mapper = Code("""
            function () {
                var month = this.depD.substr(0,7);
                var key = month + '-' + this.orig + '-' + this.dest;
                emit( key, {
                            "month": month,
                            "orig": this.orig,
                            "dest": this.dest,
                            "comp": this.comp,
                            "depD": this.depD,
                            "arrD": this.arrD,
                            "priceAdult": this.prices.adt
                           } );
            }
              """)

reducer = Code("""
function (key, flights) {
        var minPrice = 100000000;
        var selectFlight = {};
        
        flights.forEach( function(flight){
                if ( minPrice > flight.priceAdult ) {
                    minPrice = flight.priceAdult;
                    selectFlight = flight;
                }
            }
        );
        
        return selectFlight;
    }
""")

result = col_flights.map_reduce(mapper, reducer, "cheapest_flight_monthly")
for doc in result.find():
    pprint(doc)
