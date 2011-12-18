# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
from com.vaadin.addon.colorpicker.ColorPickerHistory import (ColorPickerHistory,)
from com.vaadin.addon.colorpicker.events.ColorChangeEvent import (ColorChangeEvent,)
from com.vaadin.addon.colorpicker.ColorPickerPreview import (ColorPickerPreview,)
from com.vaadin.addon.colorpicker.ColorPicker import (ColorPicker,)
from com.vaadin.addon.colorpicker.ColorPickerSelect import (ColorPickerSelect,)
from com.vaadin.addon.colorpicker.ColorSelector import (ColorSelector,)
from com.vaadin.addon.colorpicker.ColorPickerGradient import (ColorPickerGradient,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.data.Property.ValueChangeListener import (ValueChangeListener,)
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.Button import (Button,)
# from com.vaadin.ui.Button.ClickEvent import (ClickEvent,)
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.HorizontalLayout import (HorizontalLayout,)
# from com.vaadin.ui.Layout import (Layout,)
# from com.vaadin.ui.Slider import (Slider,)
# from com.vaadin.ui.Slider.ValueOutOfBoundsException import (ValueOutOfBoundsException,)
# from com.vaadin.ui.TabSheet import (TabSheet,)
# from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
# from com.vaadin.ui.Window import (Window,)
# from java.awt.Color import (Color,)
# from java.lang.reflect.Method import (Method,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collections import (Collections,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.Set import (Set,)
Coordinates2Color = ColorPicker.Coordinates2Color
ColorChangeListener = ColorPicker.ColorChangeListener


class ColorPickerPopup(Window, ClickListener, ColorChangeListener, ColorSelector):
    """The Class ColorPickerPopup.

    @author John Ahlroos / ITMill Oy
    """
    _STYLENAME = 'v-colorpicker-popup'
    _COLOR_CHANGE_METHOD = None
    # This should never happen
    try:
        _COLOR_CHANGE_METHOD = ColorChangeListener.getDeclaredMethod('colorChanged', [ColorChangeEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in ColorPicker')
    # The tabs.
    _tabs = TabSheet()
    _rgbTab = None
    _hsvTab = None
    _swatchesTab = None
    # The layout.
    _layout = VerticalLayout()
    # The ok button.
    _ok = Button('OK')
    # The cancel button.
    _cancel = Button('Cancel')
    # The resize button.
    _resize = Button('...')
    # The selected color.
    _selectedColor = Color.WHITE
    # The history.
    _history = None
    # The history container.
    _historyContainer = None
    # The rgb gradient.
    _rgbGradient = None
    # The hsv gradient.
    _hsvGradient = None
    # The red slider.
    _redSlider = None
    # The green slider.
    _greenSlider = None
    # The blue slider.
    _blueSlider = None
    # The hue slider.
    _hueSlider = None
    # The saturation slider.
    _saturationSlider = None
    # The value slider.
    _valueSlider = None
    # The preview on the rgb tab.
    _rgbPreview = None
    # The preview on the hsv tab.
    _hsvPreview = None
    # The preview on the swatches tab.
    _selPreview = None
    # The color select.
    _colorSelect = None
    # The selectors.
    _selectors = set()

    def __init__(self, initialColor):
        """Instantiates a new color picker popup."""
        super(ColorPickerPopup, self)()
        self._selectedColor = initialColor
        self.setWidth('250px')
        self.setScrollable(False)
        self.setStyleName(self._STYLENAME)
        self.setResizable(False)
        self.setImmediate(True)
        # Create the history
        self._history = ColorPickerHistory()
        self._history.addListener(self)
        # Create the preview on the rgb tab
        self._rgbPreview = ColorPickerPreview(self._selectedColor)
        self._rgbPreview.setWidth('220px')
        self._rgbPreview.setHeight('20px')
        self._rgbPreview.addListener(self)
        self._selectors.add(self._rgbPreview)
        # Create the preview on the hsv tab
        self._hsvPreview = ColorPickerPreview(self._selectedColor)
        self._hsvPreview.setWidth('220px')
        self._hsvPreview.setHeight('20px')
        self._hsvPreview.addListener(self)
        self._selectors.add(self._hsvPreview)
        # Create the preview on the swatches tab
        self._selPreview = ColorPickerPreview(self._selectedColor)
        self._selPreview.setWidth('220px')
        self._selPreview.setHeight('20px')
        self._selPreview.addListener(self)
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
        defaultColors.add(Color.BLACK)
        defaultColors.add(Color.WHITE)
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
        self._resize.addListener(self)
        self._resize.setData(bool(False))
        self._resize.setWidth('100%')
        self._resize.setHeight('10px')
        self._resize.setStyleName('resize-button')
        self._layout.addComponent(self._resize)
        # Add the buttons
        self._ok.setWidth('70px')
        self._ok.addListener(self)
        self._cancel.setWidth('70px')
        self._cancel.addListener(self)
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

        @return Returns the height in CSS string representation
        """
        historyHeight = self._historyContainer.getHeight() if self._historyContainer.isVisible() else 0
        tabsHeight = 0 if self._tabs.areTabsHidden() else 32
        contentHeight = 370
        buttonsHeight = 30
        previewHeight = 20 if self._rgbPreview.isVisible() else 0
        return historyHeight + tabsHeight + contentHeight + buttonsHeight + previewHeight + 10 + 'px'

    def createRGBTab(self, color):
        """Creates the rgb tab.

        @return the component
        """
        rgbLayout = VerticalLayout()
        rgbLayout.setMargin(False, False, True, False)
        rgbLayout.addComponent(self._rgbPreview)
        # Implement the RGB color converter

        class RGBConverter(Coordinates2Color):

            def calculate(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    c, = _0
                    hsv = [None] * 3
                    Color.RGBtoHSB(c.getRed(), c.getGreen(), c.getBlue(), hsv)
                    x = self.Math.round(hsv[0] * 220.0)
                    y = 0
                    # lower half
                    if hsv[1] == 1.0:
                        y = self.Math.round(110.0 - ((hsv[1] + hsv[2]) * 110.0))
                    else:
                        y = self.Math.round(hsv[1] * 110.0)
                    return [x, y]
                elif _1 == 2:
                    x, y = _0
                    h = x / 220.0
                    s = 1.0
                    v = 1.0
                    if y < 110:
                        s = y / 110.0
                    elif y > 110:
                        v = 1.0 - ((y - 110.0) / 110.0)
                    return Color(Color.HSBtoRGB(h, s, v))
                else:
                    raise ARGERROR(1, 2)

        # Add the RGB color gradient
        self._rgbGradient = ColorPickerGradient('rgb-gradient', RGBConverter)
        self._rgbGradient.setColor(color)
        self._rgbGradient.addListener(self)
        rgbLayout.addComponent(self._rgbGradient)
        self._selectors.add(self._rgbGradient)
        # Add the RGB sliders
        sliders = VerticalLayout()
        sliders.setStyleName('rgb-sliders')
        self._redSlider = Slider('Red', 0, 255)
        try:
            self._redSlider.setValue(color.getRed())
        except ValueOutOfBoundsException, e:
            pass # astStmt: [Stmt([]), None]
        self._redSlider.setImmediate(True)
        self._redSlider.setWidth('220px')
        self._redSlider.setStyleName('rgb-slider')
        self._redSlider.addStyleName('red')

        class _1_(ValueChangeListener):

            def valueChange(self, event):
                red = event.getProperty().getValue()
                newColor = Color(red, ColorPickerPopup_this._selectedColor.getGreen(), ColorPickerPopup_this._selectedColor.getBlue())
                ColorPickerPopup_this.setColor(newColor)

        _1_ = _1_()
        self._redSlider.addListener(_1_)
        sliders.addComponent(self._redSlider)
        self._greenSlider = Slider('Green', 0, 255)
        try:
            self._greenSlider.setValue(color.getGreen())
        except ValueOutOfBoundsException, e:
            pass # astStmt: [Stmt([]), None]
        self._greenSlider.setStyleName('rgb-slider')
        self._greenSlider.addStyleName('green')
        self._greenSlider.setWidth('220px')
        self._greenSlider.setImmediate(True)

        class _2_(ValueChangeListener):

            def valueChange(self, event):
                green = event.getProperty().getValue()
                newColor = Color(ColorPickerPopup_this._selectedColor.getRed(), green, ColorPickerPopup_this._selectedColor.getBlue())
                ColorPickerPopup_this.setColor(newColor)

        _2_ = _2_()
        self._greenSlider.addListener(_2_)
        sliders.addComponent(self._greenSlider)
        self._blueSlider = Slider('Blue', 0, 255)
        try:
            self._blueSlider.setValue(color.getBlue())
        except ValueOutOfBoundsException, e:
            pass # astStmt: [Stmt([]), None]
        self._blueSlider.setStyleName('rgb-slider')
        self._blueSlider.setStyleName('blue')
        self._blueSlider.setImmediate(True)
        self._blueSlider.setWidth('220px')

        class _3_(ValueChangeListener):

            def valueChange(self, event):
                blue = event.getProperty().getValue()
                newColor = Color(ColorPickerPopup_this._selectedColor.getRed(), ColorPickerPopup_this._selectedColor.getGreen(), blue)
                ColorPickerPopup_this.setColor(newColor)

        _3_ = _3_()
        self._blueSlider.addListener(_3_)
        sliders.addComponent(self._blueSlider)
        rgbLayout.addComponent(sliders)
        return rgbLayout

    def createHSVTab(self, color):
        """Creates the hsv tab.

        @return the component
        """
        hsvLayout = VerticalLayout()
        hsvLayout.setMargin(False, False, True, False)
        hsvLayout.addComponent(self._hsvPreview)
        # Implement the HSV color converter

        class HSVConverter(Coordinates2Color):

            def calculate(self, *args):
                _0 = args
                _1 = len(args)
                if _1 == 1:
                    c, = _0
                    hsv = [None] * 3
                    Color.RGBtoHSB(c.getRed(), c.getGreen(), c.getBlue(), hsv)
                    # Calculate coordinates
                    x = self.Math.round(hsv[2] * 220.0)
                    y = self.Math.round(220 - (hsv[1] * 220.0))
                    # Create background color of clean color
                    bgColor = Color(Color.HSBtoRGB(hsv[0], 1.0, 1.0))
                    ColorPickerPopup_this._hsvGradient.setBackgroundColor(bgColor)
                    return [x, y]
                elif _1 == 2:
                    x, y = _0
                    saturation = 1.0 - (y / 220.0)
                    value = x / 220.0
                    hue = self.float(str(ColorPickerPopup_this._hueSlider.getValue())) / 360.0
                    color = Color(Color.HSBtoRGB(hue, saturation, value))
                    return color
                else:
                    raise ARGERROR(1, 2)

        # Add the hsv gradient
        self._hsvGradient = ColorPickerGradient('hsv-gradient', HSVConverter)
        self._hsvGradient.setColor(color)
        self._hsvGradient.addListener(self)
        hsvLayout.addComponent(self._hsvGradient)
        self._selectors.add(self._hsvGradient)
        # Add the hsv sliders
        hsv = [None] * 3
        Color.RGBtoHSB(color.getRed(), color.getGreen(), color.getBlue(), hsv)
        sliders = VerticalLayout()
        sliders.setStyleName('hsv-sliders')
        self._hueSlider = Slider('Hue', 0, 360)
        try:
            self._hueSlider.setValue(hsv[0])
        except ValueOutOfBoundsException, e1:
            pass # astStmt: [Stmt([]), None]
        self._hueSlider.setStyleName('hsv-slider')
        self._hueSlider.addStyleName('hue-slider')
        self._hueSlider.setWidth('220px')
        self._hueSlider.setImmediate(True)

        class _5_(ValueChangeListener):

            def valueChange(self, event):
                hue = self.float(str(event.getProperty().getValue())) / 360.0
                saturation = self.float(str(ColorPickerPopup_this._saturationSlider.getValue())) / 100.0
                value = self.float(str(ColorPickerPopup_this._valueSlider.getValue())) / 100.0
                # Set the color
                color = Color(Color.HSBtoRGB(hue, saturation, value))
                ColorPickerPopup_this.setColor(color)
                # Set the background color of the hue gradient. This has to be
                # done here since in the conversion the base color information
                # is lost when color is black/white

                bgColor = Color(Color.HSBtoRGB(hue, 1.0, 1.0))
                ColorPickerPopup_this._hsvGradient.setBackgroundColor(bgColor)

        _5_ = _5_()
        self._hueSlider.addListener(_5_)
        sliders.addComponent(self._hueSlider)
        self._saturationSlider = Slider('Saturation', 0, 100)
        try:
            self._saturationSlider.setValue(hsv[1])
        except ValueOutOfBoundsException, e1:
            pass # astStmt: [Stmt([]), None]
        self._saturationSlider.setStyleName('hsv-slider')
        self._saturationSlider.setWidth('220px')
        self._saturationSlider.setImmediate(True)

        class _6_(ValueChangeListener):

            def valueChange(self, event):
                hue = self.float(str(ColorPickerPopup_this._hueSlider.getValue())) / 360.0
                saturation = self.float(str(event.getProperty().getValue())) / 100.0
                value = self.float(str(ColorPickerPopup_this._valueSlider.getValue())) / 100.0
                ColorPickerPopup_this.setColor(Color(Color.HSBtoRGB(hue, saturation, value)))

        _6_ = _6_()
        self._saturationSlider.addListener(_6_)
        sliders.addComponent(self._saturationSlider)
        self._valueSlider = Slider('Value', 0, 100)
        try:
            self._valueSlider.setValue(hsv[2])
        except ValueOutOfBoundsException, e1:
            pass # astStmt: [Stmt([]), None]
        self._valueSlider.setStyleName('hsv-slider')
        self._valueSlider.setWidth('220px')
        self._valueSlider.setImmediate(True)

        class _7_(ValueChangeListener):

            def valueChange(self, event):
                hue = self.float(str(ColorPickerPopup_this._hueSlider.getValue())) / 360.0
                saturation = self.float(str(ColorPickerPopup_this._saturationSlider.getValue())) / 100.0
                value = self.float(str(event.getProperty().getValue())) / 100.0
                ColorPickerPopup_this.setColor(Color(Color.HSBtoRGB(hue, saturation, value)))

        _7_ = _7_()
        self._valueSlider.addListener(_7_)
        sliders.addComponent(self._valueSlider)
        hsvLayout.addComponent(sliders)
        return hsvLayout

    def createSelectTab(self):
        """Creates the select tab.

        @return the component
        """
        # (non-Javadoc)
        # 
        # @seecom.vaadin.ui.Button.ClickListener#buttonClick(com.vaadin.ui.Button.
        # ClickEvent)

        selLayout = VerticalLayout()
        selLayout.setMargin(False, False, True, False)
        selLayout.addComponent(self._selPreview)
        self._colorSelect = ColorPickerSelect()
        self._colorSelect.addListener(self)
        selLayout.addComponent(self._colorSelect)
        return selLayout

    def buttonClick(self, event):
        # History resize was clicked
        if event.getButton() == self._resize:
            # Ok button was clicked
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
        elif event.getButton() == self._ok:
            # Cancel button was clicked
            self._history.setColor(self.getColor())
            self.fireColorChanged()
            self.close()
        elif event.getButton() == self._cancel:
            self.close()

    def fireColorChanged(self):
        """Notifies the listeners that the color changed"""
        self.fireEvent(ColorChangeEvent(self, self.getColor()))

    def getHistory(self):
        """Gets the history.

        @return the history
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#setColor(java.awt.Color)

        return self._history

    def setColor(self, color):
        # (non-Javadoc)
        # 
        # @see com.vaadin.colorpicker.ColorSelector#getColor()

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

        @return the color history
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.colorpicker.ColorSelector.ColorChangeListener#changed(com.
        # vaadin.colorpicker.ColorSelector, java.awt.Color)

        return Collections.unmodifiableList(self._history.getHistory())

    def colorChanged(self, event):
        self._selectedColor = event.getColor()
        try:
            self._redSlider.setValue(self._selectedColor.getRed())
            self._blueSlider.setValue(self._selectedColor.getBlue())
            self._greenSlider.setValue(self._selectedColor.getGreen())
            hsv = [None] * 3
            Color.RGBtoHSB(self._selectedColor.getRed(), self._selectedColor.getGreen(), self._selectedColor.getBlue(), hsv)
            self._hueSlider.setValue(hsv[0] * 360.0)
            self._saturationSlider.setValue(hsv[1] * 100.0)
            self._valueSlider.setValue(hsv[2] * 100.0)
        except ValueOutOfBoundsException, e:
            e.printStackTrace()
        for s in self._selectors:
            if (
                event.getSource() != s and s is not self and s.getColor() != self._selectedColor
            ):
                s.setColor(self._selectedColor)

    def addListener(self, listener):
        """@param listener"""
        self.addListener(ColorChangeEvent, listener, self._COLOR_CHANGE_METHOD)

    def removeListener(self, listener):
        """@param listener"""
        self.removeListener(ColorChangeEvent, listener)

    def tabIsVisible(self, tab):
        """Is the tab visible

        @param tab
                   The tab to check
        @return
        """
        tabIterator = self._tabs.getComponentIterator()
        while tabIterator.hasNext():
            if tabIterator.next() == tab:
                return True
        return False

    def tabsNumVisible(self):
        """How many tabs are visible

        @return The number of tabs visible
        """
        tabIterator = self._tabs.getComponentIterator()
        tabCounter = 0
        while tabIterator.hasNext():
            tabIterator.next()
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

        @param visible
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

        @param visible
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

        @param visible
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

        @param visible
        """
        self._historyContainer.setVisible(visible)
        self._resize.setVisible(visible)
        self.setHeight(self.calculateHeight())

    def setPreviewVisible(self, visible):
        """Set the preview visibility

        @param visible
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Panel#attach()

        self._hsvPreview.setVisible(visible)
        self._rgbPreview.setVisible(visible)
        self._selPreview.setVisible(visible)
        self.setHeight(self.calculateHeight())

    def attach(self):
        self.setHeight(self.calculateHeight())
