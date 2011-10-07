
import sys
import locale
import logging
import webbrowser

from wsgiref.simple_server import make_server

from paste.session import SessionMiddleware


def run_app(applicationClass, host='127.0.0.1', port=8080, nogui=False):

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
            format="%(levelname)s: %(message)s")

    from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet
    wsgi_app = ApplicationServlet(applicationClass, debug=True)

    wsgi_app = SessionMiddleware(wsgi_app)  # wrap in middleware

    if nogui == False:
        webbrowser.open('http://%s:%d/' % (host, port), new=0)

    httpd = make_server(host, port, wsgi_app)

    # Respond to requests until process is killed
    #httpd.serve_forever()
    # Serve one request, then exit
    httpd.handle_request()


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


class Locale(object):

    def __init__(self, lang, country=None, variant=None):
        """
        @param lang: lower-case, two-letter code as defined by ISO-639
        @param country: upper-case, two-letter code as defined by ISO-3166
        @param variant: vendor or browser-specific code (ignored)
        """
        self._language = lang.lower()

        if country is not None:
            country = country.upper()
        self._country = country

        self._variant = variant


    def getLanguage(self):
        return self._language


    def getCountry(self):
        return self._country


    def getVariant(self):
        return self._variant


    @classmethod
    def getDefault(cls):
        lang, _ = locale.getdefaultlocale()
        args = cls.splitCode(lang)
        return Locale(*args)


    @classmethod
    def splitCode(cls, code, sep='_'):
        if sep in code:
            parts = code.split(sep)
            return parts[0], parts[1]
        else:
            return code


    def __str__(self):
        s = self._language
        if self._country is not None:
            s += '_%s' % self._country
        #if self._variant is not None:
        #    s += '_%s' % self._variant
        return s


class EventObject(object):

    def __init__(self, source):
        self._source = source


    def getSource(self):
        return self._source


class IEventListener(object):
    pass