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

from colorsys import hsv_to_rgb

from muntjac.addon.colorpicker.color import Color

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
        super(ColorPickerSelect, self).__init__()

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

        for Id in ColorRangePropertyId.values():
            self._range.addItem(Id)

        layout.addComponent(self._range)

        self._grid = ColorPickerGrid(self.createAllColors(14, 10))
        self._grid.setWidth('220px')
        self._grid.setHeight('270px')

        layout.addComponent(self._grid)

        self._range.select(ColorRangePropertyId.ALL)


    def createAllColors(self, rows, columns):
        """Creates the all colors.

        @param rows:
                   the rows
        @param columns:
                   the columns

        @return: the color[][]
        """
        colors = [([None] * columns) for _ in range(rows)]

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
        colors = [([None] * columns) for _ in range(rows)]
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

    @classmethod
    def values(cls):
        return [cls.ALL, cls.RED, cls.GREEN, cls.BLUE]


ColorRangePropertyId.ALL = ColorRangePropertyId('All colors')
ColorRangePropertyId.RED = ColorRangePropertyId('Red colors')
ColorRangePropertyId.GREEN = ColorRangePropertyId('Green colors')
ColorRangePropertyId.BLUE = ColorRangePropertyId('Blue colors')
