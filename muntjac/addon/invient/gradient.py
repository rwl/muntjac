# @INVIENT_COPYRIGHT@
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

from muntjac.addon.invient.paint import IPaint

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class Unit(object):

    NUMBER = None
    PERCENT = None

    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol

    def getName(self):
        return self._name

    def getSymbol(self):
        return self._symbol

    @classmethod
    def values(cls):
        return [cls.NUMBER, cls.PERCENT]

Unit.NUMBER = Unit('number', '')
Unit.PERCENT = Unit('percent', '%')


class IColorStop(object):
    """Represents a stop-value and a color. The stop-value should be in range
    (0.0-1.0). The color of the gradient at each stop is the color specified
    for that stop. Between each such stop, the colors and the alpha component
    will be linearly interpolated over the RGBA.

    @author: Invient
    @author: Richard Lincoln
    """

    def getStopAt(self):
        raise NotImplementedError

    def getStopAtUnit(self):
        raise NotImplementedError

    def getColor(self):
        raise NotImplementedError


class IGradient(IPaint):
    """The Gradient defines a way to fill a shape with a linear color gradient
    pattern.

    @author: Invient
    @author: Richard Lincoln
    """

    def getxStart(self):
        """Returns the x-coordinate of a point at which linear gradient
                starts.
        @return: the x-coordinate of a point at which linear gradient
                starts.
        """
        raise NotImplementedError

    def getxStartUnit(self):
        """Returns the unit of x-coordinate of a point at which linear gradient starts.
        @return: the unit of x-coordinate of a point at which linear gradient starts.
        """
        raise NotImplementedError

    def getyStart(self):
        """Returns the y-coordinate of a point at which linear gradient starts.
        @return: the y-coordinate of a point at which linear gradient starts.
        """
        raise NotImplementedError

    def getyStartUnit(self):
        """Returns the unit of y-coordinate of a point at which linear gradient starts.
        @return: the unit of y-coordinate of a point at which linear gradient starts.
        """
        raise NotImplementedError

    def getxEnd(self):
        """Returns the x-coordinate of a point at which linear gradient
                ends.
        @return: the x-coordinate of a point at which linear gradient
                 ends.
        """
        raise NotImplementedError

    def getxEndUnit(self):
        """Returns the unit of x-coordinate of a point at which linear gradient ends.
        @return: the unit of x-coordinate of a point at which linear gradient ends.
        """
        raise NotImplementedError

    def getyEnd(self):
        """Returns the x-coordinate of a point at which linear gradient ends.
        @return: the x-coordinate of a point at which linear gradient ends.
        """
        raise NotImplementedError

    def getyEndUnit(self):
        """Returns the unit of y-coordinate of a point at which linear gradient ends.
        @return: the unit of y-coordinate of a point at which linear gradient ends.
        """
        raise NotImplementedError

    def getColorStops(self):
        """Returns a list of colorstops associated with this gradient.
        @return: a list of colorstops associated with this gradient.
        @see: L{IColorStop}
        """
        raise NotImplementedError


