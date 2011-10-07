
import sys
import logging
import webbrowser

from os.path import dirname

from wsgiref import simple_server

from paste.deploy import loadapp
from paste.httpserver import serve

from paste.webkit.wsgiapp import sys_path_install
sys_path_install()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
        format="%(levelname)s: %(message)s")

def main():
    wsgi_app = loadapp('config:conf.ini', relative_to=dirname(__file__))

    host = '127.0.0.1'
    port = 8080

    #webbrowser.open('http://%s:%d/SimpleApp' % (host, port), new=0)

    serve(wsgi_app, host=host, port=port)
    #httpd = simple_server.make_server(host, port, wsgi_app)

    # Respond to requests until process is killed
    #httpd.serve_forever()

    # Serve one request, then exit
    #httpd.handle_request()


if __name__ == '__main__':
    main()
