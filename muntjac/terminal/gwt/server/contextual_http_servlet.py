
import locale
from urlparse import urlparse

from os.path import join, dirname

from muntjac.util import sys_path_install

from paste.httpheaders import \
    ACCEPT_LANGUAGE, SCRIPT_NAME, PATH_INFO, IF_MODIFIED_SINCE

import muntjac
from muntjac.util import Locale

# Add 'FakeWebware' to sys path
sys_path_install()

#from paste.webkit.wkservlet import HTTPServlet
from WebKit.HTTPServlet import HTTPServlet


class ContextualHttpServlet(HTTPServlet):

    def __init__(self, contextRoot=None):

        if contextRoot is not None:
            self._contextRoot = contextRoot
        else:
            self._contextRoot = join(dirname(muntjac.__file__), '..')


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


    def getHeader(self, request, field):
        return request.serverDictionary().get(field)


    def getLocale(self, request):
        ## FIXME: implement request.locale()
        tags = ACCEPT_LANGUAGE.parse(request.environ())
        if tags:
            args = Locale.splitCode(tags[0], sep='-')
            return Locale(*args)
        else:
            return Locale.getDefault()  # server default


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


    def getServerName(self, request):
        return request.environ().get('SERVER_NAME', '')


    def isSecure(self, request):
        """Check whether the request is a HTTPS connection."""
        return request.environ().get('HTTPS', '').lower() == 'on'


    def getServerPort(self, request):
        portStr = request.environ().get('SERVER_PORT')
        if portStr is not None:
            return int(portStr)
        else:
            return None


    def getDateHeader(self, request):
        dh = IF_MODIFIED_SINCE(request.environ())
        if dh:
            return int(dh)
        else:
            return -1


    def getUrlPath(self, url):
        """
        @param url: URL of the form scheme://netloc/path;parameters?query#fragment
        @return: the path part or the url
        """
        return urlparse(url)[2]  # FIXME remove URL query


    def getRequestURI(self, request):
        """The request's URL from the protocol name up to the query string"""
        return urlparse(request.uri())[2]


    def getPathInfo(self, request):
        return PATH_INFO(request.environ())


    def getResourceAsStream(self, path):
        # FIXME:
        stream = open(join(self._contextRoot, path.lstrip('/')), 'rb')
        return stream


    def getResource(self, filename):
        # FIXME:
        path = join(self._contextRoot, filename.lstrip('/'))
        return path


    def getResourcePath(self, session, path):
        # FIXME:
        return join(self._contextRoot, path.lstrip('/'))
