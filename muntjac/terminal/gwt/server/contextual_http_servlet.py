
import locale
import urlparse

from paste.webkit.wsgiapp import sys_path_install

# Add 'FakeWebware' to sys path
sys_path_install()

from WebKit.HTTPServlet import HTTPServlet  #@PydevCodeAnalysisIgnore


class ContextualHttpServlet(HTTPServlet):

    def getContextPath(self, request):
        ## FIXME: implement request.contextPath()
        return request.serverSideContextPath()


    def originalContextPath(self, request):
        ## FIXME: implement request.originalContextPath()
        return self.getContextPath(request)


    def getServletPath(self, request):
        ## FIXME: implement request.servletPath()
        servletPath = request.environ().get('SCRIPT_NAME', '')
        pathInfo = request.environ().get('PATH_INFO', '')

        if 'REQUEST_URI' in request.environ():
            uri = request.environ()['REQUEST_URI']
            # correct servletPath if there was a redirection
            if not (uri + '/').startswith(servletPath + '/'):
                i = uri.find(pathInfo)
                servletPath = i > 0 and uri[:i] or ''

        return servletPath


    def getLocale(self, request):
        ## FIXME: implement request.locale()
        l = request.environ().get('Accept-Language')
        if l is None:
            l, _ = locale.getlocale()  # server default
        return l


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


    def getUrlPath(self, url):
        """
        @param url: URL of the form scheme://netloc/path;parameters?query#fragment
        @return: the path part or the url
        """
        urlparse(url)[2]



    def getPathInfo(self, request):
        return request.extraURLPath()


    def getResourceAsStream(self, path):
        # FIXME: make relative to context root
        stream = open(path, 'rb')
        return stream


    def getResourcePath(self, session, path):
        # FIXME: make relative to context root
        return path
