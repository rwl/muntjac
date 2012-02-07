# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.addon.invient.paint import IPaint
from muntjac.addon.colorpicker.color import Color


class Color(IPaint):
    """The Color interface represents RBG and RBGA colors.
    Do not confuse with L{Color} class. This is a simplified
    version of L{Color} for the purpose of InvientCharts

    @author: Invient
    @author: Richard Lincoln
    """
    pass


class RGB(Color):
    """Represents RBG color value.

    @author: Invient
    @author: Richard Lincoln
    """

    def __init__(self, red, green, blue):
        """Creates an RGB color with the specified red, green, and blue values.
        The values must be in the range (0 - 255).

        @param red:
                   the red component in a color
        @param green:
                   the green component in a color
        @param blue:
                   the blue component in a color
        """
        super(RGB, self).__init__()
        errorCompString = ''
        hasError = False
        if (red < 0) or (red > 255):
            hasError = True
            errorCompString = ' Red '

        if (green < 0) or (green > 255):
            hasError = True
            errorCompString += ' Green'

        if (blue < 0) or (blue > 255):
            hasError = True
            errorCompString += ' Blue'

        if hasError:
            raise ValueError('Color parameter outside of expected range:'
                    + errorCompString)

        self._red = red
        self._green = green
        self._blue = blue


    def getRed(self):
        """@return: Returns the red component in the range (0-255)."""
        return self._red


    def getGreen(self):
        """@return: Returns the green component in the range (0-255)."""
        return self._green


    def getBlue(self):
        """@return: Returns the blue component in the range (0-255)."""
        return self._blue


    def getString(self):
        """@return: Returns string representation of this RBG."""
        return ('rgb(' + str(self._red) + ',' + str(self._green) + ','
                + str(self._blue) + ')')


    def __str__(self):
        """@return: Returns string representation of this RBG."""
        return ('RGB [red=' + str(self._red) + ', green=' + str(self._green)
                + ', blue=' + str(self._blue) + ']')


class RGBA(RGB):
    """Represents RGBA color value.

    @author Invient
    @author: Richard Lincoln
    """

    def __init__(self, red, green, blue, alpha):
        """Creates an RGBA color with the specified red, green, blue and alpha
        values. The red, green and blue values must be in the range (0 -
        255). The alpha value must be in the range (0.0-1.0). The alpha value
        deaults to 1.0

        @param red:
                   the red component in a color
        @param green:
                   the green component in a color
        @param blue:
                   the blue component in a color
        @param alpha:
                   the alpha component in a color
        """
        super(RGBA, self).__init__(red, green, blue)

        if (alpha < 0.0) or (alpha > 1.0):
            errorCompString = ' Alpha'
            raise ValueError('Color parameter outside of expected range: '
                        + errorCompString)

        self._alpha = alpha


    def getAlpha(self):
        """@return: Returns the alpha component in the range (0.0-1.0)."""
        return self._alpha


    def getString(self):
        """@return: Returns string representation of this RGBA"""
        return ('rgba(' + str(self.getRed()) + ',' + str(self.getGreen())
                + ',' + str(self.getBlue()) + ',' + str(self._alpha) + ')')


    def __str__(self):
        """@return: Returns string representation of this RGBA"""
        return ('RGBA [alpha=' + str(self._alpha)
                + ', red=' + str(self.getRed())
                + ', green=' + str(self.getGreen())
                + ', blue=' + str(self.getBlue())
                + ']')
