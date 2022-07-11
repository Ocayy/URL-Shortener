import pymongo

password = ""
url = f"mongodb+srv://jaco13_python:{password}@github-projects.a4nag.mongodb.net/?retryWrites=true&w=majority"

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(url)

    def add_short_url(self, short_url: str, long_url: str, timestamp: str) -> None:
        database = self.client["URL-Shortener"]
        collection = database["urls"]

        collection.insert_one(
            {
                "short_url": short_url,
                "long_url": long_url,
                "created_date": timestamp,
                "last_visit": "",
                "visits": 0
            }
        )

    def delete_url(self, short_url: str) -> None:
        database = self.client["URL-Shortener"]
        collection = database["urls"]

        collection.delete_one({"short_url": short_url})

    def get_data_from_short_url(self, short_url: str) -> dict:
        database = self.client["URL-Shortener"]
        collection = database["urls"]

        return collection.find_one({"short_url": short_url})

    def add_visits(self, short_url: str, timestamp: str) -> None:
        database = self.client["URL-Shortener"]
        collection = database["urls"]

        collection.update_one(
            {"short_url": short_url},
            {
                "$inc": {"visits": 1},
                "$set": {"last_visit": timestamp}
            },
        )

    def get_stats(self):
        database = self.client["URL-Shortener"]
        collection = database["urls"]

        return collection.count_documents({})

    def get_all_data(self):
        database = self.client["URL-Shortener"]
        collection = database["urls"]

        return collection.find()