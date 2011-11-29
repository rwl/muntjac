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
