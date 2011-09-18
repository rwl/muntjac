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
# from java.io.IOException import (IOException,)
# from java.io.OutputStream import (OutputStream,)
# from java.io.PrintWriter import (PrintWriter,)
# from java.io.Serializable import (Serializable,)
# from java.util.Collection import (Collection,)
# from java.util.Locale import (Locale,)
# from javax.portlet.CacheControl import (CacheControl,)
# from javax.portlet.PortletMode import (PortletMode,)
# from javax.portlet.PortletURL import (PortletURL,)
# from javax.portlet.RenderResponse import (RenderResponse,)
# from javax.portlet.ResourceURL import (ResourceURL,)
# from javax.servlet.http.Cookie import (Cookie,)
# from org.w3c.dom.DOMException import (DOMException,)
# from org.w3c.dom.Element import (Element,)


class RestrictedRenderResponse(RenderResponse, Serializable):
    """Read-only wrapper for a {@link RenderResponse}.

    Only for use by {@link PortletApplicationContext} and
    {@link PortletApplicationContext2}.
    """
    _response = None

    def __init__(self, response):
        self._response = response

    def addProperty(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            cookie, = _0
        elif _1 == 2:
            if isinstance(_0[1], Element):
                key, element = _0
            else:
                key, value = _0
                self._response.addProperty(key, value)
        else:
            raise ARGERROR(1, 2)

    def createActionURL(self):
        return self._response.createActionURL()

    def createRenderURL(self):
        return self._response.createRenderURL()

    def encodeURL(self, path):
        return self._response.encodeURL(path)

    def flushBuffer(self):
        # NOP
        # TODO throw?
        pass

    def getBufferSize(self):
        return self._response.getBufferSize()

    def getCharacterEncoding(self):
        return self._response.getCharacterEncoding()

    def getContentType(self):
        return self._response.getContentType()

    def getLocale(self):
        return self._response.getLocale()

    def getNamespace(self):
        return self._response.getNamespace()

    def getPortletOutputStream(self):
        # write forbidden
        return None

    def getWriter(self):
        # write forbidden
        return None

    def isCommitted(self):
        return self._response.isCommitted()

    def reset(self):
        # NOP
        # TODO throw?
        pass

    def resetBuffer(self):
        # NOP
        # TODO throw?
        pass

    def setBufferSize(self, size):
        # NOP
        # TODO throw?
        pass

    def setContentType(self, type):
        # NOP
        # TODO throw?
        pass

    def setProperty(self, key, value):
        self._response.setProperty(key, value)

    def setTitle(self, title):
        self._response.setTitle(title)

    def setNextPossiblePortletModes(self, portletModes):
        # NOP
        # TODO throw?
        pass

    def createResourceURL(self):
        return self._response.createResourceURL()

    def getCacheControl(self):
        return self._response.getCacheControl()

    # NOP
    # TODO throw?
    # NOP
    # TODO throw?

    def createElement(self, tagName):
        # NOP
        return None
