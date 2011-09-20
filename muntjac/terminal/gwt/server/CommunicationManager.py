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

import uuid

from muntjac.terminal.gwt.server.AbstractCommunicationManager import AbstractCommunicationManager, Callback, Request, Response, InvalidUIDLSecurityKeyException,\
    Session
from muntjac.terminal.gwt.server.AbstractApplicationServlet import AbstractApplicationServlet


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

    def __init__(self, application, applicationServlet=None):
        """@deprecated use {@link #CommunicationManager(Application)} instead
        @param application
        @param applicationServlet
        ---
        TODO New constructor - document me!

        @param application
        """
        if applicationServlet is not None:
            raise DeprecationWarning

        super(CommunicationManager, self)(application)

        self._pidToNameToStreamVariable = None
        self._streamVariableToSeckey = None


    def handleFileUpload(self, request, response):
        """Handles file upload request submitted via Upload component.

        @see #getStreamVariableTargetUrl(ReceiverOwner, String, StreamVariable)

        @param request
        @param response
        @throws IOException
        @throws InvalidUIDLSecurityKeyException
        """
        # URI pattern: APP/UPLOAD/[PID]/[NAME]/[SECKEY] See #createReceiverUrl

        pathInfo = request.extraURLPath()
        # strip away part until the data we are interested starts
        startOfData = pathInfo.find(AbstractApplicationServlet.UPLOAD_URL_PREFIX) \
                + len(AbstractApplicationServlet.UPLOAD_URL_PREFIX)
        uppUri = pathInfo[startOfData:]
        parts = uppUri.split('/', 3)  # 0 = pid, 1= name, 2 = sec key
        variableName = parts[1]
        paintableId = parts[0]

        streamVariable = self._pidToNameToStreamVariable.get(paintableId).get(variableName)
        secKey = self._streamVariableToSeckey[streamVariable]
        if secKey == parts[2]:

            source = self.getVariableOwner(paintableId)
            contentType = request.getHeader('Content-type')
            if 'boundary' in request.getHeader('Content-type'):
                # Multipart requests contain boundary string
                self.doHandleSimpleMultipartFileUpload(HttpServletRequestWrapper(request),
                                                       HttpServletResponseWrapper(response),
                                                       streamVariable,
                                                       variableName,
                                                       source,
                                                       contentType.split('boundary=')[1])
            else:
                # if boundary string does not exist, the posted file is from
                # XHR2.post(File)
                self.doHandleXhrFilePost(HttpServletRequestWrapper(request),
                                         HttpServletResponseWrapper(response),
                                         streamVariable,
                                         variableName,
                                         source,
                                         request.getHeader('Content-Length'))
        else:
            raise InvalidUIDLSecurityKeyException, 'Security key in upload post did not match!'


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
        self.doHandleUidlRequest(HttpServletRequestWrapper(request),
                                 HttpServletResponseWrapper(response),
                                 AbstractApplicationServletWrapper(applicationServlet),
                                 window)


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
        return self.doGetApplicationWindow(HttpServletRequestWrapper(request),
                                           AbstractApplicationServletWrapper(applicationServlet),
                                           application, assumedWindow)


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
        return self.handleURI(window,
                              HttpServletRequestWrapper(request),
                              HttpServletResponseWrapper(response),
                              AbstractApplicationServletWrapper(applicationServlet))


    def unregisterPaintable(self, p):
        # Cleanup possible receivers
        if self._pidToNameToStreamVariable is not None:
            removed = self._pidToNameToStreamVariable.pop(self.getPaintableId(p), None)
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

        nameToStreamVariable = self._pidToNameToStreamVariable[paintableId]
        if nameToStreamVariable is None:
            nameToStreamVariable = dict()
            self._pidToNameToStreamVariable[paintableId] = nameToStreamVariable
        nameToStreamVariable[name] = value

        if self._streamVariableToSeckey is None:
            self._streamVariableToSeckey = dict()
        seckey = self._streamVariableToSeckey[value]
        if seckey is None:
            seckey = str(uuid.uuid4())
            self._streamVariableToSeckey[value] = seckey

        return 'app://' + AbstractApplicationServlet.UPLOAD_URL_PREFIX + key + '/' + seckey


    def cleanStreamVariable(self, owner, name):
        nameToStreamVar = self._pidToNameToStreamVariable[self.getPaintableId(owner)]
        nameToStreamVar.pop('name')
        if len(nameToStreamVar) == 0:
            self._pidToNameToStreamVariable.pop(self.getPaintableId(owner))


class HttpServletRequestWrapper(Request):
    """Concrete wrapper class for {@link HttpServletRequest}.

    @see Request
    """

    def __init__(self, request):
        self._request = request


    def getAttribute(self, name):
        return self._request.field(name)


    def getContentLength(self):
        return self._request.getHeader('Content-Length')


    def getInputStream(self):
        return self._request.rawInput()


    def getParameter(self, name):
        return self._request.field(name)


    def getRequestID(self):
        return 'RequestURL:' + self._request.uri()


    def getSession(self):
        return HttpSessionWrapper(self._request.session())


    def getWrappedRequest(self):
        return self._request


    def isRunningInPortlet(self):
        return False


    def setAttribute(self, name, o):
        self._request.setField(name, o)


class HttpServletResponseWrapper(Response):
    """Concrete wrapper class for {@link HttpServletResponse}.

    @see Response
    """

    def __init__(self, response):
        self._response = response


    def getOutputStream(self):
        return self._response


    def getWrappedResponse(self):
        return self._response


    def setContentType(self, typ):
        self._response.setHeader('Content-Type', typ)


class HttpSessionWrapper(Session):
    """Concrete wrapper class for {@link HttpSession}.

    @see Session
    """

    def __init__(self, session):
        self._session = session


    def getAttribute(self, name):
        return self._session.value(name)


    def getMaxInactiveInterval(self):
        return self._session.timeout()


    def getWrappedSession(self):
        return self._session


    def isNew(self):
        return self._session.isNew()


    def setAttribute(self, name, o):
        self._session.setValue(name, o)


class AbstractApplicationServletWrapper(Callback):

    def __init__(self, servlet):
        self._servlet = servlet


    def criticalNotification(self, request, response, cap, msg, details, outOfSyncURL):
        self._servlet.criticalNotification(request.getWrappedRequest(),
                                           response.getWrappedResponse(),
                                           cap, msg, details, outOfSyncURL)


    def getRequestPathInfo(self, request):
        return self._servlet.getRequestPathInfo(request.getWrappedRequest())


    def getThemeResourceAsStream(self, themeName, resource):
        return self._servlet.getServletContext().getResourceAsStream('/' \
                + AbstractApplicationServlet.THEME_DIRECTORY_PATH \
                + themeName + '/' + resource)
