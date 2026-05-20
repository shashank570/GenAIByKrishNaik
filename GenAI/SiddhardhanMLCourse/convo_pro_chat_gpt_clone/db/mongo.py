from pymongo import MongoClient # Mongo DB Driver
from config.settings import Settings

settings = Settings()

_client = MongoClient(settings.MONGO_DB_URL, tz_aware=True)
# tz_aware -> "Return datetime objects with timezone information attached. Used for comparing dates"
# without tz_aware -> datetime.datetime(2025, 8, 17, 10, 30)
# with tz_aware -> datetime.datetime(2025, 8, 17, 10, 30, tzinfo=<UTC>)
_db = _client[settings.MONGO_DB_NAME]


def get_collection(name: str):
    return _db[name]


# chat_collection = get_collection("chat_history") 

# chat_collection.insert_one({
#     "user": "Shashank",
#     "message": "Hello"
# })

# you can also use find(), find_one()