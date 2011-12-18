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
from muntjac.ui.window import ICloseListener

from muntjac.addon.colorpicker.color_picker_popup import ColorPickerPopup
from muntjac.addon.colorpicker.events.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_selector import ColorSelector


class ColorChangeListener(object):
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


_COLOR_CHANGE_METHOD = getattr(ColorChangeListener, 'colorChanged')


class ColorPicker(AbstractComponent, ICloseListener, ColorSelector):
    """Colorpicker

    @author John Ahlroos / ITMill Oy
    """

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
        self._parent = None

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


    def addListener(self, listener):
        self.addListener(ColorChangeEvent, listener, self._COLOR_CHANGE_METHOD)


    def removeListener(self, listener):
        self.removeListener(ColorChangeEvent, listener)


    def paintContent(self, target):
        target.addAttribute('red', Integer.toHexString(self.color.getRed()))
        target.addAttribute('green', Integer.toHexString(self.color.getGreen()))
        target.addAttribute('blue', Integer.toHexString(self.color.getBlue()))
        target.addAttribute('alpha', self.color.getAlpha())
        target.addAttribute('popup', self._popupStatus)
        target.addAttribute('btnstyle', self.buttonStyle)
        target.addAttribute('btncaption', self.buttonCaption)


    def changeVariables(self, source, variables):
        if 'popup' in variables:
            openPopup = variables['popup']
            if openPopup and not self.isReadOnly():
                if self._parent is None:
                    self._parent = self.getWindow()

                # Check that the parent is actually a browser
                # level window and not another sub-window
                if self._parent.getParent() is not None:
                    self._parent = self._parent.getParent()

                if self._window is None:

                    # Create the popup
                    self._window = ColorPickerPopup(self.color)
                    self._window.setCaption(self.caption)

                    self._window.setRGBTabVisible(self.rgbVisible)
                    self._window.setHSVTabVisible(self.hsvVisible)
                    self._window.setSwatchesTabVisible(self.swatchesVisible)
                    self._window.setHistoryVisible(self.historyVisible)
                    self._window.setPreviewVisible(self.textfieldVisible)

                    self._window.setImmediate(True)
                    self._window.addListener(self)

                    ColorPicker_this = self

                    class _0_(ColorPicker.ColorChangeListener):

                        def colorChanged(self, event):
                            ColorPicker_this.colorChanged(event)

                    _0_ = _0_()
                    self._window.addListener(_0_)

                    self._window.getHistory().setColor(self.color)
                    self._parent.addWindow(self._window)
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
                    self._parent.addWindow(self._window)
            elif self._window is not None:
                self._window.setVisible(False)
                self._parent.removeWindow(self._window)


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
