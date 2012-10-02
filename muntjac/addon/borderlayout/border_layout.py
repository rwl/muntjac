# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.terminal.sizeable import ISizeable

from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.label import Label


DEFAULT_MINIMUM_HEIGHT = '50px'


class Constraint(object):
    NORTH = 'NORTH'
    WEST = 'WEST'
    CENTER = 'CENTER'
    EAST = 'EAST'
    SOUTH = 'SOUTH'
    _values = [NORTH, WEST, CENTER, EAST, SOUTH]

    @classmethod
    def values(cls):
        return cls._values[:]


class BorderLayout(VerticalLayout):
    """BorderLayout mimics {@link java.awt.BorderLayout} in Muntjac."""

    def __init__(self):
        """Create a layout structure that mimics the traditional
        {@link java.awt.BorderLayout}.
        """
        super(VerticalLayout, self).__init__()

        self._mainLayout = VerticalLayout()
        self._centerLayout = HorizontalLayout()

        self._minimumNorthHeight = DEFAULT_MINIMUM_HEIGHT
        self._minimumSouthHeight = DEFAULT_MINIMUM_HEIGHT
        self._minimumWestWidth = DEFAULT_MINIMUM_HEIGHT
        self._minimumEastWidth = DEFAULT_MINIMUM_HEIGHT

        self.north = Label('')
        self.west = Label('')
        self.center = Label('')
        self.east = Label('')
        self.south = Label('')

        self._centerLayout.addComponent(self.west)
        self._centerLayout.addComponent(self.center)
        self._centerLayout.addComponent(self.east)
        self._centerLayout.setSizeFull()

        self._mainLayout.addComponent(self.north)
        self._mainLayout.addComponent(self._centerLayout)
        self._mainLayout.addComponent(self.south)
        self._mainLayout.setExpandRatio(self._centerLayout, 1)

        super(BorderLayout, self).setWidth('100%')
        super(BorderLayout, self).addComponent(self._mainLayout)


    def setWidth(self, width):
        if self._mainLayout is None:
            return
        self._mainLayout.setWidth(width)
        self._centerLayout.setExpandRatio(self.center, 1)
        self.requestRepaint()


    def setHeight(self, height):
        self._mainLayout.setHeight(height)
        self.west.setHeight('100%')
        self.center.setHeight('100%')
        self.east.setHeight('100%')
        self._centerLayout.setExpandRatio(self.center, 1)
        self.requestRepaint()


    def setSizeFull(self):
        super(BorderLayout, self).setSizeFull()
        self._mainLayout.setSizeFull()
        self._centerLayout.setExpandRatio(self.center, 1)
        self.requestRepaint()


    def setMargin(self, margin):
        self._mainLayout.setMargin(margin)
        self.requestRepaint()


    def setSpacing(self, spacing):
        self._mainLayout.setSpacing(spacing)
        self._centerLayout.setSpacing(spacing)
        self.requestRepaint()


    def isSpacing(self):
        return self._mainLayout.isSpacing() and self._centerLayout.isSpacing()


    def removeComponent(self, c):
        self.replaceComponent(c, Label(''))


    def addComponent(self, c, constraint):
        """Add component into borderlayout

        @param c
                   component to be added into layout
        @param constraint
                   place of the component (have to be on of BorderLayout.NORTH,
                   BorderLayout.WEST, BorderLayout.CENTER, BorderLayout.EAST, or
                   BorderLayout.SOUTH
        """
        if constraint == Constraint.NORTH:
            self._mainLayout.replaceComponent(self.north, c)
            self.north = c
            if ((self.north.getHeight() < 0)
                    or (self.north.getHeightUnits() == ISizeable.UNITS_PERCENTAGE)):
                self.north.setHeight(self._minimumNorthHeight)
        elif constraint == Constraint.WEST:
            self._centerLayout.replaceComponent(self.west, c)
            self.west = c
            if ((self.west.getWidth() < 0)
                    or (self.west.getWidthUnits() == ISizeable.UNITS_PERCENTAGE)):
                self.west.setWidth(self._minimumWestWidth)
        elif constraint == Constraint.CENTER:
            self._centerLayout.replaceComponent(self.center, c)
            self.center = c
            self.center.setHeight(self._centerLayout.getHeight(),
                    self._centerLayout.getHeightUnits())
            self.center.setWidth('100%')
            self._centerLayout.setExpandRatio(self.center, 1)
        elif constraint == self.Constraint.EAST:
            self._centerLayout.replaceComponent(self.east, c)
            self.east = c
            if ((self.east.getWidth() < 0)
                    or (self.east.getWidthUnits() == ISizeable.UNITS_PERCENTAGE)):
                self.east.setWidth(self._minimumEastWidth)
        elif constraint == Constraint.SOUTH:
            self._mainLayout.replaceComponent(self.south, c)
            self.south = c
            if ((self.south.getHeight() < 0)
                    or (self.south.getHeightUnits() == ISizeable.UNITS_PERCENTAGE)):
                self.south.setHeight(self._minimumSouthHeight)
        else:
            raise ValueError, 'Invalid BorderLayout constraint.'
        self._centerLayout.setExpandRatio(self.center, 1)
        self.requestRepaint()


    def replaceComponent(self, oldComponent, newComponent):
        if oldComponent == self.north:
            self._mainLayout.replaceComponent(self.north, newComponent)
            self.north = newComponent
        elif oldComponent == self.west:
            self._centerLayout.replaceComponent(self.west, newComponent)
            self.west = newComponent
        elif oldComponent == self.center:
            self._centerLayout.replaceComponent(self.center, newComponent)
            self._centerLayout.setExpandRatio(newComponent, 1)
            self.center = newComponent
        elif oldComponent == self.east:
            self._centerLayout.replaceComponent(self.east, newComponent)
            self.east = newComponent
        elif oldComponent == self.south:
            self._mainLayout.replaceComponent(self.south, newComponent)
            self.south = newComponent
        self._centerLayout.setExpandRatio(self.center, 1)
        self.requestRepaint()


    def setMinimumNorthHeight(self, minimumNorthHeight):
        """Set minimum height of the component in the BorderLayout.NORTH

        @param minimumNorthHeight
        """
        self._minimumNorthHeight = minimumNorthHeight


    def getMinimumNorthHeight(self):
        """Get minimum height of the component in the BorderLayout.NORTH"""
        return self._minimumNorthHeight


    def setMinimumSouthHeight(self, minimumSouthHeight):
        """Set minimum height of the component in the BorderLayout.SOUTH

        @param minimumNorthHeight
        """
        self._minimumSouthHeight = minimumSouthHeight


    def getMinimumSouthHeight(self):
        """Get minimum height of the component in the BorderLayout.SOUTH"""
        return self._minimumSouthHeight


    def setMinimumWestWidth(self, minimumWestWidth):
        """Set minimum height of the component in the BorderLayout.WEST

        @param minimumNorthHeight
        """
        self._minimumWestWidth = minimumWestWidth


    def getMinimumWestWidth(self):
        """Get minimum height of the component in the BorderLayout.WEST"""
        return self._minimumWestWidth


    def setMinimumEastWidth(self, minimumEastWidth):
        """Set minimum height of the component in the BorderLayout.EAST

        @param minimumNorthHeight
        """
        self._minimumEastWidth = minimumEastWidth


    def getMinimumEastWidth(self):
        """Get minimum height of the component in the BorderLayout.EAST"""
        return self._minimumEastWidth


    def getComponent(self, position):
        """Return component from specific position

        @param constraint
        @return
        """
        if position == Constraint.NORTH:
            return self.north
        elif position == Constraint.WEST:
            return self.west
        elif position == Constraint.CENTER:
            return self.center
        elif position == Constraint.EAST:
            return self.east
        elif position == Constraint.SOUTH:
            return self.south
        else:
            raise ValueError, 'Invalid BorderLayout constraint.'
