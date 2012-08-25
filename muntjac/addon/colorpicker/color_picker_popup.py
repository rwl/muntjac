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

import sys
import traceback

from colorsys import hsv_to_rgb

from muntjac.ui.window import Window
from muntjac.ui.button import IClickListener, Button
from muntjac.ui.tab_sheet import TabSheet
from muntjac.ui.vertical_layout import VerticalLayout

from muntjac.addon.colorpicker.color import Color


from muntjac.addon.colorpicker.color_picker \
    import ICoordinates2Color, IColorChangeListener

from muntjac.addon.colorpicker.color_picker_history import ColorPickerHistory
from muntjac.addon.colorpicker.color_change_event import ColorChangeEvent
from muntjac.addon.colorpicker.color_picker_preview import ColorPickerPreview
from muntjac.addon.colorpicker.color_picker_select import ColorPickerSelect
from muntjac.addon.colorpicker.color_selector import IColorSelector
from muntjac.addon.colorpicker.color_picker_gradient import ColorPickerGradient
from muntjac.ui.horizontal_layout import HorizontalLayout
from muntjac.ui.alignment import Alignment
from muntjac.ui.slider import Slider, ValueOutOfBoundsException
from muntjac.data.property import IValueChangeListener


_COLOR_CHANGE_METHOD = getattr(IColorChangeListener, 'colorChanged')


