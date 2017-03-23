from app.models.ConnectionFactoryMongo import ConnectionFactoryMongo
import bson, json
from time import strftime, gmtime


class Curriculum:
    """
    Classe para manipulação de dados curriculum
    """

    def __init__(self):
        self.enigma = ConnectionFactoryMongo()
        self.db = self.enigma.get_curriculum()

    def add_curriculum(self, curriculum):
        """
        Adicionar um novo curriculo

        :param curriculum:
        :return:
        """

        return self.db.insert(curriculum)

    def update_curriculum(self, id_curriculum, curriculum):
        """
        Atualizar o curriculo a partir do id

        :param id_curriculum:
        :param curriculum:
        :return:
        """
        try:

            print(

                self.db.update({
                    u'_id': bson.ObjectId(id_curriculum)},
                    {'$set': curriculum}, upsert=False)
            )
        except Exception as e:
            return e

    def drop_curriculum(self, id_curriculum):
        """
        Deletar o curriculum a partir do id

        :param id_curriculum:
        :return:
        """
        try:

            self.db.delete_many({'_id': bson.ObjectId(id_curriculum)})
        except:
            return 'Erro babaca'

    def search_curriculum(self, pass_key):
        """
        Busca por currculim pelo o texto inserido no paramento
        :param pass_key:
        :return:
        """
        try:
            self.db.find({'$text': {'$search': pass_key}})
            return c
        except:
            return {'error': None}

    def list_curriculum(self):
        """
        listar todos os curriculum
        :return:
        """
        try:
            self.db.find().skip(num * 5).limit(5).sort('date_post', pymongo.DESCENDING)
        except BaseException as w:
            return w

    def find_id_curriculum(self, id):
        """
        encontrar por um currilum pelo id
        :param id:
        :return:
        """
        try:

            return self.db.find_one({'_id': bson.ObjectId(id)})
        except Exception as e:
            return e
