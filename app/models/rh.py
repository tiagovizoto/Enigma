from app.models.ConnectionFactoryMongo import ConnectionFactoryMongo
import bson, json
from time import strftime, gmtime


class Rh:
    """
    Classe para manipulação dos dados RH
    """
    def __init__(self):
        self.db = ConnectionFactoryMongo().get_job()
        self.db_rh = ConnectionFactoryMongo().get_rh()

    def new_job(self, job):
        """
        Adicionar uma nova vaga
        :param job:
        :return:
        """
        try:
            if job:
                _id = self.db.insert(job)
                return _id
            return False
        except Exception as e:
            return e

    def delete_job(self, id_job):
        """
        Metodo para deletar a vaga pelo id
        :param id_job: id da vaga
        :return: Erro babaca
        """
        try:
            self.db.delete_many({'_id': bson.ObjectId(id_job)})
        except:
            return 'Erro babaca'

    def update_job(self, id_job, date_job):
        """
        Metodo para update de uma vaga apartir do id
        :param id_job: receber a id da vaga
        :param date_job: vaga com os dados atualizado
        :return: returna o erro
        """
        job = date_job
        try:
            print(self.db.update({u'_id': bson.ObjectId(id_job)}, {'$set': {
                'job':{
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
            }
            }, upsert=False)
                  )
        except Exception as e:
            return e

    def my_profile(self, id):
        return self.db_rh.find_one({'_id': bson.ObjectId(id)})

    def create_profile(self, profile):
        return self.db_rh.insert_one(profile)

    def update_profile(self, id_rh,profile):
        return self.db_rh.update({u'_id': bson.ObjectId(id_rh)},{'$set':{profile}})