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

from muntjac.ui.abstract_component import AbstractComponent

from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_picker import IColorChangeListener
from muntjac.addon.colorpicker.color_selector import IColorSelector


_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')


class ColorPickerGradient(AbstractComponent, IColorSelector):
    """The Class ColorPickerGradient.

    @author: John Ahlroos
    @author: Richard Lincoln
    """

    def __init__(self, Id, converter):
        """Instantiates a new color picker gradient.

        @param id:
                   the id
        @param converter:
                   the converter
        """
        #: The id.
        self._id = Id

        #: The converter.
        self._converter = None

        #: The foreground color.
        self._color = None

        #: The x-coordinate.
        self._x = 0

        #: The y-coordinate.
        self._y = 0

        #: The background color.
        self._backgroundColor = None

        self.requestRepaint()


    def setColor(self, c):
        self._color = c
        coords = self._converter.calculate(c)
        self._x = coords[0]
        self._y = coords[1]
        self.requestRepaint()


    def paintContent(self, target):
        target.addAttribute('cssid', self._id)

        if self._color is not None:
            target.addAttribute('cursorX', self._x)
            target.addAttribute('cursorY', self._y)

        if self._backgroundColor is not None:
            bgRed = hex(self._backgroundColor.getRed())
            bgRed = '0' + bgRed if len(bgRed) < 2 else bgRed
            bgGreen = hex(self._backgroundColor.getGreen())
            bgGreen = '0' + bgGreen if len(bgGreen) < 2 else bgGreen
            bgBlue = hex(self._backgroundColor.getBlue())
            bgBlue = '0' + bgBlue if len(bgBlue) < 2 else bgBlue
            target.addAttribute('bgColor', '#' + bgRed + bgGreen + bgBlue)


    def changeVariables(self, source, variables):
        if 'cursorX' in variables and 'cursorY' in variables:
            self._x = variables['cursorX']
            self._y = variables['cursorY']
            self._color = self._converter.calculate(self._x, self._y)
            self.fireColorChanged(self._color)


    def addListener(self, listener, iface=None):

        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.registerListener(ColorChangeEvent, listener,
                    _COLOR_CHANGE_METHOD)

        super(ColorPickerGradient, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType  # set by decorator

        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPickerGradient, self).addCallback(callback, eventType,
                    *args)


    def removeListener(self, listener, iface=None):

        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.withdrawListener(ColorChangeEvent, listener)

        super(ColorPickerGradient, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)

        else:
            super(ColorPickerGradient, self).removeCallback(callback,
                    eventType)


    def setBackgroundColor(self, color):
        """Sets the background color.

        @param color:
                   the new background color
        """
        self._backgroundColor = color
        self.requestRepaint()


    def getColor(self):
        return self._color


    def fireColorChanged(self, color):
        """Notifies the listeners that the color has changed

        @param color:
                   The color which it changed to
        """
        self.fireEvent(ColorChangeEvent(self, color))
