# -*- coding: utf-8 -*-
from com.vaadin.addon.colorpicker.events.ColorChangeEvent import (ColorChangeEvent,)
from com.vaadin.addon.colorpicker.ColorPicker import (ColorPicker,)
from com.vaadin.addon.colorpicker.ColorSelector import (ColorSelector,)
# from com.vaadin.data.validator.RegexpValidator import (RegexpValidator,)
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.TextField import (TextField,)
# from java.awt.Color import (Color,)
# from java.lang.reflect.Method import (Method,)
ColorChangeListener = ColorPicker.ColorChangeListener


class ColorPickerPreview(CssLayout, ColorSelector, ValueChangeListener):
    """The Class ColorPickerPreview.

    @author John Ahlroos / ITMill Oy 2010
    """
    _STYLE_DARK_COLOR = 'v-textfield-dark'
    _STYLE_LIGHT_COLOR = 'v-textfield-light'
    _COLOR_CHANGE_METHOD = None
    # This should never happen
    try:
        _COLOR_CHANGE_METHOD = ColorChangeListener.getDeclaredMethod('colorChanged', [ColorChangeEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in ColorPicker')
    # The color.
    _color = None
    # The field.
    _field = None
    # The old value.
    _oldValue = None

    def __init__(self, color):
        """Instantiates a new color picker preview."""
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#setColor(java.awt.Color)

        self.setStyleName('v-colorpicker-preview')
        self.setImmediate(True)
        self._color = color
        self._field = TextField()
        self._field.setReadOnly(True)
        self._field.setImmediate(True)
        self._field.setSizeFull()
        self._field.setStyleName('v-colorpicker-preview-textfield')
        self._field.setData(self)
        self._field.addListener(self)
        self._field.addValidator(RegexpValidator('#[0-9a-fA-F]{6}', True, ''))
        self.addComponent(self._field)
        self.setColor(color)

    def setColor(self, color):
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#getColor()

        self._color = color
        red = Integer.toHexString.toHexString(color.getRed())
        red = '0' + red if len(red) < 2 else red
        green = Integer.toHexString.toHexString(color.getGreen())
        green = '0' + green if len(green) < 2 else green
        blue = Integer.toHexString.toHexString(color.getBlue())
        blue = '0' + blue if len(blue) < 2 else blue
        # Unregister listener
        self._field.removeListener(self)
        self._field.setReadOnly(False)
        self._field.setValue('#' + red + green + blue)
        if self._field.isValid():
            self._oldValue = '#' + red + green + blue
        else:
            self._field.setValue(self._oldValue)
        # Re-register listener
        self._field.setReadOnly(True)
        self._field.addListener(self)
        # Set the text color
        self._field.removeStyleName(self._STYLE_DARK_COLOR)
        self._field.removeStyleName(self._STYLE_LIGHT_COLOR)
        if (
            self._color.getRed() + self._color.getGreen() + self._color.getBlue() < 3 * 128
        ):
            self._field.addStyleName(self._STYLE_DARK_COLOR)
        else:
            self._field.addStyleName(self._STYLE_LIGHT_COLOR)
        self.requestRepaint()

    def getColor(self):
        return self._color

    def addListener(self, listener):
        """@param listener"""
        self.addListener(ColorChangeEvent, listener, self._COLOR_CHANGE_METHOD)

    def removeListener(self, listener):
        """@param listener"""
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.data.Property.ValueChangeListener#valueChange(com.vaadin.data
        # .Property.ValueChangeEvent)

        self.removeListener(ColorChangeEvent, listener)

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
            self.fireEvent(ColorChangeEvent(self._field.getData(), self._color))

    def getCss(self, c):
        """Called when the component is refreshing"""
        red = Integer.toHexString.toHexString(self._color.getRed())
        red = '0' + red if len(red) < 2 else red
        green = Integer.toHexString.toHexString(self._color.getGreen())
        green = '0' + green if len(green) < 2 else green
        blue = Integer.toHexString.toHexString(self._color.getBlue())
        blue = '0' + blue if len(blue) < 2 else blue
        css = 'background: #' + red + green + blue
        return css
