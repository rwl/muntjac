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

from colorsys import hsv_to_rgb

from muntjac.util import Color

from muntjac.ui.custom_component import CustomComponent
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.select import Select

from muntjac.data.property import IValueChangeListener

from muntjac.addon.colorpicker.color_picker_grid import ColorPickerGrid
from muntjac.addon.colorpicker.color_selector import IColorSelector


class ColorPickerSelect(CustomComponent, IColorSelector, IValueChangeListener):
    """The Class ColorPickerSelect.

    @author: John Ahlroos / ITMill Oy LTd 2010
    @author: Richard Lincoln
    """

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
        self._range.addListener(self, IValueChangeListener)

        for Id in self.ColorRangePropertyId.values():
            self._range.addItem(Id)

        self._range.select(ColorRangePropertyId.ALL)

        layout.addComponent(self._range)

        self._grid = ColorPickerGrid(self.createAllColors(14, 10))
        self._grid.setWidth('220px')
        self._grid.setHeight('270px')

        layout.addComponent(self._grid)


    def createAllColors(self, rows, columns):
        """Creates the all colors.

        @param rows:
                   the rows
        @param columns:
                   the columns

        @return: the color[][]
        """
        colors = [([None] * rows) for _ in columns]

        for row in range(rows):
            for col in range(columns):

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

                    colors[row][col] = \
                            Color(*hsv_to_rgb(hue, saturation, value))
                else:
                    hue = 0.0
                    saturation = 0.0
                    value = 1.0 - (col / columns)

                    colors[row][col] = \
                            Color(*hsv_to_rgb(hue, saturation, value))

        return colors


    def createColor(self, color, rows, columns):
        """Creates the color.

        @param color:
                   the color
        @param rows:
                   the rows
        @param columns:
                   the columns

        @return: the color[][]
        """
        colors = [None] * columns
        hsv = color.getHSV()

        hue = hsv[0]
        saturation = 1.0
        value = 1.0

        for row in range(rows):
            for col in range(columns):

                index = (row * columns) + col
                saturation = 1.0
                value = 1.0

                if index <= (rows * columns) / 2:
                    saturation = index / (rows * columns) / 2.0
                else:
                    index -= (rows * columns) / 2
                    value = 1.0 - (index / (rows * columns) / 2.0)

                colors[row][col] = Color(*hsv_to_rgb(hue, saturation, value))

        return colors


    def addListener(self, listener, iface=None):
        self._grid.addListener(listener, iface)


    def removeListener(self, listener, iface=None):
        self._grid.removeListener(listener, iface)


    def getColor(self):
        return self._grid.getColor()


    def setColor(self, color):
        self._grid.getColor()


    def valueChange(self, event):
        if self._grid is None:
            return

        if event.getProperty().getValue() == ColorRangePropertyId.ALL:
            self._grid.setColorGrid(self.createAllColors(14, 10))

        elif event.getProperty().getValue() == ColorRangePropertyId.RED:
            self._grid.setColorGrid(self.createColor(Color(255, 0, 0), 14, 10))

        elif event.getProperty().getValue() == ColorRangePropertyId.GREEN:
            self._grid.setColorGrid(self.createColor(Color(0, 255, 0), 14, 10))

        elif event.getProperty().getValue() == ColorRangePropertyId.BLUE:
            self._grid.setColorGrid(self.createColor(Color(0, 0, 255), 14, 10))


class ColorRangePropertyId(object):
    """The Enum ColorRangePropertyId."""

    ALL = None
    RED = None
    GREEN = None
    BLUE = None

    def __init__(self, caption):
        """Instantiates a new color range property id.

        @param caption:
                   the caption
        """
        self._caption = caption

    def __str__(self):
        return self._caption


ColorRangePropertyId.ALL = ColorRangePropertyId('All colors')
ColorRangePropertyId.RED = ColorRangePropertyId('Red colors')
ColorRangePropertyId.GREEN = ColorRangePropertyId('Green colors')
ColorRangePropertyId.BLUE = ColorRangePropertyId('Blue colors')
