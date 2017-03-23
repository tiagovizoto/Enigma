#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import bson, json
from time import strftime, gmtime

class ConnectionFactoryMongo:
    def __init__(self):
        self.connection = pymongo.MongoClient("127.0.0.1:27017")
        self.db = self.connection.enigma

    def get_token(self):
        token = self.db.tokens
        return token

    def get_job(self):
        jobs_db = self.db.jobs
        return jobs_db

    def get_curriculum(self):
        return self.db.curriculum


class JobsModel:
    def __init__(self):
        self.db = ConnectionFactoryMongo().get_job()

    def add_jobs(self, job_json):
        try:
            self.db.insert_one(job_json)
            return True
        except Exception as e:
            return False

    def count_jobs(self):
        return self.db.count()

    def list_jobs(self, num):
        jobs = self.db.find().skip(num * 5).limit(5).sort('date_post', pymongo.DESCENDING)
        return jobs

    def find_jobs_email(self, email):
        try:
            jobs = self.db.find({'business.email': email})
            return jobs
        except Exception as e:
            return None

    def remove_jobs(self, id_job):
        try:
            self.db.delete_many({'_id': bson.ObjectId(id_job)})
        except:
            return 'Erro babaca'

    def search_jobs(self, pass_key):
        """Metodo para"""
        try:
            a = self.db.find({'$text': {'$search': pass_key}})
            return a
        except:
            return 'Sorry'

    def findEmailBussniss(self, id_job):
        result = self.db.find_one({'_id': bson.ObjectId(id_job)})
        return result['business']['email']

    def find_id(self, id):
        try:
            result = []
            result = self.db.find_one({'_id': bson.ObjectId(id)})
            return result
        except Exception as e:
            return e

    def update_job(self, id_job, date_job):
        job = date_job
        try:
            print(self.db.update({u'_id': bson.ObjectId(id_job)}, {'$set': {

                'title': job['title'],
                'location': job['location'],
                'description': job['description'],
                'business': {
                    'name': job['business']['name'],
                    'email': job['business']['email'],
                },
                'salary': {
                    'value': job['salary']['value'],
                    'coin': job['salary']['coin'],
                    'period_pay': job['salary']['period_pay']
                },
                'date_update': strftime("%Y-%m-%d", gmtime()),
            }
            }, upsert=False)
                  )
        except Exception as e:
            return e

    def insert_pearson(self, id, name, email):
        try:
            self.db.update({u'_id': id}, {'$set': {'candidaty': [{
                'name': name,
                'email': email,
                'date_apply': strftime("%Y-%m-%d", gmtime())
            }]}})
        except Exception as e:
            return e


class Token:
    def __init__(self):
        self.enigma = ConnectionFactoryMongo()

    def insert_token(self, token, email):
        db = self.enigma.get_token()
        try:
            if not db.find_one({'email': email}):
                db.insert({'email': email, 'tokens': [
                    {'token': token, 'date_create': strftime("%Y-%m-%d", gmtime()), 'active': True}
                ]})

            else:
                db.update_one({'email': email}, {'$push': {'tokens':
                                                               {'token': token,
                                                                'date_create': strftime("%Y-%m-%d", gmtime()),
                                                                'active': True}
                                                           }})
        except Exception as e:
            return e

    def find_token(self, token):
        db = self.enigma.get_token()
        a = db.find({'tokens': {'$elemMatch': {'token': token}}})
        return a

    def alter_token(self, token):
        try:
            db = self.enigma.get_token()
            db.update({'token': token}, {'$set': {'active': False}})
        except Exception as e:
            return e

    def list_token(self, email):
        db = self.enigma.get_token()
        try:
            return db.find({'email': email})
        except Exception as e:
            return e


class Curriculum(ConnectionFactoryMongo):
    def __init__(self):
         self.db = ConnectionFactoryMongo.__init__()

    def add_curriculum(self,curriculum):
        return self.db.insert(curriculum)

    def update_curriculum(self, id_curriculum, curriculum):
        try:
            print(
                self.db.update({
                u'_id': bson.ObjectId(id_curriculum)},
                {'$set': curriculum}, upsert=False)
                  )
        except Exception as e:
            return e

    def drop_curriculum(self, id_curriculum):
        try:
            self.db.delete_many({'_id': bson.ObjectId(id_curriculum)})
        except:
            return 'Erro babaca'


    def search_curriculum(self, pass_key):
        try:
            a = self.db.find({'$text': {'$search': pass_key}})
            return a
        except:
            return {'error':None}

    def list_curriculum(self):
        try:
            return self.db.find().skip(num * 5).limit(5).sort('date_post', pymongo.DESCENDING)
        except BaseException as w:
            return w

    def find_id(self, id):
        try:
            result = []
            result = self.db.find_one({'_id': bson.ObjectId(id)})
            return result
        except Exception as e:
            return e

'''a = Token()
b = a.find_token('SBEG0SG7G69ZIQYO')
for i in b:
    print(i['email'])'''
##db.tokens.find({tokens:{$elemMatch:{token:'IV522ZRJ0CVESYF5'}}}).pretty()
