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

from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.window import ICloseListener

from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_selector import IColorSelector


class IColorChangeListener(object):
    """The listener interface for receiving colorChange events. The class that
    is interested in processing a colorChange event implements this
    interface, and the object created with that class is registered with a
    component using the component's C{addColorChangeListener} method. When
    the colorChange event occurs, that object's appropriate
    method is invoked.

    @see: L{ColorChangeEvent}
    """

    def colorChanged(self, event):
        raise NotImplementedError


_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')


class ColorPicker(AbstractComponent, ICloseListener, IColorSelector,
            IColorChangeListener):
    """ColorPicker

    @author: John Ahlroos / ITMill Oy
    @author: Richard Lincoln
    """

    CLIENT_WIDGET = None #ClientWidget(VColorPickerButton)

    TYPE_MAPPING = 'com.vaadin.addon.colorpicker.ColorPicker'

    def __init__(self, caption='Colors', initialColor=None):
        """Instantiates a new color picker.

        @param caption:
                   the caption
        @param initialColor:
                   the initial color
        """
        self.buttonStyle = str(ButtonStyle.BUTTON_NORMAL)

        self.popupStyle = PopupStyle.POPUP_NORMAL

        self.buttonCaption = ''

        # The window.
        self._window = None

        # The window.
        self._parent_window = None

        # The popup status.
        self._popupStatus = False

        self._positionX = 0
        self._positionY = 0

        self.rgbVisible = True
        self.hsvVisible = True
        self.swatchesVisible = True
        self.historyVisible = True
        self.textfieldVisible = True

        if initialColor is None:
            initialColor = Color(0, 0, 0)

        # The color.
        self.color = initialColor
        self.caption = caption

        super(ColorPicker, self).__init__()


    def setColor(self, color):
        self.color = color
        if self._window is not None:
            self._window.setColor(color)
        self.requestRepaint()


    def getColor(self):
        return self.color


    def setPosition(self, x, y):
        """Sets the position of the popup window

        @param x:
                   the x-coordinate
        @param y:
                   the y-coordinate
        """
        self._positionX = x
        self._positionY = y
        if self._window is not None:
            self._window.setPositionX(x)
            self._window.setPositionY(y)


    def addListener(self, listener, iface=None):

        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.registerListener(ColorChangeEvent, listener,
                    _COLOR_CHANGE_METHOD)

        super(ColorPicker, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType  # set by decorator

        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPicker, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):

        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.withdrawListener(ColorChangeEvent, listener)

        super(ColorPicker, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)

        else:
            super(ColorPicker, self).removeCallback(callback, eventType)


    def paintContent(self, target):
        target.addAttribute('red', '%.2x' % self.color.getRed())
        target.addAttribute('green', '%.2x' % self.color.getGreen())
        target.addAttribute('blue', '%.2x' % self.color.getBlue())
        target.addAttribute('alpha', self.color.getAlpha())
        target.addAttribute('popup', self._popupStatus)
        target.addAttribute('btnstyle', self.buttonStyle)
        target.addAttribute('btncaption', self.buttonCaption)


    def changeVariables(self, source, variables):
        if 'popup' in variables:
            openPopup = variables['popup']
            if openPopup and not self.isReadOnly():
                if self._parent_window is None:
                    self._parent_window = self.getWindow()

                # Check that the parent is actually a browser
                # level window and not another sub-window
                if self._parent_window.getParent() is not None:
                    self._parent_window = self._parent_window.getParent()

                if self._window is None:
                    # Create the popup

                    from muntjac.addon.colorpicker.color_picker_popup \
                        import ColorPickerPopup

                    self._window = ColorPickerPopup(self.color)
                    self._window.setCaption(self.caption)

                    self._window.setRGBTabVisible(self.rgbVisible)
                    self._window.setHSVTabVisible(self.hsvVisible)
                    self._window.setSwatchesTabVisible(self.swatchesVisible)
                    self._window.setHistoryVisible(self.historyVisible)
                    self._window.setPreviewVisible(self.textfieldVisible)

                    self._window.setImmediate(True)
                    self._window.addListener(self, ICloseListener)
                    self._window.addListener(self, IColorChangeListener)

                    self._window.getHistory().setColor(self.color)
                    self._parent_window.addWindow(self._window)
                    self._window.setVisible(True)
                    self._window.setPositionX(self._positionX)
                    self._window.setPositionY(self._positionY)
                else:
                    self._window.setRGBTabVisible(self.rgbVisible)
                    self._window.setHSVTabVisible(self.hsvVisible)
                    self._window.setSwatchesTabVisible(self.swatchesVisible)
                    self._window.setHistoryVisible(self.historyVisible)
                    self._window.setPreviewVisible(self.textfieldVisible)

                    self._window.setColor(self.color)
                    self._window.getHistory().setColor(self.color)
                    self._window.setVisible(True)
                    self._parent_window.addWindow(self._window)
            elif self._window is not None:
                self._window.setVisible(False)
                self._parent_window.removeWindow(self._window)


    def windowClose(self, e):
        if e.getWindow() == self._window:
            self._popupStatus = False
            self.requestRepaint()


    def colorChanged(self, event):
        """Fired when a color change event occurs

        @param event:
                   The color change event
        """
        self.color = event.getColor()
        self.fireColorChanged()


    def fireColorChanged(self):
        """Notifies the listeners that the selected color has changed"""
        self.fireEvent(ColorChangeEvent(self, self.color))


    def setButtonStyle(self, style):
        """Sets the style of the button

        @param style:
                   The style
        """
        self.buttonStyle = str(style)


    def setPopupStyle(self, style):
        """The style for the popup window

        @param style:
                   The style
        """
        self.popupStyle = style

        if style == self.POPUP_NORMAL:
            self.setRGBVisibility(True)
            self.setHSVVisibility(True)
            self.setSwatchesVisibility(True)
            self.setHistoryVisibility(True)
            self.setTextfieldVisibility(True)
        elif style == self.POPUP_SIMPLE:
            self.setRGBVisibility(False)
            self.setHSVVisibility(False)
            self.setSwatchesVisibility(True)
            self.setHistoryVisibility(False)
            self.setTextfieldVisibility(False)


    def setButtonCaption(self, caption):
        """Sets the caption of the button. This replaces the css color code
        displayed as the caption.

        @param caption:
                   The caption of the button
        """
        self.buttonCaption = '' if caption is None else caption


    def setRGBVisibility(self, visible):
        """Set the visibility of the RGB Tab

        @param visible:
                   The visibility
        """
        if not visible and not self.hsvVisible and not self.swatchesVisible:
            raise ValueError('Cannot hide all tabs.')

        self.rgbVisible = visible
        if self._window is not None:
            self._window.setRGBTabVisible(visible)


    def setHSVVisibility(self, visible):
        """Set the visibility of the HSV Tab

        @param visible:
                   The visibility
        """
        if not visible and not self.rgbVisible and not self.swatchesVisible:
            raise ValueError('Cannot hide all tabs.')

        self.hsvVisible = visible
        if self._window is not None:
            self._window.setHSVTabVisible(visible)


    def setSwatchesVisibility(self, visible):
        """Set the visibility of the Swatches Tab

        @param visible:
                   The visibility
        """
        if not visible and not self.hsvVisible and not self.rgbVisible:
            raise ValueError('Cannot hide all tabs.')

        self.swatchesVisible = visible
        if self._window is not None:
            self._window.setSwatchesTabVisible(visible)


    def setHistoryVisibility(self, visible):
        """Sets the visibility of the Color History

        @param visible:
                   The visibility
        """
        self.historyVisible = visible
        if self._window is not None:
            self._window.setHistoryVisible(visible)


    def setTextfieldVisibility(self, visible):
        """Sets tje visibility of the CSS color code text field

        @param visible:
                   The visibility
        """
        self.textfieldVisible = visible
        if self._window is not None:
            self._window.setPreviewVisible(visible)


class ICoordinates2Color(object):
    """Interface for converting 2d-coordinates to a Color"""

    def calculate(self, c_or_x, y=None):
        """Calculate color from coordinates

        @param c_or_x:
                   the c or the x-coordinate
        @param y
                   the y-coordinate

        @return the integer array with the coordinates or the color
        """
        raise NotImplementedError


class ButtonStyle(object):

    BUTTON_NORMAL = None
    BUTTON_AREA = None

    _style = None

    def __init__(self, styleName):
        self._style = styleName

    def __str__(self):
        return self._style

ButtonStyle.BUTTON_NORMAL = ButtonStyle('normal')
ButtonStyle.BUTTON_AREA = ButtonStyle('area')


class PopupStyle(object):

    POPUP_NORMAL = None
    POPUP_SIMPLE = None

    _style = None

    def __init__(self, styleName):
        self._style = styleName

    def __str__(self):
        return self._style

PopupStyle.POPUP_NORMAL = PopupStyle('normal')
PopupStyle.POPUP_SIMPLE = PopupStyle('simple')
