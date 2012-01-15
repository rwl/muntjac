# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class IColorSelector(object):
    """The Interface ColorSelector.

    @author: John Ahlroos
    """

    def setColor(self, color):
        """Sets the color.

        @param color: the new color
        """
        raise NotImplementedError


    def getColor(self):
        """Gets the color.

        @return: the color
        """
        raise NotImplementedError
