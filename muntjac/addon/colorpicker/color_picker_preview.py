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

from muntjac.addon.colorpicker.color import Color

from muntjac.ui.css_layout import CssLayout
from muntjac.ui.text_field import TextField

from muntjac.data.property import IValueChangeListener

from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_picker import IColorChangeListener
from muntjac.addon.colorpicker.color_selector import IColorSelector
from muntjac.data.validators.regexp_validator import RegexpValidator


_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')


class ColorPickerPreview(CssLayout, IColorSelector, IValueChangeListener):
    """The Class ColorPickerPreview.

    @author: John Ahlroos / ITMill Oy 2010
    @author: Richard Lincoln
    """

    _STYLE_DARK_COLOR = 'v-textfield-dark'
    _STYLE_LIGHT_COLOR = 'v-textfield-light'

    def __init__(self, color):
        """Instantiates a new color picker preview."""
        super(ColorPickerPreview, self).__init__()

        self.setStyleName('v-colorpicker-preview')
        self.setImmediate(True)

        self._color = color

        self._field = TextField()
        self._field.setReadOnly(True)
        self._field.setImmediate(True)
        self._field.setSizeFull()
        self._field.setStyleName('v-colorpicker-preview-textfield')
        self._field.setData(self)
        self._field.addListener(self, IValueChangeListener)
        self._field.addValidator(RegexpValidator('#[0-9a-fA-F]{6}', True, ''))
        self._oldValue = None
        self.addComponent(self._field)

        self.setColor(color)


    def setColor(self, color):
        self._color = color

        red = '%.2x' % color.getRed()
#        red = '0' + red if len(red) < 2 else red

        green = '%.2x' % color.getGreen()
#        green = '0' + green if len(green) < 2 else green

        blue = '%.2x' % color.getBlue()
#        blue = '0' + blue if len(blue) < 2 else blue

        # Unregister listener
        self._field.removeListener(self, IValueChangeListener)
        self._field.setReadOnly(False)

        self._field.setValue('#' + red + green + blue)

        if self._field.isValid():
            self._oldValue = '#' + red + green + blue
        else:
            self._field.setValue(self._oldValue)

        # Re-register listener
        self._field.setReadOnly(True)
        self._field.addListener(self, IValueChangeListener)

        # Set the text color
        self._field.removeStyleName(self._STYLE_DARK_COLOR)
        self._field.removeStyleName(self._STYLE_LIGHT_COLOR)
        if (self._color.getRed() + self._color.getGreen()
                + self._color.getBlue() < 3 * 128):
            self._field.addStyleName(self._STYLE_DARK_COLOR)
        else:
            self._field.addStyleName(self._STYLE_LIGHT_COLOR)

        self.requestRepaint()


    def getColor(self):
        return self._color


    def addListener(self, listener, iface=None):
        """Adds a color change listener

        @param listener:
                   The color change listener
        """
        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.registerListener(ColorChangeEvent, listener,
                    _COLOR_CHANGE_METHOD)

        super(ColorPickerPreview, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType  # set by decorator

        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPickerPreview, self).addCallback(callback, eventType,
                    *args)


    def removeListener(self, listener, iface=None):
        """Removes a color change listener

        @param listener:
                   The listener
        """
        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.withdrawListener(ColorChangeEvent, listener)

        super(ColorPickerPreview, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)

        else:
            super(ColorPickerPreview, self).removeCallback(callback, eventType)


    def valueChange(self, event):
        value = event.getProperty().getValue()

        if not self._field.isValid():
            self._field.setValue(self._oldValue)
            return
        else:
            self._oldValue = value

        if value is not None and len(value) == 7:
            red = int(value[1:3], 16)
            green = int(value[3:5], 16)
            blue = int(value[5:7], 16)
            self._color = Color(red, green, blue)

            evt = ColorChangeEvent(self._field.getData(), self._color)
            self.fireEvent(evt)


    def getCss(self, c):
        """Called when the component is refreshing"""
        red = '%.2x' % self._color.getRed()
#        red = '0' + red if len(red) < 2 else red

        green = '%.2x' % self._color.getGreen()
#        green = '0' + green if len(green) < 2 else green

        blue = '%.2x' % self._color.getBlue()
#        blue = '0' + blue if len(blue) < 2 else blue

        css = 'background: #' + red + green + blue
        return css
