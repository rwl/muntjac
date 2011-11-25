# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.dd.VerticalDropLocation import (VerticalDropLocation,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.dd.HorizontalDropLocation import (HorizontalDropLocation,)


class DDUtil(object):

    @classmethod
    def getVerticalDropLocation(cls, *args):
        """@deprecated use the version with the actual event instead of detected
                    clientY value

        @param element
        @param clientY
        @param topBottomRatio
        @return
        """
        _0 = args
        _1 = len(args)
        if _1 == 3:
            if isinstance(_0[1], NativeEvent):
                element, event, topBottomRatio = _0
                offsetHeight = element.getOffsetHeight()
                return cls.getVerticalDropLocation(element, offsetHeight, event, topBottomRatio)
            else:
                element, clientY, topBottomRatio = _0
                offsetHeight = element.getOffsetHeight()
                return cls.getVerticalDropLocation(element, offsetHeight, clientY, topBottomRatio)
        elif _1 == 4:
            if isinstance(_0[2], NativeEvent):
                element, offsetHeight, event, topBottomRatio = _0
                clientY = Util.getTouchOrMouseClientY(event)
                return cls.getVerticalDropLocation(element, offsetHeight, clientY, topBottomRatio)
            else:
                element, offsetHeight, clientY, topBottomRatio = _0
                absoluteTop = element.getAbsoluteTop()
                fromTop = clientY - absoluteTop
                percentageFromTop = fromTop / offsetHeight
                if percentageFromTop < topBottomRatio:
                    return VerticalDropLocation.TOP
                elif percentageFromTop > 1 - topBottomRatio:
                    return VerticalDropLocation.BOTTOM
                else:
                    return VerticalDropLocation.MIDDLE
        else:
            raise ARGERROR(3, 4)

    @classmethod
    def getHorizontalDropLocation(cls, *args):
        """None
        ---
        @deprecated use the version with the actual event
        @param element
        @param clientX
        @param leftRightRatio
        @return
        """
        _0 = args
        _1 = len(args)
        if _1 == 3:
            if isinstance(_0[1], NativeEvent):
                element, event, leftRightRatio = _0
                touchOrMouseClientX = Util.getTouchOrMouseClientX(event)
                return cls.getHorizontalDropLocation(element, touchOrMouseClientX, leftRightRatio)
            else:
                element, clientX, leftRightRatio = _0
                absoluteLeft = element.getAbsoluteLeft()
                offsetWidth = element.getOffsetWidth()
                fromTop = clientX - absoluteLeft
                percentageFromTop = fromTop / offsetWidth
                if percentageFromTop < leftRightRatio:
                    return HorizontalDropLocation.LEFT
                elif percentageFromTop > 1 - leftRightRatio:
                    return HorizontalDropLocation.RIGHT
                else:
                    return HorizontalDropLocation.CENTER
        else:
            raise ARGERROR(3, 3)
