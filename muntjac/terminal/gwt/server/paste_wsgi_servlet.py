
import logging

from urlparse import urlparse

from os.path import join, dirname, normpath

try:
    from cPickle import UnpicklingError
except ImportError:
    from pickle import UnpicklingError

from paste.httpheaders import \
    (ACCEPT_LANGUAGE, SCRIPT_NAME, PATH_INFO, IF_MODIFIED_SINCE,
     USER_AGENT, CONTENT_LENGTH, CONTENT_TYPE)

from babel.core import Locale, UnknownLocaleError

import muntjac

from muntjac.util import sys_path_install, defaultLocale
# Add 'FakeWebware' to sys path
sys_path_install()

#from paste.webkit.wkservlet import HTTPServlet
from WebKit.HTTPServlet import HTTPServlet


logger = logging.getLogger(__name__)


class EndResponseException(Exception):
    pass


class PasteWsgiServlet(HTTPServlet):

    EndResponse = EndResponseException

    def __init__(self, contextRoot=None, contextPath=None, timeout=1800):
#        super(PasteWsgiServlet, self).__init__()

        if contextRoot is not None:
            self.contextRoot = contextRoot
        else:
            root = join(dirname(muntjac.__file__), 'public')
            self.contextRoot = normpath(root)

        self.contextPath = contextPath if contextPath is not None else ''

        self._timeout = timeout


#    def __call__(self, environ, start_response):
#        pass

    def awake(self, transaction):
#        super(PasteWsgiServlet, self).awake(transaction)

        self.init()


    def respond(self, transaction):
#        super(PasteWsgiServlet, self).respond(transaction)

        self.service(transaction.request(), transaction.response())


    def init(self):
        raise NotImplementedError


    def service(self, request, response):
        raise NotImplementedError


    def getContextPath(self, request):
        ## FIXME: implement request.contextPath()
        return self.contextPath


    def originalContextPath(self, request):
        ## FIXME: implement request.originalContextPath()
        return self.getContextPath(request)


    def getServletPath(self, request):
        ## FIXME: implement request.servletPath()
        servletPath = SCRIPT_NAME(request.environ())
#        pathInfo = PATH_INFO(request.environ())
#
#        if 'REQUEST_URI' in request.environ():
#            uri = request.environ()['REQUEST_URI']
#            # correct servletPath if there was a redirection
#            if not (uri + '/').startswith(servletPath + '/'):
#                i = uri.find(pathInfo)
#                servletPath = i > 0 and uri[:i] or ''

        return servletPath


    def getUrlPath(self, url):
        """
        @param url: URL of the form scheme://netloc/path;parameters?query#frag
        @return: the path part or the url
        """
        return urlparse(url)[2]  # FIXME remove URL query


    def getResourceAsStream(self, path):
        # FIXME:
        path = join(self.contextRoot, path.lstrip('/'))
        stream = open(normpath(path), 'rb')
        return stream


    def getResource(self, filename):
        # FIXME:
        path = join(self.contextRoot, filename.lstrip('/'))
        return path


    def getResourcePath(self, session, path):
        # FIXME:
        return join(self.contextRoot, path.lstrip('/'))

    # Request

    def getParameters(self, request):
        return request.fields()


    def getParameter(self, request, key, default=''):
        return request.field(key, default)


    def setParameter(self, request, key, value):
        request.setField(key, value)


    def getHeader(self, request, field):
        return request.serverDictionary().get(field)


    def getUserAgent(self, request):
        return USER_AGENT(request.environ())


    def getContentLength(self, request):
        return CONTENT_LENGTH(request.environ())


    def getContentType(self, request):
        return CONTENT_TYPE(request.environ())


    def getIfModifiedSince(self, request):
        dh = IF_MODIFIED_SINCE(request.environ())
        return int(dh) if dh else -1


    def getServerPort(self, request):
        portStr = request.environ().get('SERVER_PORT')
        return int(portStr) if portStr is not None else None


    def getRequestUri(self, request):
        """The request's URL from the protocol name up to the query string"""
        return urlparse(request.uri())[2]


    def getPathInfo(self, request):
        return PATH_INFO(request.environ())


    def getLocale(self, request):
        ## FIXME: implement request.locale()
        tags = ACCEPT_LANGUAGE.parse(request.environ())
        if tags:
            try:
                return Locale.parse(tags[0], sep='-')
            except UnknownLocaleError, e:
                try:
                    return Locale.parse(tags[0])
                except UnknownLocaleError, e:
                    logger.error('Locale parsing error: %s' % e)
                    return defaultLocale()
        else:
            return defaultLocale()  # server default


    def getServerName(self, request):
        return request.environ().get('SERVER_NAME', '')


    def isSecure(self, request):
        """Check whether the request is a HTTPS connection."""
        return request.environ().get('HTTPS', '').lower() == 'on'


    def getInputStream(self, request):
        return request.rawInput()

    # Response

    def setHeader(self, response, name, value):
        response.setHeader(name, value)


    def setStatus(self, response, n, msg=''):
        response.setStatus(n, msg)


    def write(self, response, value):
        response.write(value)


    def redirect(self, response, url):
        response.sendRedirect(url)


    def getOutputStream(self, response):
        return response

    # Session

    def getSession(self, request, allowSessionCreation=True):
        try:
            if allowSessionCreation:
                return request.session()
            else:
                if request.transaction().hasSession():
                    return request.session()
                else:
                    return None
        except EOFError, e:
            logger.exception('Session retrieval error: %s' % str(e))
            return None
        except UnpicklingError, e:
            logger.exception('Session retrieval error: %s' % str(e))
            return None
        except ValueError, e:
            logger.exception('Session retrieval error: %s' % str(e))
            return None


    def invalidateSession(self, request):
        try:
            request.session().invalidate()
        except Exception, e:
            logger.error('Session invalidation error: %s' % e)


    def getSessionId(self, request):
        try:
            return request.sessionId()
        except Exception, e:
            logger.error('Session ID error: %s' % e)
            return None


    def getSessionAttribute(self, session, name, default=None):
        if session is not None:
            return session.value(name, default)
        else:
            return default


    def setSessionAttribute(self, session, name, value):
        if session is not None:
            session.setValue(name, value)


    def getMaxInactiveInterval(self, session):
        if session is not None:
            return session.value('timeout', self._timeout)
        else:
            return self._timeout


    def isSessionNew(self, session):
        if session is not None:
            return session.isNew()
        else:
            return True
