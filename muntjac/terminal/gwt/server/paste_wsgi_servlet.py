
from urlparse import urlparse

from os.path import join, dirname, normpath

from paste.httpheaders import \
    (ACCEPT_LANGUAGE, SCRIPT_NAME, PATH_INFO, IF_MODIFIED_SINCE,
     USER_AGENT, CONTENT_LENGTH, CONTENT_TYPE)

from babel import Locale

import muntjac

from muntjac.util import sys_path_install, defaultLocale
# Add 'FakeWebware' to sys path
sys_path_install()

#from paste.webkit.wkservlet import HTTPServlet
from WebKit.HTTPServlet import HTTPServlet


class PasteWsgiServlet(HTTPServlet):

    def __init__(self, contextRoot=None, timeout=1800):
#        super(PasteWsgiServlet, self).__init__()

        if contextRoot is not None:
            self._contextRoot = contextRoot
        else:
            self._contextRoot = join(dirname(muntjac.__file__), '..')

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
        return ''  # default web app


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
        path = join(self._contextRoot, path.lstrip('/'))
        stream = open(normpath(path), 'rb')
        return stream


    def getResource(self, filename):
        # FIXME:
        path = join(self._contextRoot, filename.lstrip('/'))
        return path


    def getResourcePath(self, session, path):
        # FIXME:
        return join(self._contextRoot, path.lstrip('/'))

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


    def getRequestUriPath(self, request):
        """The request's URL from the protocol name up to the query string"""
        return urlparse(request.uri())[2]


    def getRequestUri(self, request):
        return request.uri()


    def getPathInfo(self, request):
        return PATH_INFO(request.environ())


    def getLocale(self, request):
        ## FIXME: implement request.locale()
        tags = ACCEPT_LANGUAGE.parse(request.environ())
        if tags:
            return Locale.parse(tags[0], sep='-')
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
        if allowSessionCreation:
            return request.session()
        else:
            if request.transaction().hasSession():
                return request.session()
            else:
                return None


    def invalidateSession(self, request):
        request.session().invalidate()


    def getSessionId(self, request):
        return request.sessionId()


    def getSessionAttribute(self, session, name, default=None):
        return session.value(name, default)


    def setSessionAttribute(self, session, name, value):
        session.setValue(name, value)


    def getMaxInactiveInterval(self, session):
        return session.value('timeout', self._timeout)


    def isSessionNew(self, session):
        return session.isNew()