# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

import re
import logging

from muntjac.terminal.gwt.server.exceptions import ServletException

from muntjac.terminal.gwt.server.abstract_application_servlet import \
    AbstractApplicationServlet

from muntjac.util import loadClass


logger = logging.getLogger(__name__)


class ApplicationRunnerServlet(AbstractApplicationServlet):

    def awake(self, transaction):
        super(ApplicationRunnerServlet, self).awake(transaction)

        # The name of the application class currently used. Only valid
        # within one request.
        self._defaultPackages = None

        self._request = None  # ThreadLocal()

        initParameter = self.getApplicationOrSystemProperty('defaultPackages',
                None)
        if initParameter is not None:
            self._defaultPackages = re.split(',', initParameter)


    def respond(self, transaction):
        self._request = transaction.request()

        super(ApplicationRunnerServlet, self).respond(transaction)

        self._request = None


    def getApplicationUrl(self, request):
        path = super(ApplicationRunnerServlet, self).getApplicationUrl(request)

        path += self.getApplicationRunnerApplicationClassName(request)
        path += '/'

        return path


    def getNewApplication(self, request):
        # Creates a new application instance
        try:
            application = self.getApplicationClass()()
            return application
        except TypeError:
            raise ServletException('Failed to load application class: '
                    + self.getApplicationRunnerApplicationClassName(request))


    def getApplicationRunnerApplicationClassName(self, request):
        return self.getApplicationRunnerURIs(request).applicationClassname


    @classmethod
    def getApplicationRunnerURIs(cls, request):
        """Parses application runner URIs.

        If request URL is e.g.
        http://localhost:8080/muntjac/run/muntjac.demo.calc.Calc then

          - context=muntjac
          - Runner servlet=run
          - Muntjac application=muntjac.demo.calc.Calc

        @return: string array containing widgetset URI, application URI and
                context, runner, application classname
        """
        urlParts = re.split('\\/', request.uri())
        context = None
        # String runner = null;
        uris = URIS()
        applicationClassname = None
        contextPath = cls.getContextPath(request)
        if urlParts[1] == re.sub('\\/', '', contextPath):
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

        baseName = self.getApplicationRunnerApplicationClassName(self._request)

        try:
            appClass = loadClass(baseName)
            return appClass
        except Exception:
            if self._defaultPackages is not None:
                for i in range(len(self._defaultPackages)):
                    try:
                        clsName = self._defaultPackages[i] + '.' + baseName
                        appClass = loadClass(clsName)
                    except TypeError:
                        pass  # Ignore as this is expected for many packages
                    except Exception:
                        # TODO: handle exception
                        logger.info('Failed to find application '
                                'class in the default package.')

                    if appClass is not None:
                        return appClass

        raise TypeError, 'class not found exception'


    def getRequestPathInfo(self, request):
        path = self.getPathInfo(request)
        if path is None:
            return None
        clsName = self.getApplicationRunnerApplicationClassName(request)
        path = path[1 + len(clsName):]
        return path


    def getStaticFilesLocation(self, request):
        uris = self._getApplicationRunnerURIs(request)
        staticFilesPath = uris.staticFilesPath
        if staticFilesPath == '/':
            staticFilesPath = ''
        return staticFilesPath


class URIS(object):

    def __init__(self):
        self.staticFilesPath = None
        # self.applicationURI;
        # self.context;
        # self.runner;
        self.applicationClassname = None
