# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""WebKit utility functions.

TODO: Move to PasteWebKit.
"""

import locale
import urlparse

def getContextPath(request):
    ## FIXME: implement request.contextPath()
    return request.serverSideContextPath()


def originalContextPath(request):
    ## FIXME: implement request.originalContextPath()
    return getContextPath(request)


def getServletPath(request):
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


def getLocale(request):
    ## FIXME: implement request.locale()
    l = request.environ().get('Accept-Language')
    if l is None:
        l, _ = locale.getlocale()  # server default
    return l


def serverName(request):
    return request.environ().get('SERVER_NAME', '')


def isSecure(request):
    """Check whether the request is a HTTPS connection."""
    return request.environ().get('HTTPS', '').lower() == 'on'


def serverPort(request):
    portStr = request.environ().get('SERVER_PORT')
    if portStr is not None:
        return int(portStr)
    else:
        return None


def getUrlPath(url):
    """
    @param url: URL of the form scheme://netloc/path;parameters?query#fragment
    @return: the path part or the url
    """
    urlparse(url)[2]


def loadClass(className):
    return (lambda x: getattr(__import__(x.rsplit('.', 1)[0],
                                         fromlist=x.rsplit('.', 1)[0]),
                              x.split('.')[-1]))(className)


def getPathInfo(request):
    return request.extraURLPath()


def getResourceAsStream(servlet, path):
    # FIXME: make relative to context root
    stream = open(path, 'rb')
    return stream


def getSuperClass(cls):
    return cls.__mro__[1] if len(cls.__mro__) > 1 else None
