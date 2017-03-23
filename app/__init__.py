from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app.controllers import default
from app.controllers import rh
from app.controllers import candidate
from app.controllers import admin