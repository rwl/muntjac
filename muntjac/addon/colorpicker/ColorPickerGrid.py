# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
from com.vaadin.addon.colorpicker.events.ColorChangeEvent import (ColorChangeEvent,)
from com.vaadin.addon.colorpicker.ColorPicker import (ColorPicker,)
from com.vaadin.addon.colorpicker.ColorSelector import (ColorSelector,)
# from java.awt.Color import (Color,)
# from java.awt.Point import (Point,)
# from java.lang.reflect.Method import (Method,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)
ColorChangeListener = ColorPicker.ColorChangeListener


class ColorPickerGrid(AbstractComponent, ColorSelector):
    """The Class ColorPickerGrid.

    @author John Ahlroos
    """
    _COLOR_CHANGE_METHOD = None
    # This should never happen
    try:
        _COLOR_CHANGE_METHOD = ColorChangeListener.getDeclaredMethod('colorChanged', [ColorChangeEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in ColorPicker')
    # The x-coordinate.
    _x = 0
    # The y-coordinate.
    _y = 0
    # The rows.
    _rows = 1
    # The columns.
    _columns = 1
    # The color grid.
    _colorGrid = [None] * 1
    # The changed colors.
    _changedColors = dict()

    def __init__(self, *args):
        """Instantiates a new color picker grid.
        ---
        Instantiates a new color picker grid.

        @param rows
                   the rows
        @param columns
                   the columns
        ---
        Instantiates a new color picker grid.

        @param colors
                   the colors
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self._colorGrid[0][0] = Color.white
        elif _1 == 1:
            colors, = _0
            self._rows = colors.length
            self._columns = colors[0].length
            self._colorGrid = colors
            _0 = True
            row = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    row += 1
                if not (row < self._rows):
                    break
                _1 = True
                col = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        col += 1
                    if not (col < self._columns):
                        break
                    self._changedColors.put(Point(row, col), self._colorGrid[row][col])
            self.requestRepaint()
        elif _1 == 2:
            rows, columns = _0
            self.removeStyleName('v-customcomponent')
            self._rows = rows
            self._columns = columns
            self._colorGrid = [None] * columns
            self._colorGrid[0][0] = Color.white
        else:
            raise ARGERROR(0, 2)

    def setColorGrid(self, colors):
        """Sets the color grid.

        @param colors
                   the new color grid
        """
        self._rows = len(colors)
        self._columns = colors[0].length
        self._colorGrid = colors
        _0 = True
        row = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                row += 1
            if not (row < self._rows):
                break
            _1 = True
            col = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    col += 1
                if not (col < self._columns):
                    break
                self._changedColors.put(Point(row, col), self._colorGrid[row][col])
        self.requestRepaint()

    def addListener(self, listener):
        """Adds a color change listener

        @param listener
                   The color change listener
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#getColor()

        self.addListener(ColorChangeEvent, listener, self._COLOR_CHANGE_METHOD)

    def getColor(self):
        return self._colorGrid[self._x][self._y]

    def removeListener(self, listener):
        """Removes a color change listener

        @param listener
                   The listener
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#setColor(java.awt.Color)

        self.removeListener(ColorChangeEvent, listener)

    def setColor(self, color):
        self._colorGrid[self._x][self._y] = color
        self._changedColors.put(Point(self._x, self._y), color)
        self.requestRepaint()

    def setPosition(self, x, y):
        """Sets the position.

        @param x
                   the x
        @param y
                   the y
        """
        if x >= 0 and x < self._columns and y >= 0 and y < self._rows:
            self._x = x
            self._y = y

    def getPosition(self):
        """Gets the position.

        @return the position
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.ui.AbstractField#paintContent(com.vaadin.terminal.PaintTarget)

        return [self._x, self._y]

    def paintContent(self, target):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.AbstractField#changeVariables(java.lang.Object,
        # java.util.Map)

        target.addAttribute('rows', self._rows)
        target.addAttribute('columns', self._columns)
        if not self._changedColors.isEmpty():
            colors = [None] * len(self._changedColors)
            XCoords = [None] * len(self._changedColors)
            YCoords = [None] * len(self._changedColors)
            counter = 0
            for p in self._changedColors.keys():
                c = self._changedColors[p]
                if c is None:
                    continue
                red = Integer.toHexString.toHexString(c.getRed())
                red = '0' + red if len(red) < 2 else red
                green = Integer.toHexString.toHexString(c.getGreen())
                green = '0' + green if len(green) < 2 else green
                blue = Integer.toHexString.toHexString(c.getBlue())
                blue = '0' + blue if len(blue) < 2 else blue
                color = '#' + red + green + blue
                colors[counter] = color
                XCoords[counter] = String.valueOf.valueOf(p.getX())
                YCoords[counter] = String.valueOf.valueOf(p.getY())
                counter += 1
            target.addVariable(self, 'changedColors', colors)
            target.addVariable(self, 'changedX', XCoords)
            target.addVariable(self, 'changedY', YCoords)
            self._changedColors.clear()

    def changeVariables(self, source, variables):
        if 'selectedX' in variables and 'selectedY' in variables:
            self._x = int(str(variables['selectedX']))
            self._y = int(str(variables['selectedY']))
            self.fireColorChanged(self._colorGrid[self._y][self._x])
        if 'refresh' in variables and variables['refresh'] == False:
            _0 = True
            row = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    row += 1
                if not (row < self._rows):
                    break
                _1 = True
                col = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        col += 1
                    if not (col < self._columns):
                        break
                    self._changedColors.put(Point(row, col), self._colorGrid[row][col])
            self.requestRepaint()

    def fireColorChanged(self, color):
        """Notifies the listeners that a color change has occurred

        @param color
                   The color which it changed to
        """
        self.fireEvent(ColorChangeEvent(self, color))
