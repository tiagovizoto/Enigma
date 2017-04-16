from app.models.ConnectionFactoryMongo import ConnectionFactoryMongo
import bson, json
from time import strftime, gmtime


class Token:
    """
    Classe para o gerenciamento de tokens
    """
    def __init__(self):
        self.enigma = ConnectionFactoryMongo()

    def insert_token(self, token, email):
        """
        >>Metodo usado para inserir um novo token que foi gerado no controller

        :param token:
        :param email:
        :return:
        """
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
        """
        metodo usado para buscar um token já criado
        :param token:
        :return:
        """
        db = self.enigma.get_token()
        a = db.find_one({'tokens': {'$elemMatch': {'token': token}}})
        print(a)
        return a

    def alter_token(self, token):
        """
        MEtodo usado para mudar o status do token, se está ativo ou inativo

        :param token:
        :return:
        """
        try:
            db = self.enigma.get_token()
            db.update({'token': token}, {'$set': {'active': False}})
        except Exception as e:
            return e

    def list_token(self, email):
        """
        Metodo usado para listar os token de um email

        :param email:
        :return:
        """
        db = self.enigma.get_token()
        try:
            return db.find({'email': email})
        except Exception as e:
            return e
