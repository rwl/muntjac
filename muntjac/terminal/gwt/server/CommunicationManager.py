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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.server.AbstractCommunicationManager import (AbstractCommunicationManager, Callback, Request, Response,)
from com.vaadin.terminal.gwt.server.AbstractApplicationServlet import (AbstractApplicationServlet,)
# from java.io.IOException import (IOException,)
# from java.io.InputStream import (InputStream,)
# from java.io.OutputStream import (OutputStream,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)
# from java.util.UUID import (UUID,)
# from javax.servlet.ServletException import (ServletException,)
# from javax.servlet.http.HttpServletRequest import (HttpServletRequest,)
# from javax.servlet.http.HttpServletResponse import (HttpServletResponse,)
# from javax.servlet.http.HttpSession import (HttpSession,)


class CommunicationManager(AbstractCommunicationManager):
    """Application manager processes changes and paints for single application
    instance.

    This class handles applications running as servlets.

    @see AbstractCommunicationManager

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.0
    """

    class HttpServletRequestWrapper(Request):
        """Concrete wrapper class for {@link HttpServletRequest}.

        @see Request
        """
        _request = None

        def __init__(self, request):
            self._request = request

        def getAttribute(self, name):
            return self._request.getAttribute(name)

        def getContentLength(self):
            return self._request.getContentLength()

        def getInputStream(self):
            return self._request.getInputStream()

        def getParameter(self, name):
            return self._request.getParameter(name)

        def getRequestID(self):
            return 'RequestURL:' + self._request.getRequestURI()

        def getSession(self):
            return self.HttpSessionWrapper(self._request.getSession())

        def getWrappedRequest(self):
            return self._request

        def isRunningInPortlet(self):
            return False

        def setAttribute(self, name, o):
            self._request.setAttribute(name, o)

    class HttpServletResponseWrapper(Response):
        """Concrete wrapper class for {@link HttpServletResponse}.

        @see Response
        """
        _response = None

        def __init__(self, response):
            self._response = response

        def getOutputStream(self):
            return self._response.getOutputStream()

        def getWrappedResponse(self):
            return self._response

        def setContentType(self, type):
            self._response.setContentType(type)

    class HttpSessionWrapper(Session):
        """Concrete wrapper class for {@link HttpSession}.

        @see Session
        """
        _session = None

        def __init__(self, session):
            self._session = session

        def getAttribute(self, name):
            return self._session.getAttribute(name)

        def getMaxInactiveInterval(self):
            return self._session.getMaxInactiveInterval()

        def getWrappedSession(self):
            return self._session

        def isNew(self):
            return self._session.isNew()

        def setAttribute(self, name, o):
            self._session.setAttribute(name, o)

    class AbstractApplicationServletWrapper(Callback):
        _servlet = None

        def __init__(self, servlet):
            self._servlet = servlet

        def criticalNotification(self, request, response, cap, msg, details, outOfSyncURL):
            self._servlet.criticalNotification(request.getWrappedRequest(), response.getWrappedResponse(), cap, msg, details, outOfSyncURL)

        def getRequestPathInfo(self, request):
            return self._servlet.getRequestPathInfo(request.getWrappedRequest())

        def getThemeResourceAsStream(self, themeName, resource):
            return self._servlet.getServletContext().getResourceAsStream('/' + AbstractApplicationServlet.THEME_DIRECTORY_PATH + themeName + '/' + resource)

    def __init__(self, *args):
        """@deprecated use {@link #CommunicationManager(Application)} instead
        @param application
        @param applicationServlet
        ---
        TODO New constructor - document me!

        @param application
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            application, = _0
            super(CommunicationManager, self)(application)
        elif _1 == 2:
            application, applicationServlet = _0
            super(CommunicationManager, self)(application)
        else:
            raise ARGERROR(1, 2)

    def handleFileUpload(self, request, response):
        """Handles file upload request submitted via Upload component.

        @see #getStreamVariableTargetUrl(ReceiverOwner, String, StreamVariable)

        @param request
        @param response
        @throws IOException
        @throws InvalidUIDLSecurityKeyException
        """
        # URI pattern: APP/UPLOAD/[PID]/[NAME]/[SECKEY] See #createReceiverUrl
        pathInfo = request.getPathInfo()
        # strip away part until the data we are interested starts
        startOfData = pathInfo.find(AbstractApplicationServlet.UPLOAD_URL_PREFIX) + len(AbstractApplicationServlet.UPLOAD_URL_PREFIX)
        uppUri = pathInfo[startOfData:]
        parts = uppUri.split('/', 3)
        # 0 = pid, 1= name, 2 = sec key
        variableName = parts[1]
        paintableId = parts[0]
        streamVariable = self._pidToNameToStreamVariable[paintableId].get(variableName)
        secKey = self._streamVariableToSeckey[streamVariable]
        if secKey == parts[2]:
            source = self.getVariableOwner(paintableId)
            contentType = request.getContentType()
            if request.getContentType().contains('boundary'):
                # Multipart requests contain boundary string
                self.doHandleSimpleMultipartFileUpload(self.HttpServletRequestWrapper(request), self.HttpServletResponseWrapper(response), streamVariable, variableName, source, contentType.split('boundary=')[1])
            else:
                # if boundary string does not exist, the posted file is from
                # XHR2.post(File)
                self.doHandleXhrFilePost(self.HttpServletRequestWrapper(request), self.HttpServletResponseWrapper(response), streamVariable, variableName, source, request.getContentLength())
        else:
            raise self.InvalidUIDLSecurityKeyException('Security key in upload post did not match!')

    def handleUidlRequest(self, request, response, applicationServlet, window):
        """Handles UIDL request

        TODO document

        @param request
        @param response
        @param applicationServlet
        @param window
                   target window of the UIDL request, can be null if window not
                   found
        @throws IOException
        @throws ServletException
        """
        self.doHandleUidlRequest(self.HttpServletRequestWrapper(request), self.HttpServletResponseWrapper(response), self.AbstractApplicationServletWrapper(applicationServlet), window)

    def getApplicationWindow(self, request, applicationServlet, application, assumedWindow):
        """Gets the existing application or creates a new one. Get a window within
        an application based on the requested URI.

        @param request
                   the HTTP Request.
        @param application
                   the Application to query for window.
        @param assumedWindow
                   if the window has been already resolved once, this parameter
                   must contain the window.
        @return Window matching the given URI or null if not found.
        @throws ServletException
                    if an exception has occurred that interferes with the
                    servlet's normal operation.
        """
        return self.doGetApplicationWindow(self.HttpServletRequestWrapper(request), self.AbstractApplicationServletWrapper(applicationServlet), application, assumedWindow)

    def handleURI(self, window, request, response, applicationServlet):
        """Calls the Window URI handler for a request and returns the
        {@link DownloadStream} returned by the handler.

        If the window is the main window of an application, the deprecated
        {@link Application#handleURI(java.net.URL, String)} is called first to
        handle {@link ApplicationResource}s and the window handler is only called
        if it returns null.

        @see AbstractCommunicationManager#handleURI(Window, Request, Response,
             Callback)

        @param window
        @param request
        @param response
        @param applicationServlet
        @return
        """
        return self.handleURI(window, self.HttpServletRequestWrapper(request), self.HttpServletResponseWrapper(response), self.AbstractApplicationServletWrapper(applicationServlet))

    def unregisterPaintable(self, p):
        # Cleanup possible receivers
        if self._pidToNameToStreamVariable is not None:
            removed = self._pidToNameToStreamVariable.remove(self.getPaintableId(p))
            if removed is not None:
                for key in removed.keys():
                    self._streamVariableToSeckey.remove(removed[key])
        super(CommunicationManager, self).unregisterPaintable(p)

    _pidToNameToStreamVariable = None
    _streamVariableToSeckey = None

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
        nameToStreamVariable = self._pidToNameToStreamVariable[paintableId]
        if nameToStreamVariable is None:
            nameToStreamVariable = dict()
            self._pidToNameToStreamVariable.put(paintableId, nameToStreamVariable)
        nameToStreamVariable.put(name, value)
        if self._streamVariableToSeckey is None:
            self._streamVariableToSeckey = dict()
        seckey = self._streamVariableToSeckey[value]
        if seckey is None:
            seckey = str(UUID.randomUUID())
            self._streamVariableToSeckey.put(value, seckey)
        return 'app://' + AbstractApplicationServlet.UPLOAD_URL_PREFIX + key + '/' + seckey

    def cleanStreamVariable(self, owner, name):
        nameToStreamVar = self._pidToNameToStreamVariable[self.getPaintableId(owner)]
        nameToStreamVar.remove('name')
        if nameToStreamVar.isEmpty():
            self._pidToNameToStreamVariable.remove(self.getPaintableId(owner))
