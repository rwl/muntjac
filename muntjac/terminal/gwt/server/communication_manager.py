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

"""Processes changes and paints for single application instance."""

import uuid

from warnings import warn

from muntjac.terminal.gwt.server.abstract_communication_manager import \
    AbstractCommunicationManager, ICallback, IRequest, IResponse, \
    InvalidUIDLSecurityKeyException, ISession

from muntjac.terminal.gwt.server.abstract_application_servlet import \
    AbstractApplicationServlet


class CommunicationManager(AbstractCommunicationManager):
    """Application manager processes changes and paints for single application
    instance.

    This class handles applications running as servlets.

    @see: L{AbstractCommunicationManager}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, application, applicationServlet=None):
        """@deprecated: use L{CommunicationManager} instead
        """
        if applicationServlet is not None:
            warn("deprecated", DeprecationWarning)

        super(CommunicationManager, self).__init__(application)

        self._pidToNameToStreamVariable = None
        self._streamVariableToSeckey = None


    def handleFileUpload(self, request, response, applicationServlet):
        """Handles file upload request submitted via Upload component.

        @see: L{getStreamVariableTargetUrl}
        @raise L{IOException}:
        @raise L{InvalidUIDLSecurityKeyException}:
        """
        # URI pattern: APP/UPLOAD/[PID]/[NAME]/[SECKEY] See #createReceiverUrl

        pathInfo = applicationServlet.getPathInfo(request)
        # strip away part until the data we are interested starts
        startOfData = \
                pathInfo.find(AbstractApplicationServlet.UPLOAD_URL_PREFIX) \
                + len(AbstractApplicationServlet.UPLOAD_URL_PREFIX)
        uppUri = pathInfo[startOfData:]
        parts = uppUri.split('/', 3)  # 0 = pid, 1= name, 2 = sec key
        variableName = parts[1]
        paintableId = parts[0]

        streamVariable = self._pidToNameToStreamVariable.get(
                paintableId).get(variableName)
        secKey = self._streamVariableToSeckey.get(streamVariable)
        if secKey == parts[2]:

            source = self.getVariableOwner(paintableId)
            contentType = applicationServlet.getContentType(request)
            if 'boundary' in applicationServlet.getContentType(request):
                # Multipart requests contain boundary string
                self.doHandleSimpleMultipartFileUpload(
                        HttpServletRequestWrapper(request,
                                applicationServlet),
                        HttpServletResponseWrapper(response,
                                applicationServlet),
                        streamVariable,
                        variableName,
                        source,
                        contentType.split('boundary=')[1])
            else:
                # if boundary string does not exist, the posted file is from
                # XHR2.post(File)
                self.doHandleXhrFilePost(
                        HttpServletRequestWrapper(request,
                                applicationServlet),
                        HttpServletResponseWrapper(response,
                                applicationServlet),
                        streamVariable,
                        variableName,
                        source,
                        applicationServlet.getContentType(request))
        else:
            raise InvalidUIDLSecurityKeyException, \
                    'Security key in upload post did not match!'


    def handleUidlRequest(self, request, response, applicationServlet, window):
        """Handles UIDL request.

        @param request:
        @param response:
        @param applicationServlet:
        @param window:
                   target window of the UIDL request, can be null if window
                   not found
        @raise IOException:
        @raise ServletException:
        """
        self.doHandleUidlRequest(
                HttpServletRequestWrapper(request, applicationServlet),
                HttpServletResponseWrapper(response, applicationServlet),
                AbstractApplicationServletWrapper(applicationServlet),
                window)


    def getApplicationWindow(self, request, applicationServlet,
                application, assumedWindow):
        """Gets the existing application or creates a new one. Get a window
        within an application based on the requested URI.

        @param request:
                   the HTTP Request.
        @param application:
                   the Application to query for window.
        @param assumedWindow:
                   if the window has been already resolved once, this
                   parameter must contain the window.
        @return: Window matching the given URI or null if not found.
        @raise ServletException:
                    if an exception has occurred that interferes with the
                    servlet's normal operation.
        """
        return self.doGetApplicationWindow(
                HttpServletRequestWrapper(request, applicationServlet),
                AbstractApplicationServletWrapper(applicationServlet),
                application,
                assumedWindow)


    def handleURI(self, window, request, response, applicationServlet):
        """Calls the Window URI handler for a request and returns the
        L{DownloadStream} returned by the handler.

        If the window is the main window of an application, the deprecated
        L{Application.handleURI} is called first to handle
        L{ApplicationResource}s and the window handler is only called if
        it returns C{None}.

        @see: L{AbstractCommunicationManager.handleURI}
        """
        return AbstractCommunicationManager.handleURI(self, window,
                HttpServletRequestWrapper(request, applicationServlet),
                HttpServletResponseWrapper(response, applicationServlet),
                AbstractApplicationServletWrapper(applicationServlet))


    def unregisterPaintable(self, p):
        # Cleanup possible receivers
        if self._pidToNameToStreamVariable is not None:
            removed = self._pidToNameToStreamVariable.pop(
                    self.getPaintableId(p), None)
            if removed is not None:
                self._streamVariableToSeckey.pop(removed, None)

        super(CommunicationManager, self).unregisterPaintable(p)


    def getStreamVariableTargetUrl(self, owner, name, value):
        # We will use the same APP/* URI space as ApplicationResources but
        # prefix url with UPLOAD
        #
        # eg. APP/UPLOAD/[PID]/[NAME]/[SECKEY]
        #
        # SECKEY is created on each paint to make URL's unpredictable (to
        # prevent CSRF attacks).
        #
        # NAME and PID from URI forms a key to fetch StreamVariable when
        # handling post
        paintableId = self.getPaintableId(owner)
        key = paintableId + '/' + name

        if self._pidToNameToStreamVariable is None:
            self._pidToNameToStreamVariable = dict()

        nameToStreamVariable = self._pidToNameToStreamVariable.get(paintableId)
        if nameToStreamVariable is None:
            nameToStreamVariable = dict()
            self._pidToNameToStreamVariable[paintableId] = nameToStreamVariable
        nameToStreamVariable[name] = value

        if self._streamVariableToSeckey is None:
            self._streamVariableToSeckey = dict()

        seckey = self._streamVariableToSeckey.get(value)
        if seckey is None:
            seckey = str(uuid.uuid4())
            self._streamVariableToSeckey[value] = seckey

        return ('app://' + AbstractApplicationServlet.UPLOAD_URL_PREFIX
                + key + '/' + seckey)


    def cleanStreamVariable(self, owner, name):
        nameToStreamVar = self._pidToNameToStreamVariable.get(
                self.getPaintableId(owner))
        if 'name' in nameToStreamVar:
            del nameToStreamVar['name']
        if len(nameToStreamVar) == 0:
            if self.getPaintableId(owner) in self._pidToNameToStreamVariable:
                del self._pidToNameToStreamVariable[self.getPaintableId(owner)]


class HttpServletRequestWrapper(IRequest):
    """Concrete wrapper class for L{HttpServletRequest}.

    @see: L{IRequest}
    """

    def __init__(self, request, applicationServlet):
        self._request = request
        self.servlet = applicationServlet


    def getAttribute(self, name, default=''):
        return self.servlet.getParameter(self._request, name, default)


    def getContentLength(self):
        return self.servlet.getContentLength(self._request)


    def getInputStream(self):
        return self.servlet.getInputStream(self._request)


    def getParameter(self, name):
        return self.servlet.getParameter(self._request, name, None)


    def getRequestID(self):
        return 'RequestURL:' + self.servlet.getRequestUri(self._request)


    def getSession(self):
        session = self.servlet.getSession(self._request)
        return HttpSessionWrapper(session, self.servlet)


    def getWrappedRequest(self):
        return self._request


    def getWrappedServlet(self):
        return self.servlet


    def isRunningInPortlet(self):
        return False


    def setAttribute(self, name, o):
        self.servlet.setParameter(self._request, name, o)


class HttpServletResponseWrapper(IResponse):
    """Concrete wrapper class for L{HttpServletResponse}.

    @see: L{IResponse}
    """

    def __init__(self, response, applicationServlet):
        self._response = response
        self.servlet = applicationServlet


    def getOutputStream(self):
        return self.servlet.getOutputStream(self._response)


    def getWrappedResponse(self):
        return self._response


    def getWrappedServlet(self):
        return self.servlet


    def setContentType(self, typ):
        self.servlet.setHeader(self._response, 'Content-Type', typ)


class HttpSessionWrapper(ISession):
    """Concrete wrapper class for L{HttpSession}.

    @see: L{ISession}
    """

    def __init__(self, session, applicationServlet):
        self._session = session
        self.servlet = applicationServlet


    def getAttribute(self, name, default=None):
        return self.servlet.getSessionAttribute(self._session, name, default)


    def getMaxInactiveInterval(self):
        """maximum time interval, in seconds, between client accesses"""
        return self.servlet.getMaxInactiveInterval(self._session)


    def getWrappedSession(self):
        return self._session


    def getWrappedServlet(self):
        return self.servlet


    def isNew(self):
        return self.servlet.isSessionNew(self._session)


    def setAttribute(self, name, value):
        self.servlet.setSessionAttribute(self._session, name, value)


class AbstractApplicationServletWrapper(ICallback):

    def __init__(self, servlet):
        self.servlet = servlet


    def criticalNotification(self, request, response, cap, msg,
                details, outOfSyncURL):

        self.servlet.criticalNotification(request.getWrappedRequest(),
                response.getWrappedResponse(), cap, msg, details, outOfSyncURL)


    def getRequestPathInfo(self, request):
        return self.servlet.getRequestPathInfo(request.getWrappedRequest())


    def getThemeResourceAsStream(self, themeName, resource):
        return self.servlet.getResourceAsStream(
                ('/' + AbstractApplicationServlet.THEME_DIRECTORY_PATH
                + themeName + '/' + resource))
