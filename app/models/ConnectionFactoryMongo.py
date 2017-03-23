import pymongo


class ConnectionFactoryMongo:
    def __init__(self):
        self.connection = pymongo.MongoClient("127.0.0.1:27017")
        self.db = self.connection.enigma

    def get_token(self):
        token = self.db.tokens
        return token

    def get_job(self):
        jobs_db = self.db.jobs
        return self.db.jobs

    def get_curriculum(self):
        return self.db.curriculum

    def get_rh(self):
        return self.db.rh