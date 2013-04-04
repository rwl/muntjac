# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
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

from collections import deque

from muntjac.addon.colorpicker.color import Color

from muntjac.ui.custom_component import CustomComponent

from muntjac.addon.colorpicker.color_picker_grid import ColorPickerGrid
from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_picker import IColorChangeListener
from muntjac.addon.colorpicker.color_selector import IColorSelector


_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')


class ColorPickerHistory(CustomComponent, IColorSelector,
            IColorChangeListener):
    """The Class ColorPickerHistory.

    @author: John Ahlroos
    @author: Richard lincoln
    """

    _STYLENAME = 'v-colorpicker-history'

    #: The rows.
    _rows = 4

    #: The columns.
    _columns = 15

    #: The colorHistory. This is common for all colorpickers
    _colorHistory = deque()

    #: The grid.
    _grid = None


    def __init__(self):
        """Instantiates a new color picker history."""
        super(ColorPickerHistory, self).__init__()

        self.removeStyleName('v-customcomponent')
        self.setStyleName(self._STYLENAME)

        self._grid = ColorPickerGrid(self._rows, self._columns)
        self._grid.setWidth('100%')
        self._grid.setPosition(0, 0)
        self._grid.addListener(self, IColorChangeListener)

        self.setCompositionRoot(self._grid)


    def setHeight(self, height, unit=None):
        super(ColorPickerHistory, self).setHeight(height, unit)
        self._grid.setHeight(height, unit)


    def setColor(self, color):
        # Check that the color does not already exist
        exists = False
        for c in self._colorHistory:
            if color == c:
                exists = True
                break

        # If the color does not exist then add it
        if not exists:
            self._colorHistory.append(color)

        colorList = list(self._colorHistory)

        # Invert order of colors
        colorList.reverse()

        # Move the selected color to the front of the list
        colorList.insert(0, colorList.pop( colorList.index(color) ))

        # Create 2d color map
        colors = [([None] * self._columns) for _ in range(self._rows)]
        iterator = iter(colorList)

        for row in range(self._rows):
            for col in range(self._columns):
                try:
                    colors[row][col] = iterator.next()
                except StopIteration:
                    colors[row][col] = Color.WHITE

        self._grid.setColorGrid(colors)
        self._grid.requestRepaint()


    def getColor(self):
        return self._colorHistory[0]


    def getHistory(self):
        """Gets the history.

        @return: the history
        """
        array = list(self._colorHistory)
        return array


    def hasColor(self, c):
        """Checks for color.

        @param c:
                   the c
        @return: true, if successful
        """
        return c in self._colorHistory


    def addListener(self, listener, iface=None):
        """Adds a color change listener

        @param listener:
                   The color change listener
        """
        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.registerListener(ColorChangeEvent, listener,
                    _COLOR_CHANGE_METHOD)

        super(ColorPickerHistory, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType  # set by decorator

        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPickerHistory, self).addCallback(callback, eventType,
                    *args)


    def removeListener(self, listener, iface=None):
        """Removes a color change listener

        @param listener:
                   The listener
        """
        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.withdrawListener(ColorChangeEvent, listener)

        super(ColorPickerHistory, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)

        else:
            super(ColorPickerHistory, self).removeCallback(callback, eventType)


    def colorChanged(self, event):
        self.fireEvent(ColorChangeEvent(self, event.getColor()))
