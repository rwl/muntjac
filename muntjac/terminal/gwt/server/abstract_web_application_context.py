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
