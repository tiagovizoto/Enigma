from sendgrid import *
import base64
from datetime import datetime
import random

from config import KEY_SENDMAIL


class SendGridEmail:
    """
    Class responsabilite from send of email general.
    Use web api v3 by SendGrid
    """

    def send_me(self, name, email, message):
        sg = sendgrid.SendGridAPIClient(apikey=KEY_SENDMAIL)
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": "tiagovizoto@yahoo.com.br"
                        }
                    ],
                    "subject": "Hello Worffffffffld from the SendGrid Python Library!"
                }
            ],
            "from": {
                "email": str(email)
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": str("Messsagem: %s   Nome: %s E-mail: %s" % (message,name,email))
                }
            ]
        }
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def send_rh(self, nome, email, message,curriculum, emailRH, id_job,title):

        """with open("c.pdf", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        attachment = Attachment()
        attachment.set_content(str(encoded_string))
        attachment.set_type("application/pdf")
        attachment.set_filename("c.pdf")
        attachment.set_disposition("attachment")
        attachment.set_content_id("Balance Sheet")
        mail.add_attachment(attachment)"""

        with open(curriculum, 'rb') as f:
            file = f.read()
            f.close()

        encoded = base64.b64encode(file).decode('ascii')
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": emailRH
                        }
                    ],
                    "subject": str("Curriculo para a Vaga %s" % (title))
                }
            ],
            "from": {
                "email": "tiagovizoto@enigmajob.xyz"
            },
            "attachments": [
                {
                    "content": encoded,
                    "filename": str("%s.pdf" %nome),
                    "name": "c",
                    "type": "pdf"
                }
            ],
            "content": [
                {
                    "type": "text/HTML",
                    "value": "Nova Canditadura na vaga %s <br> Nome: %s <br> Messagem: %s <br><br> Email:  %s  <br><br><br><br>EnigmaJob.xyz Simples e Eficiente" % (id_job, nome, message,email)
                }
            ]
        }

        print(str(encoded))
        print(type(data))
        sg = sendgrid.SendGridAPIClient(apikey=KEY_SENDMAIL)
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.headers)
        print(response.body)

    def send_token(self, token, email):
        sg = sendgrid.SendGridAPIClient(apikey=KEY_SENDMAIL)
        data = {
            "personalizations": [
                {
                    "to": [
                        {
                            "email": email
                        }
                    ],
                    "subject": "EnigmaJob : Token para o acesso Administrativo das Vagas    "
                }
            ],
            "from": {
                "email": "tiago@enigma.xyz"
            },
            "content": [
                {
                    "type": "text/HTML",
                            "value": str("<h1>EnigmaJob</h1> "
                                         "<b style='color:red'> O Token tem validade de 48 horas "
                                         "e é só valido para as vagas postadas com seu email %s. </b><br>"
                                         "<h4>Segue o seu Token para o acesso: %s "
                                         "</h4>ou pelo o http://www.enigmajob.xyz/manager/%s<br>"
                                          %(email,token,token)
                                         )
                }
            ]
        }
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.headers)
        print(response.body)


''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQSRVTUWYZ') for i in range(18))



