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

from com.vaadin.terminal.gwt.server.PortletCommunicationManager import (PortletCommunicationManager,)
from com.vaadin.terminal.gwt.server.AbstractWebApplicationContext import (AbstractWebApplicationContext,)
from com.vaadin.terminal.ExternalResource import (ExternalResource,)
from com.vaadin.terminal.gwt.server.RestrictedRenderResponse import (RestrictedRenderResponse,)
# from java.io.File import (File,)
# from java.io.Serializable import (Serializable,)
# from java.net.URL import (URL,)
# from java.util.HashMap import (HashMap,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)
# from java.util.logging.Level import (Level,)
# from java.util.logging.Logger import (Logger,)
# from javax.portlet.ActionRequest import (ActionRequest,)
# from javax.portlet.ActionResponse import (ActionResponse,)
# from javax.portlet.EventRequest import (EventRequest,)
# from javax.portlet.EventResponse import (EventResponse,)
# from javax.portlet.MimeResponse import (MimeResponse,)
# from javax.portlet.PortletConfig import (PortletConfig,)
# from javax.portlet.PortletMode import (PortletMode,)
# from javax.portlet.PortletModeException import (PortletModeException,)
# from javax.portlet.PortletResponse import (PortletResponse,)
# from javax.portlet.PortletSession import (PortletSession,)
# from javax.portlet.PortletURL import (PortletURL,)
# from javax.portlet.RenderRequest import (RenderRequest,)
# from javax.portlet.RenderResponse import (RenderResponse,)
# from javax.portlet.ResourceRequest import (ResourceRequest,)
# from javax.portlet.ResourceResponse import (ResourceResponse,)
# from javax.portlet.ResourceURL import (ResourceURL,)
# from javax.portlet.StateAwareResponse import (StateAwareResponse,)
# from javax.servlet.http.HttpSessionBindingListener import (HttpSessionBindingListener,)
# from javax.xml.namespace.QName import (QName,)
import time