class LinearGradient(IGradient):
    """Represents linear gradient where points of a linear gradient specify a
    line. For more details on gradient, refer to CSS 3 gradient
    documentation.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, xStart, xStartUnit_or_yStart, yStart_or_xEnd,
                 yStartUnit_or_yEnd, xEnd_or_colorStops, xEndUnit=None,
                 yEnd=None, yEndUnit=None, colorStops=None):
        """Creates a LinearGradient with the specified xStart, xEnd, yStart
        and yEnd values with default {@link Unit} value number.

        @param xStart:
                   the x-coordinate of a point at which linear gradient
                   starts.
        @param xStartUnit_or_yStart:
                   the unit for the xStart value. It can have one of the two
                   values Unit.NUMBER or Unit.PERCENT. If it is null then the
                   default value is Unit.NUMBER. Or the y-coordinate of a point
                   at which linear gradient starts.
        @param yStart_or_xEnd:
                   the y-coordinate of a point at which linear gradient
                   starts or the x-coordinate of a point at which linear
                   gradient ends.
        @param yStartUnit_or_yEnd:
                   the unit for the yStart value. It can have one of the two
                   values Unit.NUMBER or Unit.PERCENT. If it is null then the
                   default value is Unit.NUMBER. Or the y-coordinate of a point
                   at which linear gradient ends.
        @param xEnd_or_colorStops:
                   the x-coordinate of a point at which linear gradient ends or
                   the list of colorstops for the linear gradient.
        @param xEndUnit:
                   the unit for the xEnd value. It can have one of the two
                   values Unit.NUMBER or Unit.PERCENT. If it is null then the
                   default value is Unit.NUMBER.
        @param yEnd:
                   the y-coordinate of a point at which linear gradient ends.
        @param yEndUnit
                   the unit for the yEnd value. It can have one of the two
                   values Unit.NUMBER or Unit.PERCENT. If it is null then the
                   default value is Unit.NUMBER.
        @param colorStops:
                   the list of colorstops for the linear gradient.
        """
        self._xStart = 0
        self._xStartUnit = Unit.NUMBER
        self._yStart = 0
        self._yStartUnit = Unit.NUMBER
        self._xEnd = 0
        self._xEndUnit = Unit.NUMBER
        self._yEnd = 0
        self._yEndUnit = Unit.NUMBER
        self._colorStops = list()

        xStartUnit = yStartUnit = None
        if xEndUnit is None:
            xStart, yStart, xEnd, yEnd, colorStops = (xStart,
                xStartUnit_or_yStart, yStart_or_xEnd, yStartUnit_or_yEnd,
                 xEnd_or_colorStops)
        else:
            xStartUnit, yStart, yStartUnit, xEnd, xEndUnit, yEnd, yEndUnit, \
            colorStops = (xStartUnit_or_yStart, yStart_or_xEnd,
                yStartUnit_or_yEnd, xEnd_or_colorStops, xEndUnit, yEnd,
                yEndUnit, colorStops)

        super(LinearGradient, self).__init__()

        self._xStart = xStart
        if xStartUnit is not None:
            self._xStartUnit = xStartUnit

        self._yStart = yStart
        if yStartUnit is not None:
            self._yStartUnit = yStartUnit

        self._xEnd = xEnd
        if xEndUnit is not None:
            self._xEndUnit = xEndUnit

        self._yEnd = yEnd
        if yEndUnit is not None:
            self._yEndUnit = yEndUnit

        if colorStops is not None:
            self._colorStops = colorStops

    def getxStart(self):
        return self._xStart

    def getxEnd(self):
        return self._xEnd

    def getyStart(self):
        return self._yStart

    def getyEnd(self):
        return self._yEnd

    def getxStartUnit(self):
        return self._xStartUnit

    def getyStartUnit(self):
        return self._yStartUnit

    def getxEndUnit(self):
        return self._xEndUnit

    def getyEndUnit(self):
        return self._yEndUnit

    def getColorStops(self):
        return self._colorStops

    def getString(self):
        """@return: Returns string representation of this LinearGradient"""
        sb = StringIO()
        # The prefix "JSOBJ:" indicates that the string is a JavaScript
        # object
        x1 = '\'' + str(self._xStart) + self._xStartUnit.getSymbol() + '\''
        y1 = '\'' + str(self._yStart) + self._yStartUnit.getSymbol() + '\''
        x2 = '\'' + str(self._xEnd) + self._xEndUnit.getSymbol() + '\''
        y2 = '\'' + str(self._yEnd) + self._yEndUnit.getSymbol() + '\''
        sb.write('JSOBJ:{')
        sb.write(' linearGradient: [' + x1 + ',' + y1 + ',' + x2 + ',' + y2 + '],')
        sb.write(' stops: [')
        count = 0
        for colorStop in self._colorStops:
            if colorStop.getColor() is not None:
                stopAt = ('\'' + str(colorStop.getStopAt())
                        + colorStop.getStopAtUnit().getSymbol() + '\'')
                stopColor = '\'' + colorStop.getColor().getString() + '\''
                if count > 0:
                    sb.write(',')
                sb.write('[' + stopAt + ', ' + stopColor + ']')
                count += 1
        sb.write(' ]')
        sb.write('}')
        return sb.getvalue()


class LinearColorStop(IColorStop):
    """Represents stop-value and color for the L{LinearGradient}

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, stopAt, stopAtUnit_or_color, color=None):
        self._stopAt = None
        self._stopAtUnit = Unit.NUMBER
        self._color = None

        if color == None:
            color = stopAtUnit_or_color
            super(LinearColorStop, self).__init__()
            self._stopAt = stopAt
            self._color = color
        else:
            stopAtUnit = stopAtUnit_or_color
            super(LinearColorStop, self).__init__()
            self._stopAt = stopAt
            if stopAtUnit is not None:
                self._stopAtUnit = stopAtUnit
            self._color = color

    def getStopAt(self):
        return self._stopAt

    def getStopAtUnit(self):
        return self._stopAtUnit

    def getColor(self):
        return self._color
