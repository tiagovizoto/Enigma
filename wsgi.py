from run import app

import sys
sys.path.insert(0, '/var/www/enigmajob/')
application = app
activate_this = '/var/www/enigmajob/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))