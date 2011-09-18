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
from com.vaadin.terminal.gwt.server.RestrictedRenderResponse import (RestrictedRenderResponse,)
from com.vaadin.terminal.gwt.server.WebApplicationContext import (WebApplicationContext,)
# from java.io.Serializable import (Serializable,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)
# from javax.portlet.ActionRequest import (ActionRequest,)
# from javax.portlet.ActionResponse import (ActionResponse,)
# from javax.portlet.Portlet import (Portlet,)
# from javax.portlet.PortletSession import (PortletSession,)
# from javax.portlet.RenderRequest import (RenderRequest,)
# from javax.portlet.RenderResponse import (RenderResponse,)
# from javax.servlet.http.HttpSession import (HttpSession,)


class PortletApplicationContext(WebApplicationContext, Serializable):
    """@author marc"""
    portletSession = None
    portletListeners = dict()
    portletToApplication = dict()

    def __init__(self):
        pass

    @classmethod
    def getApplicationContext(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], HttpSession):
                session, = _0
                cx = session.getAttribute(WebApplicationContext.getName())
                if cx is None:
                    cx = PortletApplicationContext()
                if cx.session is None:
                    cx.session = session
                session.setAttribute(WebApplicationContext.getName(), cx)
                return cx
            else:
                session, = _0
                cx = session.getAttribute(WebApplicationContext.getName(), PortletSession.APPLICATION_SCOPE)
                if cx is None:
                    cx = PortletApplicationContext()
                if not isinstance(cx, PortletApplicationContext):
                    # TODO Should we even try this? And should we leave original as-is?
                    pcx = PortletApplicationContext()
                    pcx.applications.addAll(cx.applications)
                    cx.applications.clear()
                    pcx.browser = cx.browser
                    cx.browser = None
                    pcx.listeners = cx.listeners
                    cx.listeners = None
                    pcx.session = cx.session
                    cx = pcx
                if cx.portletSession is None:
                    cx.portletSession = session
                session.setAttribute(WebApplicationContext.getName(), cx, PortletSession.APPLICATION_SCOPE)
                return cx
        else:
            raise ARGERROR(1, 1)

    def removeApplication(self, application):
        self.portletListeners.remove(application)
        _0 = True
        it = self.portletToApplication.values()
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            value = it.next()
            if value == application:
                # values().iterator() is backed by the map
                it.remove()
        super(PortletApplicationContext, self).removeApplication(application)

    def reinitializeSession(self):
        """Reinitializing the session is not supported from portlets.

        @see com.vaadin.terminal.gwt.server.WebApplicationContext#reinitializeSession()
        """
        raise self.UnsupportedOperationException('Reinitializing the session is not supported from portlets')

    def setPortletApplication(self, portlet, app):
        self.portletToApplication.put(portlet, app)

    def getPortletApplication(self, portlet):
        return self.portletToApplication[portlet]

    def getPortletSession(self):
        return self.portletSession

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

    @classmethod
    def dispatchRequest(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 3:
            if isinstance(_0[1], ActionRequest):
                portlet, request, response = _0
                ctx = cls.getApplicationContext(request.getPortletSession())
                if ctx is not None:
                    ctx.firePortletActionRequest(portlet, request, response)
            else:
                portlet, request, response = _0
                ctx = cls.getApplicationContext(request.getPortletSession())
                if ctx is not None:
                    ctx.firePortletRenderRequest(portlet, request, response)
        else:
            raise ARGERROR(3, 3)

    def firePortletRenderRequest(self, portlet, request, response):
        app = self.getPortletApplication(portlet)
        listeners = self.portletListeners[app]
        if listeners is not None:
            for l in listeners:
                l.handleRenderRequest(request, RestrictedRenderResponse(response))

    def firePortletActionRequest(self, portlet, request, response):
        app = self.getPortletApplication(portlet)
        listeners = self.portletListeners[app]
        if listeners is not None:
            for l in listeners:
                l.handleActionRequest(request, response)

    class PortletListener(Serializable):

        def handleRenderRequest(self, request, response):
            pass

        def handleActionRequest(self, request, response):
            pass