class ColorPickerPopup(Window, IClickListener, IColorChangeListener,
            IColorSelector):
    """The Class ColorPickerPopup.

    @author: John Ahlroos / ITMill Oy
    @author: Richard Lincoln
    """

    _STYLENAME = 'v-colorpicker-popup'

    def __init__(self, initialColor):
        """Instantiates a new color picker popup."""

        #: The tabs.
        self._tabs = TabSheet()

        #: The layout.
        self._layout = VerticalLayout()

        #: The ok button.
        self._ok = Button('OK')

        #: The cancel button.
        self._cancel = Button('Cancel')

        #: The resize button.
        self._resize = Button('...')

        #: The selected color.
        self._selectedColor = Color.WHITE

        #: The history.
        self._history = None

        #: The history container.
        self._historyContainer = None

        #: The rgb gradient.
        self._rgbGradient = None

        #: The hsv gradient.
        self._hsvGradient = None

        #: The red slider.
        self._redSlider = None

        #: The green slider.
        self._greenSlider = None

        #: The blue slider.
        self._blueSlider = None

        #: The hue slider.
        self._hueSlider = None

        #: The saturation slider.
        self._saturationSlider = None

        #: The value slider.
        self._valueSlider = None

        #: The preview on the rgb tab.
        self._rgbPreview = None

        #: The preview on the hsv tab.
        self._hsvPreview = None

        #: The preview on the swatches tab.
        self._selPreview = None

        #: The color select.
        self._colorSelect = None

        #: The selectors.
        self._selectors = set()

        super(ColorPickerPopup, self).__init__()

        self._selectedColor = initialColor

        self.setWidth('250px')
        self.setScrollable(False)
        self.setStyleName(self._STYLENAME)
        self.setResizable(False)
        self.setImmediate(True)

        # Create the history
        self._history = ColorPickerHistory()
        self._history.addListener(self, IColorChangeListener)

        # Create the preview on the rgb tab
        self._rgbPreview = ColorPickerPreview(self._selectedColor)
        self._rgbPreview.setWidth('220px')
        self._rgbPreview.setHeight('20px')
        self._rgbPreview.addListener(self, IColorChangeListener)
        self._selectors.add(self._rgbPreview)

        # Create the preview on the hsv tab
        self._hsvPreview = ColorPickerPreview(self._selectedColor)
        self._hsvPreview.setWidth('220px')
        self._hsvPreview.setHeight('20px')
        self._hsvPreview.addListener(self, IColorChangeListener)
        self._selectors.add(self._hsvPreview)

        # Create the preview on the swatches tab
        self._selPreview = ColorPickerPreview(self._selectedColor)
        self._selPreview.setWidth('220px')
        self._selPreview.setHeight('20px')
        self._selPreview.addListener(self, IColorChangeListener)
        self._selectors.add(self._selPreview)

        # Set the layout
        self._layout.setSpacing(False)
        self._layout.setSizeFull()
        self.setContent(self._layout)

        # Create the tabs
        self._rgbTab = self.createRGBTab(self._selectedColor)
        self._tabs.addTab(self._rgbTab, 'RGB', None)

        self._hsvTab = self.createHSVTab(self._selectedColor)
        self._tabs.addTab(self._hsvTab, 'HSV', None)

        self._swatchesTab = self.createSelectTab()
        self._tabs.addTab(self._swatchesTab, 'Swatches', None)

        # Add the tabs
        self._tabs.setWidth('100%')

        self._layout.addComponent(self._tabs)

        # Add the history
        self._history.setWidth('97%')
        self._history.setHeight('27px')

        # Create the default colors
        defaultColors = list()
        defaultColors.append(Color.BLACK)
        defaultColors.append(Color.WHITE)

        # Create the history
        innerContainer = VerticalLayout()
        innerContainer.setSizeFull()
        innerContainer.addComponent(self._history)
        innerContainer.setExpandRatio(self._history, 1)

        outerContainer = VerticalLayout()
        outerContainer.setWidth('99%')
        outerContainer.setHeight('27px')
        outerContainer.addComponent(innerContainer)
        self._historyContainer = outerContainer

        self._layout.addComponent(self._historyContainer)

        # Add the resize button for the history
        self._resize.addListener(self, IClickListener)
        self._resize.setData(False)
        self._resize.setWidth('100%')
        self._resize.setHeight('10px')
        self._resize.setStyleName('resize-button')
        self._layout.addComponent(self._resize)

        # Add the buttons
        self._ok.setWidth('70px')
        self._ok.addListener(self, IClickListener)

        self._cancel.setWidth('70px')
        self._cancel.addListener(self, IClickListener)

        buttons = HorizontalLayout()
        buttons.addComponent(self._ok)
        buttons.addComponent(self._cancel)
        buttons.setWidth('100%')
        buttons.setHeight('30px')
        buttons.setComponentAlignment(self._ok, Alignment.MIDDLE_CENTER)
        buttons.setComponentAlignment(self._cancel, Alignment.MIDDLE_CENTER)
        self._layout.addComponent(buttons)

        self.setHeight(self.calculateHeight())


    def calculateHeight(self):
        """Calculates the height of the popup menu

        @return: Returns the height in CSS string representation
        """
        if self._historyContainer.isVisible():
            historyHeight = self._historyContainer.getHeight()
        else:
            historyHeight = 0

        tabsHeight = 0 if self._tabs.areTabsHidden() else 32
        contentHeight = 370
        buttonsHeight = 30
        previewHeight = 20 if self._rgbPreview.isVisible() else 0

        return (str(historyHeight + tabsHeight + contentHeight + buttonsHeight
                + previewHeight + 10) + 'px')


    def createRGBTab(self, color):
        """Creates the rgb tab.

        @return: the component
        """
        rgbLayout = VerticalLayout()
        rgbLayout.setMargin(False, False, True, False)
        rgbLayout.addComponent(self._rgbPreview)

        # Add the RGB color gradient
        self._rgbGradient = ColorPickerGradient('rgb-gradient', RGBConverter())
        self._rgbGradient.setColor(color)
        self._rgbGradient.addListener(self, IColorChangeListener)
        rgbLayout.addComponent(self._rgbGradient)
        self._selectors.add(self._rgbGradient)

        # Add the RGB sliders
        sliders = VerticalLayout()
        sliders.setStyleName('rgb-sliders')

        self._redSlider = Slider('Red', 0, 255)
        try:
            self._redSlider.setValue(color.getRed())
        except ValueOutOfBoundsException:
            pass

        self._redSlider.setImmediate(True)
        self._redSlider.setWidth('220px')
        self._redSlider.setStyleName('rgb-slider')
        self._redSlider.addStyleName('red')
        self._redSlider.addListener(RedValueChangeListener(self),
                IValueChangeListener)
        sliders.addComponent(self._redSlider)

        self._greenSlider = Slider('Green', 0, 255)
        try:
            self._greenSlider.setValue(color.getGreen())
        except ValueOutOfBoundsException:
            pass

        self._greenSlider.setStyleName('rgb-slider')
        self._greenSlider.addStyleName('green')
        self._greenSlider.setWidth('220px')
        self._greenSlider.setImmediate(True)
        self._greenSlider.addListener(GreenValueChangeListener(self),
                IValueChangeListener)
        sliders.addComponent(self._greenSlider)

        self._blueSlider = Slider('Blue', 0, 255)
        try:
            self._blueSlider.setValue(color.getBlue())
        except ValueOutOfBoundsException:
            pass

        self._blueSlider.setStyleName('rgb-slider')
        self._blueSlider.setStyleName('blue')
        self._blueSlider.setImmediate(True)
        self._blueSlider.setWidth('220px')
        self._blueSlider.addListener(BlueValueChangeListener(self),
                IValueChangeListener)
        sliders.addComponent(self._blueSlider)

        rgbLayout.addComponent(sliders)

        return rgbLayout


    def createHSVTab(self, color):
        """Creates the hsv tab.

        @return: the component
        """
        hsvLayout = VerticalLayout()
        hsvLayout.setMargin(False, False, True, False)
        hsvLayout.addComponent(self._hsvPreview)

        # Add the hsv gradient
        self._hsvGradient = ColorPickerGradient('hsv-gradient',
                HSVConverter(self))
        self._hsvGradient.setColor(color)
        self._hsvGradient.addListener(self, IColorChangeListener)
        hsvLayout.addComponent(self._hsvGradient)
        self._selectors.add(self._hsvGradient)

        # Add the hsv sliders
        hsv = color.getHSV()
        sliders = VerticalLayout()
        sliders.setStyleName('hsv-sliders')

        self._hueSlider = Slider('Hue', 0, 360)
        try:
            self._hueSlider.setValue(hsv[0])
        except ValueOutOfBoundsException:
            pass

        self._hueSlider.setStyleName('hsv-slider')
        self._hueSlider.addStyleName('hue-slider')
        self._hueSlider.setWidth('220px')
        self._hueSlider.setImmediate(True)
        self._hueSlider.addListener(HueValueChangeListener(self),
                IColorChangeListener)
        sliders.addComponent(self._hueSlider)

        self._saturationSlider = Slider('Saturation', 0, 100)
        try:
            self._saturationSlider.setValue(hsv[1])
        except ValueOutOfBoundsException:
            pass

        self._saturationSlider.setStyleName('hsv-slider')
        self._saturationSlider.setWidth('220px')
        self._saturationSlider.setImmediate(True)
        self._saturationSlider.addListener(SaturationValueChangeListener(self),
                IColorChangeListener)
        sliders.addComponent(self._saturationSlider)

        self._valueSlider = Slider('Value', 0, 100)
        try:
            self._valueSlider.setValue(hsv[2])
        except ValueOutOfBoundsException:
            pass

        self._valueSlider.setStyleName('hsv-slider')
        self._valueSlider.setWidth('220px')
        self._valueSlider.setImmediate(True)
        self._valueSlider.addListener(BrightnessValueChangeListener(self),
                IColorChangeListener)
        sliders.addComponent(self._valueSlider)

        hsvLayout.addComponent(sliders)

        return hsvLayout


    def createSelectTab(self):
        """Creates the select tab.

        @return: the component
        """
        selLayout = VerticalLayout()
        selLayout.setMargin(False, False, True, False)
        selLayout.addComponent(self._selPreview)

        self._colorSelect = ColorPickerSelect()
        self._colorSelect.addListener(self, IColorChangeListener)
        selLayout.addComponent(self._colorSelect)

        return selLayout


    def buttonClick(self, event):
        # History resize was clicked
        if event.getButton() == self._resize:
            state = self._resize.getData()

            # minimize
            if state:
                self._historyContainer.setHeight('27px')
                self._history.setHeight('27px')

            # maximize
            else:
                self._historyContainer.setHeight('90px')
                self._history.setHeight('80px')

            self.setHeight(self.calculateHeight())

            self._resize.setData(bool(not state))

        # Ok button was clicked
        elif event.getButton() == self._ok:
            self._history.setColor(self.getColor())
            self.fireColorChanged()
            self.close()

        # Cancel button was clicked
        elif event.getButton() == self._cancel:
            self.close()


    def fireColorChanged(self):
        """Notifies the listeners that the color changed"""
        self.fireEvent(ColorChangeEvent(self, self.getColor()))


    def getHistory(self):
        """Gets the history.

        @return: the history
        """
        return self._history


    def setColor(self, color):
        if color is None:
            return

        self._selectedColor = color

        self._hsvGradient.setColor(self._selectedColor)
        self._hsvPreview.setColor(self._selectedColor)

        self._rgbGradient.setColor(self._selectedColor)
        self._rgbPreview.setColor(self._selectedColor)

        self._selPreview.setColor(self._selectedColor)


    def getColor(self):
        return self._selectedColor


    def getColorHistory(self):
        """Gets the color history.

        @return: the color history
        """
        return list(self._history.getHistory())


    def colorChanged(self, event):
        self._selectedColor = event.getColor()
        try:
            self._redSlider.setValue(self._selectedColor.getRed())
            self._blueSlider.setValue(self._selectedColor.getBlue())
            self._greenSlider.setValue(self._selectedColor.getGreen())

            hsv = self._selectedColor.getHSV()

            self._hueSlider.setValue(hsv[0] * 360.0)
            self._saturationSlider.setValue(hsv[1] * 100.0)
            self._valueSlider.setValue(hsv[2] * 100.0)
        except ValueOutOfBoundsException:
            traceback.print_exc(file=sys.stdout)

        for s in self._selectors:
            if (event.getSource() != s and s is not self
                    and s.getColor() != self._selectedColor):
                s.setColor(self._selectedColor)


    def addListener(self, listener, iface=None):
        """Adds a color change listener

        @param listener:
                   The color change listener
        """
        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.registerListener(ColorChangeEvent, listener,
                    _COLOR_CHANGE_METHOD)

        super(ColorPickerPopup, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType  # set by decorator

        if issubclass(eventType, ColorChangeEvent):
            self.registerCallback(ColorChangeEvent, callback, None, *args)
        else:
            super(ColorPickerPopup, self).addCallback(callback, eventType,
                    *args)


    def removeListener(self, listener, iface=None):
        """Removes a color change listener

        @param listener:
                   The listener
        """
        if (isinstance(listener, IColorChangeListener) and
                (iface is None or issubclass(iface, IColorChangeListener))):
            self.withdrawListener(ColorChangeEvent, listener)

        super(ColorPickerPopup, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ColorChangeEvent):
            self.withdrawCallback(ColorChangeEvent, callback)

        else:
            super(ColorPickerPopup, self).removeCallback(callback, eventType)


    def tabIsVisible(self, tab):
        """Is the tab visible

        @param tab:
                   The tab to check
        """
        tabIterator = self._tabs.getComponentIterator()
        for t in tabIterator:
            if t == tab:
                return True
        return False


    def tabsNumVisible(self):
        """How many tabs are visible

        @return: The number of tabs visible
        """
        tabIterator = self._tabs.getComponentIterator()
        tabCounter = 0
        for _ in tabIterator:
            tabCounter += 1
        return tabCounter


    def checkIfTabsNeeded(self):
        """Checks if tabs are needed and hides them if not"""
        if self.tabsNumVisible() == 1:
            self._tabs.hideTabs(True)
            self.setHeight(self.calculateHeight())
        else:
            self._tabs.hideTabs(False)
            self.setHeight(self.calculateHeight())


    def setRGBTabVisible(self, visible):
        """Set RGB tab visibility

        @param visible:
                   The visibility of the RGB tab
        """
        if visible and not self.tabIsVisible(self._rgbTab):
            self._tabs.addTab(self._rgbTab, 'RGB', None)
            self.checkIfTabsNeeded()
        elif not visible and self.tabIsVisible(self._rgbTab):
            self._tabs.removeComponent(self._rgbTab)
            self.checkIfTabsNeeded()


    def setHSVTabVisible(self, visible):
        """Set HSV tab visibility

        @param visible:
                   The visibility of the HSV tab
        """
        if visible and not self.tabIsVisible(self._hsvTab):
            self._tabs.addTab(self._hsvTab, 'HSV', None)
            self.checkIfTabsNeeded()
        elif not visible and self.tabIsVisible(self._hsvTab):
            self._tabs.removeComponent(self._hsvTab)
            self.checkIfTabsNeeded()


    def setSwatchesTabVisible(self, visible):
        """Set Swatches tab visibility

        @param visible:
                   The visibility of the Swatches tab
        """
        if visible and not self.tabIsVisible(self._swatchesTab):
            self._tabs.addTab(self._swatchesTab, 'Swatches', None)
            self.checkIfTabsNeeded()
        elif not visible and self.tabIsVisible(self._swatchesTab):
            self._tabs.removeComponent(self._swatchesTab)
            self.checkIfTabsNeeded()


    def setHistoryVisible(self, visible):
        """Set the History visibility
        """
        self._historyContainer.setVisible(visible)
        self._resize.setVisible(visible)
        self.setHeight(self.calculateHeight())


    def setPreviewVisible(self, visible):
        """Set the preview visibility
        """
        self._hsvPreview.setVisible(visible)
        self._rgbPreview.setVisible(visible)
        self._selPreview.setVisible(visible)
        self.setHeight(self.calculateHeight())


    def attach(self):
        self.setHeight(self.calculateHeight())


# Implement the RGB color converter
class RGBConverter(ICoordinates2Color):

    def calculate(self, c_or_x, y=None):
        if y is None:
            c = c_or_x
            hsv = c.getHSV()

            x = round(hsv[0] * 220.0)
            y = 0

            # lower half
            if hsv[1] == 1.0:
                y = round(110.0 - ((hsv[1] + hsv[2]) * 110.0))
            else:
                y = round(hsv[1] * 110.0)

            return [x, y]
        else:
            x = c_or_x
            h = x / 220.0
            s = 1.0
            v = 1.0

            if y < 110:
                s = y / 110.0
            elif y > 110:
                v = 1.0 - ((y - 110.0) / 110.0)

            return Color(*hsv_to_rgb(h, s, v))


# Implement the HSV color converter
class HSVConverter(ICoordinates2Color):

    def __init__(self, cpp):
        self._cpp = cpp


    def calculate(self, c_or_x, y=None):
        if y is None:
            c = c_or_x
            hsv = c.getHSV()

            # Calculate coordinates
            x = round(hsv[2] * 220.0)
            y = round(220 - (hsv[1] * 220.0))

            # Create background color of clean color
            bgColor = Color(*hsv_to_rgb(hsv[0], 1.0, 1.0))
            self._cpp._hsvGradient.setBackgroundColor(bgColor)

            return [x, y]
        else:
            x = c_or_x
            saturation = 1.0 - (y / 220.0)
            value = x / 220.0
            hue = float(str(self._cpp._hueSlider.getValue())) / 360.0

            color = Color(*hsv_to_rgb(hue, saturation, value))
            return color


class _ColorValueChangeListener(IValueChangeListener):

    def __init__(self, cpp):
        self._cpp = cpp


class RedValueChangeListener(_ColorValueChangeListener):

    def valueChange(self, event):
        red = event.getProperty().getValue()
        newColor = Color(int(red), self._cpp._selectedColor.getGreen(),
                self._cpp._selectedColor.getBlue())
        self._cpp.setColor(newColor)


class GreenValueChangeListener(_ColorValueChangeListener):

    def valueChange(self, event):
        green = event.getProperty().getValue()
        newColor = Color(self._cpp._selectedColor.getRed(), int(green),
                self._cpp._selectedColor.getBlue())
        self._cpp.setColor(newColor)


class BlueValueChangeListener(_ColorValueChangeListener):

    def valueChange(self, event):
        blue = event.getProperty().getValue()
        newColor = Color(self._cpp._selectedColor.getRed(),
                self._cpp._selectedColor.getGreen(), int(blue))
        self._cpp.setColor(newColor)


class HueValueChangeListener(_ColorValueChangeListener):

    def valueChange(self, event):
        hue = float(str(event.getProperty().getValue())) / 360.0
        saturation = float(str(self._cpp._saturationSlider.getValue())) / 100.0
        value = float(str(self._cpp._valueSlider.getValue())) / 100.0

        # Set the color
        color = Color(*hsv_to_rgb(hue, saturation, value))
        self._cpp.setColor(color)

        # Set the background color of the hue gradient. This has to be
        # done here since in the conversion the base color information
        # is lost when color is black/white
        bgColor = Color(*hsv_to_rgb(hue, 1.0, 1.0))
        self._cpp._hsvGradient.setBackgroundColor(bgColor)


class SaturationValueChangeListener(_ColorValueChangeListener):

    def valueChange(self, event):
        hue = float(str(self._cpp._hueSlider.getValue())) / 360.0
        saturation = float(str(event.getProperty().getValue())) / 100.0
        value = float(str(self._cpp._valueSlider.getValue())) / 100.0

        self._cpp.setColor( Color(*hsv_to_rgb(hue, saturation, value)) )


class BrightnessValueChangeListener(_ColorValueChangeListener):

    def valueChange(self, event):
        hue = float(str(self._cpp._hueSlider.getValue())) / 360.0
        saturation = float(str(self._cpp._saturationSlider.getValue())) / 100.0
        value = float(str(event.getProperty().getValue())) / 100.0

        self._cpp.setColor( Color(*hsv_to_rgb(hue, saturation, value)) )
