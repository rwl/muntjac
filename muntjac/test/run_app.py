from os.path import dirname

from paste.deploy import loadapp
from paste.httpserver import serve

wsgi_app = loadapp('config:conf.ini',
                   relative_to=dirname(__file__))

serve(wsgi_app, host='127.0.0.1', port=8080)
