from pymongo import MongoClient

# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
# ! Fake username and password FOR LOCAL USE ONLY !

login = "john"
password = "doe"
address = "127.0.0.1"

client = MongoClient(
    f"mongodb://{login}:{password}@{address}:27017/?authSource=admin&readPreference=primary&appname=Airlines%20Parser&ssl=false"
)

# !                                               !
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

db = client["airlines"]

frequent_flyers = db["frequent_flyers"]
boarding_data = db["boarding_data"]
sirena = db["sirena"]
exchange = db["exchange"]
