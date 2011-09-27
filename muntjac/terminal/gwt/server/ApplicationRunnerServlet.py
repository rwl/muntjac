# Copyright (C) 2010 IT Mill Ltd.
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

import logging

from muntjac.terminal.gwt.server.AbstractApplicationServlet import AbstractApplicationServlet
from muntjac.terminal.gwt.server.ServletException import ServletException


class ApplicationRunnerServlet(AbstractApplicationServlet):

    _logger = logging.getLogger('.'.join(__package__, __class__.__name__))

    def init(self, servletConfig):
        super(ApplicationRunnerServlet, self).init(servletConfig)

        # The name of the application class currently used. Only valid within one
        # request.
        self._defaultPackages = None
        self._request = None  # ThreadLocal()

        initParameter = servletConfig.getInitParameter('defaultPackages')
        if initParameter is not None:
            self._defaultPackages = initParameter.split(',')


    def service(self, request, response):
        self._request = request
        super(ApplicationRunnerServlet, self).service(request, response)
        self._request = None


    def getApplicationUrl(self, request):
        url = super(ApplicationRunnerServlet, self).getApplicationUrl(request)

        path = url
        path += self.getApplicationRunnerApplicationClassName(request)
        path += '/'

        return path


    def getNewApplication(self, request):
        # Creates a new application instance
        try:
            application = self.getApplicationClass()()
            return application
        except TypeError:
            raise ServletException('Failed to load application class: ' \
                    + self.getApplicationRunnerApplicationClassName(request))


    def _getApplicationRunnerApplicationClassName(self, request):
        return self.getApplicationRunnerURIs(request).applicationClassname


    @classmethod
    def _getApplicationRunnerURIs(cls, request):
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
        urlParts = request.uri().split('\\/')
        context = None
        # String runner = null;
        uris = URIS()
        applicationClassname = None
        contextPath = request.contextPath()
        if urlParts[1] == contextPath.replaceAll('\\/', ''):
            # class name comes after web context and runner application
            context = urlParts[1]
            # runner = urlParts[2]
            if len(urlParts) == 3:
                raise ValueError, 'No application specified'

            applicationClassname = urlParts[3]

            uris.staticFilesPath = '/' + context
            # uris.applicationURI = "/" + context + "/" + runner + "/"
            # + applicationClassname
            # uris.context = context
            # uris.runner = runner
            uris.applicationClassname = applicationClassname
        else:
            # no context
            context = ''
            # runner = urlParts[1];
            if len(urlParts) == 2:
                raise ValueError, 'No application specified'

            applicationClassname = urlParts[2]

            uris.staticFilesPath = '/'
            # uris.applicationURI = "/" + runner + "/" + applicationClassname
            # uris.context = context
            # uris.runner = runner
            uris.applicationClassname = applicationClassname

        return uris


    def getApplicationClass(self):
        appClass = None

        baseName = self._getApplicationRunnerApplicationClassName(self._request)  #@PydevCodeAnalysisIgnore

        try:
            exec 'appClass = baseName()'
            return appClass
        except Exception:
            if self._defaultPackages is not None:
                for _ in range(len(self._defaultPackages)):
                    try:
                        exec "appClass = (self._defaultPackages[i] + '.' + baseName)()"
                    except TypeError:
                        # Ignore as this is expected for many packages
                        pass
                    except Exception:
                        # TODO: handle exception
                        self._logger.info('Failed to find application class in the default package.')

                    if appClass is not None:
                        return appClass

        raise TypeError, 'class not found exception'


    def getRequestPathInfo(self, request):
        path = request.extraURLPath()
        if path is None:
            return None
        path = path[1 + len(self.getApplicationRunnerApplicationClassName(request)):]
        return path


    def getStaticFilesLocation(self, request):
        uris = self._getApplicationRunnerURIs(request)
        staticFilesPath = uris.staticFilesPath
        if staticFilesPath == '/':
            staticFilesPath = ''

        return staticFilesPath


class URIS(object):
    staticFilesPath = None
    # String applicationURI;
    # String context;
    # String runner;
    applicationClassname = None
