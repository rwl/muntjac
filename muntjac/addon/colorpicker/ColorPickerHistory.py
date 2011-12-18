# -*- coding: utf-8 -*-
from com.vaadin.addon.colorpicker.ColorPickerGrid import (ColorPickerGrid,)
from com.vaadin.addon.colorpicker.events.ColorChangeEvent import (ColorChangeEvent,)
from com.vaadin.addon.colorpicker.ColorPicker import (ColorPicker,)
from com.vaadin.addon.colorpicker.ColorSelector import (ColorSelector,)
# from com.vaadin.ui.CustomComponent import (CustomComponent,)
# from java.awt.Color import (Color,)
# from java.lang.reflect.Method import (Method,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Arrays import (Arrays,)
# from java.util.Collections import (Collections,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.concurrent.ArrayBlockingQueue import (ArrayBlockingQueue,)
ColorChangeListener = ColorPicker.ColorChangeListener


class ColorPickerHistory(CustomComponent, ColorSelector, ColorChangeListener):
    """The Class ColorPickerHistory.

    @author John Ahlroos
    """
    _STYLENAME = 'v-colorpicker-history'
    _COLOR_CHANGE_METHOD = None
    # This should never happen
    try:
        _COLOR_CHANGE_METHOD = ColorChangeListener.getDeclaredMethod('colorChanged', [ColorChangeEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in ColorPicker')
    # The rows.
    _rows = 4
    # The columns.
    _columns = 15
    # The colorHistory. This is common for all colorpickers
    _colorHistory = ArrayBlockingQueue(_rows * _columns)
    # The grid.
    _grid = None

    def __init__(self):
        """Instantiates a new color picker history."""
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.AbstractComponent#setHeight(java.lang.String)

        self.removeStyleName('v-customcomponent')
        self.setStyleName(self._STYLENAME)
        self._grid = ColorPickerGrid(self._rows, self._columns)
        self._grid.setWidth('100%')
        self._grid.setPosition(0, 0)
        self._grid.addListener(self)
        self.setCompositionRoot(self._grid)

    def setHeight(self, height):
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#setColor(java.awt.Color)

        super(ColorPickerHistory, self).setHeight(height)
        self._grid.setHeight(height)

    def setColor(self, color):
        # Check that the color does not already exist
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#getColor()

        exists = False
        iter = self._colorHistory
        while iter.hasNext():
            if color == iter.next():
                exists = True
                break
        # If the color does not exist then add it
        if not exists:
            if not self._colorHistory.offer(color):
                self._colorHistory.poll()
                self._colorHistory.offer(color)
        colorList = list(self._colorHistory)
        # Invert order of colors
        Collections.reverse(colorList)
        # Move the selected color to the front of the list
        Collections.swap(colorList, colorList.index(color), 0)
        # Create 2d color map
        colors = [None] * self._columns
        iter = colorList
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
                if iter.hasNext():
                    colors[row][col] = iter.next()
                else:
                    colors[row][col] = Color.WHITE
        self._grid.setColorGrid(colors)
        self._grid.requestRepaint()

    def getColor(self):
        return self._colorHistory.peek()

    def getHistory(self):
        """Gets the history.

        @return the history
        """
        array = list([None] * len(self._colorHistory))
        return Collections.unmodifiableList(Arrays.asList(array))

    def hasColor(self, c):
        """Checks for color.

        @param c
                   the c

        @return true, if successful
        """
        return self._colorHistory.contains(c)

    def addListener(self, listener):
        """Adds a color change listener

        @param listener
                   The listener
        """
        self.addListener(ColorChangeEvent, listener, self._COLOR_CHANGE_METHOD)

    def removeListener(self, listener):
        """Removes a color change listener

        @param listener
                   The listener
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.addon.colorpicker.ColorSelector.ColorChangeListener#colorChanged
        # (com.vaadin.addon.colorpicker.events.ColorChangeEvent)

        self.removeListener(ColorChangeEvent, listener)

    def colorChanged(self, event):
        self.fireEvent(ColorChangeEvent(self, event.getColor()))
