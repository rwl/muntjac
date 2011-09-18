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

from com.vaadin.terminal.gwt.server.AbstractCommunicationManager import (AbstractCommunicationManager, Callback, Request, Response,)
from com.vaadin.terminal.gwt.server.AbstractApplicationPortlet import (AbstractApplicationPortlet,)
# from java.io.IOException import (IOException,)
# from java.io.InputStream import (InputStream,)
# from java.io.OutputStream import (OutputStream,)
# from java.lang.reflect.Method import (Method,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)
# from javax.portlet.ClientDataRequest import (ClientDataRequest,)
# from javax.portlet.MimeResponse import (MimeResponse,)
# from javax.portlet.PortletRequest import (PortletRequest,)
# from javax.portlet.PortletResponse import (PortletResponse,)
# from javax.portlet.PortletSession import (PortletSession,)
# from javax.portlet.ResourceRequest import (ResourceRequest,)
# from javax.portlet.ResourceResponse import (ResourceResponse,)
# from javax.portlet.ResourceURL import (ResourceURL,)
# from javax.servlet.ServletException import (ServletException,)
# from javax.servlet.http.HttpServletRequestWrapper import (HttpServletRequestWrapper,)


class PortletCommunicationManager(AbstractCommunicationManager):
    """TODO document me!

    @author peholmst
    """
    _currentUidlResponse = None

    class PortletRequestWrapper(Request):
        _request = None

        def __init__(self, request):
            self._request = request

        def getAttribute(self, name):
            return self._request.getAttribute(name)

        def getContentLength(self):
            return self._request.getContentLength()

        def getInputStream(self):
            return self._request.getPortletInputStream()

        def getParameter(self, name):
            value = self._request.getParameter(name)
            if value is None:
                # for GateIn portlet container simple-portal
                # do nothing - not on GateIn simple-portal
                try:
                    getRealReq = self._request.getClass().getMethod('getRealRequest')
                    origRequest = getRealReq.invoke(self._request)
                    value = origRequest.getParameter(name)
                except Exception, e:
                    pass # astStmt: [Stmt([]), None]
            return value

        def getRequestID(self):
            return 'WindowID:' + self._request.getWindowID()

        def getSession(self):
            return self.PortletSessionWrapper(self._request.getPortletSession())

        def getWrappedRequest(self):
            return self._request

        def isRunningInPortlet(self):
            return True

        def setAttribute(self, name, o):
            self._request.setAttribute(name, o)

    class PortletResponseWrapper(Response):
        _response = None

        def __init__(self, response):
            self._response = response

        def getOutputStream(self):
            return self._response.getPortletOutputStream()

        def getWrappedResponse(self):
            return self._response

        def setContentType(self, type):
            self._response.setContentType(type)

    class PortletSessionWrapper(Session):
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

    class AbstractApplicationPortletWrapper(Callback):
        _portlet = None

        def __init__(self, portlet):
            self._portlet = portlet

        def criticalNotification(self, request, response, cap, msg, details, outOfSyncURL):
            self._portlet.criticalNotification(request.getWrappedRequest(), response.getWrappedResponse(), cap, msg, details, outOfSyncURL)

        def getRequestPathInfo(self, request):
            if isinstance(request.getWrappedRequest(), ResourceRequest):
                return request.getWrappedRequest().getResourceID()
            else:
                # We do not use paths in portlet mode
                raise self.UnsupportedOperationException('PathInfo only available when using ResourceRequests')

        def getThemeResourceAsStream(self, themeName, resource):
            return self._portlet.getPortletContext().getResourceAsStream('/' + AbstractApplicationPortlet.THEME_DIRECTORY_PATH + themeName + '/' + resource)

    def __init__(self, application):
        super(PortletCommunicationManager, self)(application)

    def handleFileUpload(self, request, response):
        contentType = request.getContentType()
        name = request.getParameter('name')
        ownerId = request.getParameter('rec-owner')
        variableOwner = self.getVariableOwner(ownerId)
        streamVariable = self._ownerToNameToStreamVariable[variableOwner].get(name)
        if contentType.contains('boundary'):
            self.doHandleSimpleMultipartFileUpload(self.PortletRequestWrapper(request), self.PortletResponseWrapper(response), streamVariable, name, variableOwner, contentType.split('boundary=')[1])
        else:
            self.doHandleXhrFilePost(self.PortletRequestWrapper(request), self.PortletResponseWrapper(response), streamVariable, name, variableOwner, request.getContentLength())

    def unregisterPaintable(self, p):
        super(PortletCommunicationManager, self).unregisterPaintable(p)
        if self._ownerToNameToStreamVariable is not None:
            self._ownerToNameToStreamVariable.remove(p)

    def handleUidlRequest(self, request, response, applicationPortlet, window):
        self._currentUidlResponse = response
        self.doHandleUidlRequest(self.PortletRequestWrapper(request), self.PortletResponseWrapper(response), self.AbstractApplicationPortletWrapper(applicationPortlet), window)
        self._currentUidlResponse = None

    def handleURI(self, window, request, response, applicationPortlet):
        return self.handleURI(window, self.PortletRequestWrapper(request), self.PortletResponseWrapper(response), self.AbstractApplicationPortletWrapper(applicationPortlet))

    def getApplicationWindow(self, request, applicationPortlet, application, assumedWindow):
        """Gets the existing application or creates a new one. Get a window within
        an application based on the requested URI.

        @param request
                   the portlet Request.
        @param applicationPortlet
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
        return self.doGetApplicationWindow(self.PortletRequestWrapper(request), self.AbstractApplicationPortletWrapper(applicationPortlet), application, assumedWindow)

    _ownerToNameToStreamVariable = None

    def getStreamVariableTargetUrl(self, owner, name, value):
        if self._ownerToNameToStreamVariable is None:
            self._ownerToNameToStreamVariable = dict()
        nameToReceiver = self._ownerToNameToStreamVariable[owner]
        if nameToReceiver is None:
            nameToReceiver = dict()
            self._ownerToNameToStreamVariable.put(owner, nameToReceiver)
        nameToReceiver.put(name, value)
        resurl = self._currentUidlResponse.createResourceURL()
        resurl.setResourceID('UPLOAD')
        resurl.setParameter('name', name)
        resurl.setParameter('rec-owner', self.getPaintableId(owner))
        resurl.setProperty('name', name)
        resurl.setProperty('rec-owner', self.getPaintableId(owner))
        return str(resurl)

    def cleanStreamVariable(self, owner, name):
        map = self._ownerToNameToStreamVariable[owner]
        map.remove(name)
        if map.isEmpty():
            self._ownerToNameToStreamVariable.remove(owner)
