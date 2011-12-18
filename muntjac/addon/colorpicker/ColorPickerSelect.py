# -*- coding: utf-8 -*-
from com.vaadin.addon.colorpicker.ColorPickerGrid import (ColorPickerGrid,)
from com.vaadin.addon.colorpicker.ColorSelector import (ColorSelector,)
# from com.vaadin.ui.Select import (Select,)
# from java.awt.Color import (Color,)


class ColorPickerSelect(CustomComponent, ColorSelector, ValueChangeListener):
    """The Class ColorPickerSelect.

    @author John Ahlroos / ITMill Oy LTd 2010
    """
    # The range.
    _range = None
    # The grid.
    _grid = None

    class ColorRangePropertyId(object):
        """The Enum ColorRangePropertyId."""
        ALL = ['All colors']
        RED = ['Red colors']
        GREEN = ['Green colors']
        BLUE = ['Blue colors']
        _caption = None

        def __init__(self, caption):
            """Instantiates a new color range property id.

            @param caption
                       the caption
            """
            # (non-Javadoc)
            # 
            # @see java.lang.Enum#toString()

            self._caption = caption

        def toString(self):
            return self._caption

        _values = [ALL, RED, GREEN, BLUE]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    ColorRangePropertyId._enum_values = [ColorRangePropertyId(*v) for v in ColorRangePropertyId._enum_values]
    # The caption.

    def __init__(self):
        """Instantiates a new color picker select.

        @param rows
                   the rows
        @param columns
                   the columns
        """
        layout = VerticalLayout()
        self.setCompositionRoot(layout)
        self.setStyleName('colorselect')
        self.setWidth('220px')
        self._range = Select()
        self._range.setImmediate(True)
        self._range.setImmediate(True)
        self._range.setNullSelectionAllowed(False)
        self._range.setNewItemsAllowed(False)
        self._range.setWidth('220px')
        self._range.addListener(self)
        for id in self.ColorRangePropertyId.values():
            self._range.addItem(id)
        self._range.select(self.ColorRangePropertyId.ALL)
        layout.addComponent(self._range)
        self._grid = ColorPickerGrid(self.createAllColors(14, 10))
        self._grid.setWidth('220px')
        self._grid.setHeight('270px')
        layout.addComponent(self._grid)

    def createAllColors(self, rows, columns):
        """Creates the all colors.

        @param rows
                   the rows
        @param columns
                   the columns

        @return the color[][]
        """
        colors = [None] * columns
        _0 = True
        row = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                row += 1
            if not (row < rows):
                break
            _1 = True
            col = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    col += 1
                if not (col < columns):
                    break
                # Create the color grid by varying the saturation and value
                if row < rows - 1:
                    # Calculate new hue value
                    # The last row should have the black&white gradient
                    hue = col / columns
                    saturation = 1.0
                    value = 1.0
                    # For the upper half use value=1 and variable saturation
                    if row < rows / 2:
                        saturation = (row + 1.0) / rows / 2.0
                    else:
                        value = 1.0 - ((row - (rows / 2.0)) / rows / 2.0)
                    colors[row][col] = Color(Color.HSBtoRGB(hue, saturation, value))
                else:
                    hue = 0.0
                    saturation = 0.0
                    value = 1.0 - (col / columns)
                    colors[row][col] = Color(Color.HSBtoRGB(hue, saturation, value))
        return colors

    def createColor(self, color, rows, columns):
        """Creates the color.

        @param color
                   the color
        @param rows
                   the rows
        @param columns
                   the columns

        @return the color[][]
        """
        colors = [None] * columns
        hsv = [None] * 3
        Color.RGBtoHSB(color.getRed(), color.getGreen(), color.getBlue(), hsv)
        hue = hsv[0]
        saturation = 1.0
        value = 1.0
        _0 = True
        row = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                row += 1
            if not (row < rows):
                break
            _1 = True
            col = 0
            while True:
                if _1 is True:
                    _1 = False
                else:
                    col += 1
                if not (col < columns):
                    break
                index = (row * columns) + col
                saturation = 1.0
                value = 1.0
                if index <= (rows * columns) / 2:
                    saturation = index / (rows * columns) / 2.0
                else:
                    index -= (rows * columns) / 2
                    value = 1.0 - (index / (rows * columns) / 2.0)
                colors[row][col] = Color(Color.HSBtoRGB(hue, saturation, value))
        return colors

    def addListener(self, listener):
        """@param listener"""
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#getColor()

        self._grid.addListener(listener)

    def getColor(self):
        return self._grid.getColor()

    def removeListener(self, listener):
        """@param listener"""
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#setColor(java.awt.Color)

        self._grid.removeListener(listener)

    def setColor(self, color):
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.data.Property.ValueChangeListener#valueChange(com.vaadin.data
        # .Property.ValueChangeEvent)

        self._grid.getColor()

    def valueChange(self, event):
        if self._grid is None:
            return
        if event.getProperty().getValue() == self.ColorRangePropertyId.ALL:
            self._grid.setColorGrid(self.createAllColors(14, 10))
        elif event.getProperty().getValue() == self.ColorRangePropertyId.RED:
            self._grid.setColorGrid(self.createColor(Color(255, 0, 0), 14, 10))
        elif event.getProperty().getValue() == self.ColorRangePropertyId.GREEN:
            self._grid.setColorGrid(self.createColor(Color(0, 255, 0), 14, 10))
        elif event.getProperty().getValue() == self.ColorRangePropertyId.BLUE:
            self._grid.setColorGrid(self.createColor(Color(0, 0, 255), 14, 10))
