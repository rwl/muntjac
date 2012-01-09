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
