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

from __pyjamas__ import JS

from muntjac.terminal.gwt.client.tooltip_info import TooltipInfo


class ComponentDetail(object):

    def __init__(self, client, pid, component):
        self._component = component
        self._pid = pid
        self._tooltipInfo = TooltipInfo()

        self._relativeSize = None
        self._offsetSize = None
        self._additionalTooltips = None
        self._eventListeners = None


    def getTooltipInfo(self, key):
        """Returns a TooltipInfo assosiated with Component. If element is
        given, returns an additional TooltipInfo.

        @return: the tooltipInfo
        """
        if key is None:
            return self._tooltipInfo
        elif self._additionalTooltips is not None:
            return self._additionalTooltips.get(key)
        else:
            return None


    def setTooltipInfo(self, tooltipInfo):
        """@param tooltipInfo:
                   the tooltipInfo to set
        """
        self._tooltipInfo = tooltipInfo


    def getPid(self):
        """@return: the pid"""
        return self._pid


    def getComponent(self):
        """@return: the component"""
        return self._component


    def getRelativeSize(self):
        """@return: the relativeSize"""
        return self._relativeSize


    def setRelativeSize(self, relativeSize):
        """@param relativeSize:
                   the relativeSize to set
        """
        self._relativeSize = relativeSize


    def getOffsetSize(self):
        """@return: the offsetSize"""
        return self._offsetSize


    def setOffsetSize(self, offsetSize):
        """@param offsetSize:
                   the offsetSize to set
        """
        self._offsetSize = offsetSize


    def putAdditionalTooltip(self, key, tooltip):
        if (tooltip is None) and (self._additionalTooltips is not None):
            del self._additionalTooltips[key]
        else:
            if self._additionalTooltips is None:
                self._additionalTooltips = dict()
            self._additionalTooltips[key] = tooltip


    def registerEventListenersFromUIDL(self, uidl):
        """Stores the event listeners registered on server-side and passed
        along in the UIDL.

        @param componentUIDL:
                   The UIDL for the component
        """
        JS("""
            @{{self}}.@com.vaadin.terminal.gwt.client.ComponentDetail::eventListeners = @{{uidl}}[1].eventListeners;
        """)
        pass


    def hasEventListeners(self, eventIdentifier):
        """Checks if there is a registered server side listener for the event.

        @param eventIdentifier:
                   The identifier for the event
        @return: true if at least one listener has been registered on server
                 side for the event identified by eventIdentifier.
        """
        if self._eventListeners is not None:
            l = len(self._eventListeners)
            for i in range(l):
                if self._eventListeners.get(i) == eventIdentifier:
                    return True

        return False
