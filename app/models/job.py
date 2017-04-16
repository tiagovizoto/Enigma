from app.models.ConnectionFactoryMongo import ConnectionFactoryMongo
import bson, json
from time import strftime, gmtime
import pymongo


class Job:
    """
    Classe com o objetivo de gerenciar as vagas postadad
    """

    def __init__(self):
        self.enigma = ConnectionFactoryMongo()
        self.db = self.enigma.get_job()

    def count_jobs(self):
        """
        Retorna o total de vagas
        :return:
        """
        return self.db.count()

    def list_jobs(self, pagina):
        """
        Sistema de paginação
        :param num:
        :return:
        """
        if pagina > int(0):
            jobs = self.db.find().skip((pagina) * 10).limit(10).sort('date_post', pymongo.DESCENDING)
            return jobs
        else:
            jobs = self.db.find().skip(pagina * 10).limit(10).sort('date_post', pymongo.DESCENDING)
            return jobs


    def find_jobs_email(self, email):
        """
        Lista todas vagas postada pelo RH
        :param email:
        :return:
        """
        try:
            jobs = self.db.find({'job.business.email': email})
            if jobs:
                return jobs
            else:
                return jobs
        except Exception as e:
            return None

    def search_jobs(self, pass_key):
        """
        db.jobs.createIndex({"job.title":"text", "job.location":"text","job.description":"text","job.business.name":1,"job.requirements":1})
        Metodo usado para busca de vagas
        :param pass_key:
        :return:
        """
        try:
            a = self.db.find({'$text': {'$search': pass_key}})
            return a
        except Exception as e:
            return e

    def find_email_bussniss(self, id_job):
        """
        Metodo usado pelo controller para conferir se a pessoa é o autor da vaga
        :param id_job:
        :return:
        """
        result = self.db.find_one({'_id': bson.ObjectId(id_job)})
        return result['job']['business']['email']

    def insert_pearson(self, id, name, email):
        """
        Metodo usado para adicionar um novo candidato na vaga
        :param id:
        :param name:
        :param email:
        :return:
        """

        print("banco 1" + str(self.db.update({'_id': bson.ObjectId(id)}, {'$push': {'candidaty': {
                'name': name,
                'email': email,
                'date_apply': strftime("%Y-%m-%d", gmtime())
            }}})))

    def find_id(self, id):
        """
        Meto0do usado para encontrar a vaga a pairtr do id
        :param id:
        :return:
        """
        try:
            result = self.db.find_one({'_id': bson.ObjectId(id)})
            return result
        except Exception as e:
            return e

