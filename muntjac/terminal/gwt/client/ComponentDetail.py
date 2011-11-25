# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.TooltipInfo import (TooltipInfo,)
# from java.util.HashMap import (HashMap,)


class ComponentDetail(object):
    _component = None
    _tooltipInfo = TooltipInfo()
    _pid = None

    def __init__(self, client, pid, component):
        self._component = component
        self._pid = pid

    def getTooltipInfo(self, key):
        """Returns a TooltipInfo assosiated with Component. If element is given,
        returns an additional TooltipInfo.

        @param key
        @return the tooltipInfo
        """
        if key is None:
            return self._tooltipInfo
        elif self._additionalTooltips is not None:
            return self._additionalTooltips[key]
        else:
            return None

    def setTooltipInfo(self, tooltipInfo):
        """@param tooltipInfo
                   the tooltipInfo to set
        """
        self._tooltipInfo = tooltipInfo

    _relativeSize = None
    _offsetSize = None
    _additionalTooltips = None

    def getPid(self):
        """@return the pid"""
        return self._pid

    def getComponent(self):
        """@return the component"""
        return self._component

    def getRelativeSize(self):
        """@return the relativeSize"""
        return self._relativeSize

    def setRelativeSize(self, relativeSize):
        """@param relativeSize
                   the relativeSize to set
        """
        self._relativeSize = relativeSize

    def getOffsetSize(self):
        """@return the offsetSize"""
        return self._offsetSize

    def setOffsetSize(self, offsetSize):
        """@param offsetSize
                   the offsetSize to set
        """
        self._offsetSize = offsetSize

    def putAdditionalTooltip(self, key, tooltip):
        if tooltip is None and self._additionalTooltips is not None:
            self._additionalTooltips.remove(key)
        else:
            if self._additionalTooltips is None:
                self._additionalTooltips = dict()
            self._additionalTooltips.put(key, tooltip)

    _eventListeners = None

    def registerEventListenersFromUIDL(self, uidl):
        """Stores the event listeners registered on server-side and passed along in
        the UIDL.

        @param componentUIDL
                   The UIDL for the component
        @since 6.2
        """
        JS("""
        @{{self}}.@com.vaadin.terminal.gwt.client.ComponentDetail::eventListeners = @{{uidl}}[1].eventListeners;
    """)
        pass

    def hasEventListeners(self, eventIdentifier):
        """Checks if there is a registered server side listener for the event.

        @param eventIdentifier
                   The identifier for the event
        @return true if at least one listener has been registered on server side
                for the event identified by eventIdentifier.
        """
        if self._eventListeners is not None:
            l = len(self._eventListeners)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < l):
                    break
                if self._eventListeners.get(i) == eventIdentifier:
                    return True
        return False
