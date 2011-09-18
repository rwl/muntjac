# Copyright (C) 2011 Vaadin Ltd
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

from com.vaadin.terminal.gwt.server.AbstractApplicationServlet import (AbstractApplicationServlet,)
# from java.io.IOException import (IOException,)
# from java.net.MalformedURLException import (MalformedURLException,)
# from java.net.URL import (URL,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)
# from javax.servlet.ServletConfig import (ServletConfig,)
# from javax.servlet.ServletException import (ServletException,)
# from javax.servlet.http.HttpServletRequest import (HttpServletRequest,)
# from javax.servlet.http.HttpServletResponse import (HttpServletResponse,)


class ApplicationRunnerServlet(AbstractApplicationServlet):
    _logger = Logger.getLogger(ApplicationRunnerServlet.getName())
    # The name of the application class currently used. Only valid within one
    # request.

    _defaultPackages = None
    _request = ThreadLocal()

    def init(self, servletConfig):
        super(ApplicationRunnerServlet, self).init(servletConfig)
        initParameter = servletConfig.getInitParameter('defaultPackages')
        if initParameter is not None:
            self._defaultPackages = initParameter.split(',')

    def service(self, request, response):
        self._request.set(request)
        super(ApplicationRunnerServlet, self).service(request, response)
        self._request.set(None)

    def getApplicationUrl(self, request):
        url = super(ApplicationRunnerServlet, self).getApplicationUrl(request)
        path = str(url)
        path += self.getApplicationRunnerApplicationClassName(request)
        path += '/'
        return URL(path)

    def getNewApplication(self, request):
        # Creates a new application instance
        try:
            application = self.getApplicationClass()()
            return application
        except IllegalAccessException, e:
            raise ServletException(e)
        except InstantiationException, e:
            raise ServletException(e)
        except ClassNotFoundException, e:
            raise ServletException(self.InstantiationException('Failed to load application class: ' + self.getApplicationRunnerApplicationClassName(request)))

    def getApplicationRunnerApplicationClassName(self, request):
        return self.getApplicationRunnerURIs(request).applicationClassname

    class URIS(object):
        _staticFilesPath = None
        # String applicationURI;
        # String context;
        # String runner;
        _applicationClassname = None

    @classmethod
    def getApplicationRunnerURIs(cls, request):
        """Parses application runner URIs.

        If request URL is e.g.
        http://localhost:8080/vaadin/run/com.vaadin.demo.Calc then
        <ul>
        <li>context=vaadin</li>
        <li>Runner servlet=run</li>
        <li>Vaadin application=com.vaadin.demo.Calc</li>
        </ul>

        @param request
        @return string array containing widgetset URI, application URI and
                context, runner, application classname
        """
        urlParts = str(request.getRequestURI()).split('\\/')
        context = None
        # String runner = null;
        uris = cls.URIS()
        applicationClassname = None
        contextPath = request.getContextPath()
        if urlParts[1] == contextPath.replaceAll('\\/', ''):
            # class name comes after web context and runner application
            context = urlParts[1]
            # runner = urlParts[2];
            if len(urlParts) == 3:
                raise cls.IllegalArgumentException('No application specified')
            applicationClassname = urlParts[3]
            uris.staticFilesPath = '/' + context
            # uris.applicationURI = "/" + context + "/" + runner + "/"
            # + applicationClassname;
            # uris.context = context;
            # uris.runner = runner;
            uris.applicationClassname = applicationClassname
        else:
            # no context
            context = ''
            # runner = urlParts[1];
            if len(urlParts) == 2:
                raise cls.IllegalArgumentException('No application specified')
            applicationClassname = urlParts[2]
            uris.staticFilesPath = '/'
            # uris.applicationURI = "/" + runner + "/" + applicationClassname;
            # uris.context = context;
            # uris.runner = runner;
            uris.applicationClassname = applicationClassname
        return uris

    def getApplicationClass(self):
        # TODO use getClassLoader() ?
        appClass = None
        baseName = self.getApplicationRunnerApplicationClassName(self._request.get())
        try:
            appClass = self.getClass().getClassLoader().loadClass(baseName)
            return appClass
        except Exception, e:
            if self._defaultPackages is not None:
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(self._defaultPackages)):
                        break
                    # Ignore as this is expected for many packages
                    # TODO: handle exception
                    try:
                        appClass = self.getClass().getClassLoader().loadClass(self._defaultPackages[i] + '.' + baseName)
                    except ClassNotFoundException, ee:
                        pass # astStmt: [Stmt([]), None]
                    except Exception, e2:
                        self._logger.log(Level.FINE, 'Failed to find application class in the default package.', e2)
                    if appClass is not None:
                        return appClass
        raise self.ClassNotFoundException()

    def getRequestPathInfo(self, request):
        path = request.getPathInfo()
        if path is None:
            return None
        path = path[1 + len(self.getApplicationRunnerApplicationClassName(request)):]
        return path

    def getStaticFilesLocation(self, request):
        uris = self.getApplicationRunnerURIs(request)
        staticFilesPath = uris.staticFilesPath
        if staticFilesPath == '/':
            staticFilesPath = ''
        return staticFilesPath