class PortletApplicationContext2(AbstractWebApplicationContext):
    """TODO Write documentation, fix JavaDoc tags.

    This is automatically registered as a {@link HttpSessionBindingListener} when
    {@link PortletSession#setAttribute()} is called with the context as value.

    @author peholmst
    """
    _logger = Logger.getLogger(PortletApplicationContext2.getName())
    portletListeners = dict()
    session = None
    portletConfig = None
    portletWindowIdToApplicationMap = dict()
    _response = None
    _eventActionDestinationMap = dict()
    _eventActionValueMap = dict()
    _sharedParameterActionNameMap = dict()
    _sharedParameterActionValueMap = dict()

    def getBaseDirectory(self):
        resultPath = self.session.getPortletContext().getRealPath('/')
        if resultPath is not None:
            return File(resultPath)
        else:
            # FIXME: Handle exception
            try:
                url = self.session.getPortletContext().getResource('/')
                return File(url.getFile())
            except Exception, e:
                self._logger.log(Level.INFO, 'Cannot access base directory, possible security issue ' + 'with Application Server or Servlet Container', e)
        return None

    def getApplicationManager(self, application):
        mgr = self.applicationToAjaxAppMgrMap.get(application)
        if mgr is None:
            # Creates a new manager
            mgr = self.createPortletCommunicationManager(application)
            self.applicationToAjaxAppMgrMap.put(application, mgr)
        return mgr

    def createPortletCommunicationManager(self, application):
        return PortletCommunicationManager(application)

    @classmethod
    def getApplicationContext(cls, session):
        cxattr = session.getAttribute(PortletApplicationContext2.getName())
        cx = None
        # can be false also e.g. if old context comes from another
        # classloader when using
        # <private-session-attributes>false</private-session-attributes>
        # and redeploying the portlet - see #7461
        if isinstance(cxattr, PortletApplicationContext2):
            cx = cxattr
        if cx is None:
            cx = PortletApplicationContext2()
            session.setAttribute(PortletApplicationContext2.getName(), cx)
        if cx.session is None:
            cx.session = session
        return cx

    def removeApplication(self, application):
        super(PortletApplicationContext2, self).removeApplication(application)
        # values() is backed by map, removes the key-value pair from the map
        self.portletWindowIdToApplicationMap.values().remove(application)

    def addApplication(self, application, portletWindowId):
        self.applications.add(application)
        self.portletWindowIdToApplicationMap.put(portletWindowId, application)

    def getApplicationForWindowId(self, portletWindowId):
        return self.portletWindowIdToApplicationMap[portletWindowId]

    def getPortletSession(self):
        return self.session

    def getPortletConfig(self):
        return self.portletConfig

    def setPortletConfig(self, config):
        self.portletConfig = config

    def addPortletListener(self, app, listener):
        l = self.portletListeners[app]
        if l is None:
            l = LinkedHashSet()
            self.portletListeners.put(app, l)
        l.add(listener)

    def removePortletListener(self, app, listener):
        l = self.portletListeners[app]
        if l is not None:
            l.remove(listener)

    def firePortletRenderRequest(self, app, window, request, response):
        listeners = self.portletListeners[app]
        if listeners is not None:
            for l in listeners:
                l.handleRenderRequest(request, RestrictedRenderResponse(response), window)

    def firePortletActionRequest(self, app, window, request, response):
        key = request.getParameter(ActionRequest.ACTION_NAME)
        if key in self._eventActionDestinationMap:
            # this action request is only to send queued portlet events
            response.setEvent(self._eventActionDestinationMap[key], self._eventActionValueMap[key])
            # cleanup
            self._eventActionDestinationMap.remove(key)
            self._eventActionValueMap.remove(key)
        elif key in self._sharedParameterActionNameMap:
            # this action request is only to set shared render parameters
            response.setRenderParameter(self._sharedParameterActionNameMap[key], self._sharedParameterActionValueMap[key])
            # cleanup
            self._sharedParameterActionNameMap.remove(key)
            self._sharedParameterActionValueMap.remove(key)
        else:
            # normal action request, notify listeners
            listeners = self.portletListeners[app]
            if listeners is not None:
                for l in listeners:
                    l.handleActionRequest(request, response, window)

    def firePortletEventRequest(self, app, window, request, response):
        listeners = self.portletListeners[app]
        if listeners is not None:
            for l in listeners:
                l.handleEventRequest(request, response, window)

    def firePortletResourceRequest(self, app, window, request, response):
        listeners = self.portletListeners[app]
        if listeners is not None:
            for l in listeners:
                l.handleResourceRequest(request, response, window)

    class PortletListener(Serializable):

        def handleRenderRequest(self, request, response, window):
            pass

        def handleActionRequest(self, request, response, window):
            pass

        def handleEventRequest(self, request, response, window):
            pass

        def handleResourceRequest(self, request, response, window):
            pass

    def setResponse(self, response):
        """This is for use by {@link AbstractApplicationPortlet} only.

        TODO cleaner implementation, now "semi-static"!

        @param mimeResponse
        """
        self._response = response

    def generateApplicationResourceURL(self, resource, mapKey):
        if isinstance(self._response, MimeResponse):
            resourceURL = self._response.createResourceURL()
            filename = resource.getFilename()
            if filename is None:
                resourceURL.setResourceID('APP/' + mapKey + '/')
            else:
                resourceURL.setResourceID('APP/' + mapKey + '/' + filename)
            return str(resourceURL)
        else:
            # in a background thread or otherwise outside a request
            # TODO exception ??
            return None

    def generateActionURL(self, action):
        """Creates a new action URL.

        @param action
        @return action URL or null if called outside a MimeRequest (outside a
                UIDL request or similar)
        """
        url = None
        if isinstance(self._response, MimeResponse):
            url = self._response.createActionURL()
            url.setParameter('javax.portlet.action', action)
        else:
            return None
        return url

    def sendPortletEvent(self, window, name, value):
        """Sends a portlet event to the indicated destination.

        Internally, an action may be created and opened, as an event cannot be
        sent directly from all types of requests.

        The event destinations and values need to be kept in the context until
        sent. Any memory leaks if the action fails are limited to the session.

        Event names for events sent and received by a portlet need to be declared
        in portlet.xml .

        @param window
                   a window in which a temporary action URL can be opened if
                   necessary
        @param name
                   event name
        @param value
                   event value object that is Serializable and, if appropriate,
                   has a valid JAXB annotation
        """
        if isinstance(self._response, MimeResponse):
            actionKey = '' + 1000 * time.time()
            while actionKey in self._eventActionDestinationMap:
                actionKey = actionKey + '.'
            actionUrl = self.generateActionURL(actionKey)
            if actionUrl is not None:
                self._eventActionDestinationMap.put(actionKey, name)
                self._eventActionValueMap.put(actionKey, value)
                window.open(ExternalResource(str(actionUrl)))
            else:
                # this should never happen as we already know the response is a
                # MimeResponse
                raise self.IllegalStateException('Portlet events can only be sent from a portlet request')
        elif isinstance(self._response, StateAwareResponse):
            self._response.setEvent(name, value)
        else:
            raise self.IllegalStateException('Portlet events can only be sent from a portlet request')

    def setSharedRenderParameter(self, window, name, value):
        """Sets a shared portlet parameter.

        Internally, an action may be created and opened, as shared parameters
        cannot be set directly from all types of requests.

        The parameters and values need to be kept in the context until sent. Any
        memory leaks if the action fails are limited to the session.

        Shared parameters set or read by a portlet need to be declared in
        portlet.xml .

        @param window
                   a window in which a temporary action URL can be opened if
                   necessary
        @param name
                   parameter identifier
        @param value
                   parameter value
        """
        if isinstance(self._response, MimeResponse):
            actionKey = '' + 1000 * time.time()
            while actionKey in self._sharedParameterActionNameMap:
                actionKey = actionKey + '.'
            actionUrl = self.generateActionURL(actionKey)
            if actionUrl is not None:
                self._sharedParameterActionNameMap.put(actionKey, name)
                self._sharedParameterActionValueMap.put(actionKey, value)
                window.open(ExternalResource(str(actionUrl)))
            else:
                # this should never happen as we already know the response is a
                # MimeResponse
                raise self.IllegalStateException('Shared parameters can only be set from a portlet request')
        elif isinstance(self._response, StateAwareResponse):
            self._response.setRenderParameter(name, value)
        else:
            raise self.IllegalStateException('Shared parameters can only be set from a portlet request')

    def setPortletMode(self, window, portletMode):
        """Sets the portlet mode. This may trigger a new render request.

        Portlet modes used by a portlet need to be declared in portlet.xml .

        @param window
                   a window in which the render URL can be opened if necessary
        @param portletMode
                   the portlet mode to switch to
        @throws PortletModeException
                    if the portlet mode is not allowed for some reason
                    (configuration, permissions etc.)
        """
        if isinstance(self._response, MimeResponse):
            url = self._response.createRenderURL()
            url.setPortletMode(portletMode)
            window.open(ExternalResource(str(url)))
        elif isinstance(self._response, StateAwareResponse):
            self._response.setPortletMode(portletMode)
        else:
            raise self.IllegalStateException('Portlet mode can only be changed from a portlet request')
