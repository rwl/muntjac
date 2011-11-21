# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

"""Defines a base class for web application contexts that handles the common
tasks."""

import logging
import urllib

from muntjac.service.application_context import IApplicationContext
from muntjac.terminal.gwt.server.web_browser import WebBrowser


logger = logging.getLogger(__name__)


class AbstractWebApplicationContext(IApplicationContext):
    """Base class for web application contexts that handles the common tasks.
    """

    def __init__(self):
        self.listeners = list()
        self.applications = set()
        self.browser = WebBrowser()
        self.applicationToAjaxAppMgrMap = dict()


    def addTransactionListener(self, listener):
        if listener is not None:
            self.listeners.append(listener)


    def removeTransactionListener(self, listener):
        self.listeners.remove(listener)


    def startTransaction(self, application, request):
        """Sends a notification that a transaction is starting.

        @param application:
                   The application associated with the transaction.
        @param request:
                   the HTTP request that triggered the transaction.
        """
        for listener in self.listeners:
            listener.transactionStart(application, request)


    def endTransaction(self, application, request):
        """Sends a notification that a transaction has ended.

        @param application:
                   The application associated with the transaction.
        @param request:
                   the HTTP request that triggered the transaction.
        """
        exceptions = None
        for listener in self.listeners:
            try:
                listener.transactionEnd(application, request)
            except RuntimeError, t:
                if exceptions is None:
                    exceptions = list()
                exceptions.append(t)

        # If any runtime exceptions occurred, throw a combined exception
        if exceptions is not None:
            msg = str()
            for e in exceptions:
                if len(msg) == 0:
                    msg += '\n\n--------------------------\n\n'
                msg += str(e) + '\n'
            raise RuntimeError(msg)


    def valueBound(self, arg0):
        """@see: L{HttpSessionBindingListener.valueBound}"""
        pass  # We are not interested in bindings


    def valueUnbound(self, event):
        """@see: L{HttpSessionBindingListener.valueUnbound}"""
        # If we are going to be unbound from the session, the session
        # must be closing.
        try:
            for app in self.applications:
                app.close()
                self.removeApplication(app)
        except Exception:
            # This should never happen but is possible with rare
            # configurations (e.g. robustness tests). If you have one
            # thread doing HTTP socket write and another thread trying to
            # remove same application here. Possible if you got e.g. session
            # lifetime 1 min but socket write may take longer than 1 min.
            # FIXME: Handle exception
            logger.critical('Could not remove application, leaking memory.')


    def getBrowser(self):
        """Get the web browser associated with this application context.

        Because application context is related to the http session and server
        maintains one session per browser-instance, each context has exactly
        one web browser associated with it.
        """
        return self.browser


    def getApplications(self):
        return self.applications


    def removeApplication(self, application):
        self.applications.remove(application)
        if application in self.applicationToAjaxAppMgrMap:
            del self.applicationToAjaxAppMgrMap[application]


    def generateApplicationResourceURL(self, resource, mapKey):
        filename = resource.getFilename()
        if filename is None:
            return 'app://APP/' + mapKey + '/'
        else:
            # In case serlet container refuses requests containing
            # encoded slashes or backslashes in URLs. Application resource URLs
            # should really be passed in another way than as part of the path
            # in the future.
            encodedFileName = self.urlEncode(filename)
            return "app://APP/" + mapKey + "/" + encodedFileName


    def urlEncode(self, filename):
        return urllib.quote(filename, safe='/\\')


    def isApplicationResourceURL(self, context, relativeUri):
        # If the relative uri is null, we are ready
        if relativeUri is None:
            return False

        # Resolves the prefix
        prefix = relativeUri
        index = relativeUri.find('/')
        if index >= 0:
            prefix = relativeUri[:index]

        # Handles the resource requests
        return prefix == 'APP'


    def getURLKey(self, context, relativeUri):
        index = relativeUri.find('/')
        nxt = relativeUri.find('/', index + 1)
        if nxt < 0:
            return None

        return relativeUri[index + 1:nxt]
