from pymongo import MongoClient

# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
# ! Fake username and password FOR LOCAL USE ONLY !

address = "localhost"

client = MongoClient(
    f"mongodb://{address}:27017/?authSource=admin&readPreference=primary&appname=Airlines%20Parser&ssl=false"
)

# !                                               !
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

db = client["airlines"]

frequent_flyers = db["frequent_flyers"]
boarding_data = db["boarding_data"]
sirena = db["sirena"]
exchange = db["exchange"]
boarding_passes = db["boarding_passes"]
