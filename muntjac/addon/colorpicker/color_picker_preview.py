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
