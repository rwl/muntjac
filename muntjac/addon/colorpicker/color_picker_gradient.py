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

    CLIENT_WIDGET = None #ClientWidget(VColorPickerGradient)

    TYPE_MAPPING = 'com.vaadin.addon.colorpicker.ColorPickerGradient'

    def __init__(self, Id, converter):
        """Instantiates a new color picker gradient.

        @param id:
                   the id
        @param converter:
                   the converter
        """
        super(ColorPickerGradient, self).__init__()

        #: The id.
        self._id = Id

        #: The converter.
        self._converter = converter

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
            bgRed = '%.2x' % self._backgroundColor.getRed()
#            bgRed = '0' + bgRed if len(bgRed) < 2 else bgRed
            bgGreen = '%.2x' % self._backgroundColor.getGreen()
#            bgGreen = '0' + bgGreen if len(bgGreen) < 2 else bgGreen
            bgBlue = '%.2x' % self._backgroundColor.getBlue()
#            bgBlue = '0' + bgBlue if len(bgBlue) < 2 else bgBlue
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
