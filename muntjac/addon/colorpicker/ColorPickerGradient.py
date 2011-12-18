# -*- coding: utf-8 -*-
from com.vaadin.addon.colorpicker.events.ColorChangeEvent import (ColorChangeEvent,)
from com.vaadin.addon.colorpicker.ColorPicker import (ColorPicker,)
from com.vaadin.addon.colorpicker.ColorSelector import (ColorSelector,)
# from java.awt.Color import (Color,)
# from java.lang.reflect.Method import (Method,)
# from java.util.Map import (Map,)
ColorChangeListener = ColorPicker.ColorChangeListener


class ColorPickerGradient(AbstractComponent, ColorSelector):
    """The Class ColorPickerGradient.

    @author John Ahlroos
    """
    _COLOR_CHANGE_METHOD = None
    # This should never happen
    try:
        _COLOR_CHANGE_METHOD = ColorChangeListener.getDeclaredMethod('colorChanged', [ColorChangeEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in ColorPicker')
    # The id.
    _id = None
    # The converter.
    _converter = None
    # The foreground color.
    _color = None
    # The x-coordinate.
    _x = 0
    # The y-coordinate.
    _y = 0
    # The background color.
    _backgroundColor = None

    def __init__(self, id, converter):
        """Instantiates a new color picker gradient.

        @param id
                   the id
        @param converter
                   the converter
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#setColor(java.awt.Color)

        self._id = id
        self._converter = converter
        self.requestRepaint()

    def setColor(self, c):
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.ui.AbstractField#paintContent(com.vaadin.terminal.PaintTarget)

        self._color = c
        coords = self._converter.calculate(c)
        self._x = coords[0]
        self._y = coords[1]
        self.requestRepaint()

    def paintContent(self, target):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.AbstractField#changeVariables(java.lang.Object,
        # java.util.Map)

        target.addAttribute('cssid', self._id)
        if self._color is not None:
            target.addAttribute('cursorX', self._x)
            target.addAttribute('cursorY', self._y)
        if self._backgroundColor is not None:
            bgRed = Integer.toHexString.toHexString(self._backgroundColor.getRed())
            bgRed = '0' + bgRed if len(bgRed) < 2 else bgRed
            bgGreen = Integer.toHexString.toHexString(self._backgroundColor.getGreen())
            bgGreen = '0' + bgGreen if len(bgGreen) < 2 else bgGreen
            bgBlue = Integer.toHexString.toHexString(self._backgroundColor.getBlue())
            bgBlue = '0' + bgBlue if len(bgBlue) < 2 else bgBlue
            target.addAttribute('bgColor', '#' + bgRed + bgGreen + bgBlue)

    def changeVariables(self, source, variables):
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.colorpicker.ColorSelector#addListener(com.vaadin.colorpicker
        # .ColorSelector.ColorChangeListener)

        if 'cursorX' in variables and 'cursorY' in variables:
            self._x = variables['cursorX']
            self._y = variables['cursorY']
            self._color = self._converter.calculate(self._x, self._y)
            self.fireColorChanged(self._color)

    def addListener(self, listener):
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.colorpicker.ColorSelector#removeListener(com.vaadin.colorpicker
        # .ColorSelector.ColorChangeListener)

        self.addListener(ColorChangeEvent, listener, self._COLOR_CHANGE_METHOD)

    def removeListener(self, listener):
        self.removeListener(ColorChangeEvent, listener)

    def setBackgroundColor(self, color):
        """Sets the background color.

        @param color
                   the new background color
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#getColor()

        self._backgroundColor = color
        self.requestRepaint()

    def getColor(self):
        return self._color

    def fireColorChanged(self, color):
        """Notifies the listeners that the color has changed

        @param color
                   The color which it changed to
        """
        self.fireEvent(ColorChangeEvent(self, color))
