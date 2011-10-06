
import sys
import logging
import webbrowser

from wsgiref.simple_server import make_server

from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet


def run_app(applicationClass, host='127.0.0.1', port=8080, nogui=False):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
            format="%(levelname)s: %(message)s")

    wsgi_app = ApplicationServlet(applicationClass, debug=True)

    if nogui == False:
        webbrowser.open('http://%s:%d/' % (host, port), new=0)

    httpd = make_server(host, port, wsgi_app)

    # Respond to requests until process is killed
    httpd.serve_forever()


def loadClass(className):
    return (lambda x: getattr(__import__(x.rsplit('.', 1)[0],
                                         fromlist=x.rsplit('.', 1)[0]),
                              x.split('.')[-1]))(className)


def getSuperClass(cls):
    return cls.__mro__[1] if len(cls.__mro__) > 1 else None


def clsname(cls):
    """@return: fully qualified name of given class"""
    return cls.__module__ + "." + cls.__name__


def fullname(obj):
    """@return fully qualified name of given object's class"""
    return clsname(obj.__class__)
