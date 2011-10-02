# -*- coding: utf-8 -*-
# from com.vaadin.data.Property import (Property,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.terminal.Sizeable import (Sizeable,)
# from com.vaadin.ui.Alignment import (Alignment,)
# from com.vaadin.ui.HorizontalSplitPanel import (HorizontalSplitPanel,)
# from com.vaadin.ui.OptionGroup import (OptionGroup,)
# from com.vaadin.ui.VerticalSplitPanel import (VerticalSplitPanel,)
# from java.util.Arrays import (Arrays,)


class SplitPanelPositioningExample(VerticalLayout):
    _measurePositionFromLeft = None
    _measurePositionFromTop = None
    _horizontalSplitPanel = None
    _verticalSplitPanel = None

    def __init__(self):
        self.setStyleName('split-panel-positioning-example')
        self.setSpacing(True)
        controls = HorizontalLayout()
        controls.setSpacing(True)
        self.addComponent(controls)
        self._verticalSplitPanel = VerticalSplitPanel()
        self._verticalSplitPanel.setSplitPosition(100, Sizeable.UNITS_PIXELS)
        self._verticalSplitPanel.setLocked(True)
        self._verticalSplitPanel.setHeight('450px')
        self._verticalSplitPanel.setWidth('100%')
        self.addComponent(self._verticalSplitPanel)
        # Add some content to the top
        topArea = ALabel()
        topArea.setStyleName('top-area')
        topArea.addStyleName('measured-from-top')
        topArea.setSizeFull()
        self._verticalSplitPanel.addComponent(topArea)
        # Add a horizontal split panel in the bottom area
        self._horizontalSplitPanel = HorizontalSplitPanel()
        self._horizontalSplitPanel.setSplitPosition(30, Sizeable.UNITS_PERCENTAGE)
        self._horizontalSplitPanel.setSizeFull()
        self._horizontalSplitPanel.setLocked(True)
        self._verticalSplitPanel.addComponent(self._horizontalSplitPanel)
        # Add some content to the left and right sides of the vertical layout
        leftArea = ALabel()
        leftArea.setStyleName('left-area')
        leftArea.addStyleName('measured-from-left')
        leftArea.setSizeFull()
        self._horizontalSplitPanel.addComponent(leftArea)
        rightArea = ALabel()
        rightArea.setStyleName('right-area')
        rightArea.setSizeFull()
        self._horizontalSplitPanel.addComponent(rightArea)
        # Allow user to set the splitter positioning
        self._measurePositionFromLeft = OptionGroup('Horizontal split position', Arrays.asList('30% from left', '30% from right'))
        self._measurePositionFromLeft.setValue('30% from left')
        self._measurePositionFromLeft.setImmediate(True)

        class _0_(Property.ValueChangeListener):

            def valueChange(self, event):
                if event.getProperty().getValue() == '30% from right':
                    # Measure 30% from the left
                    self.leftArea.removeStyleName('measured-from-left')
                    self.rightArea.removeStyleName('measured-from-bottom')
                    self.rightArea.addStyleName('measured-from-right')
                    SplitPanelPositioningExample_this._horizontalSplitPanel.setSplitPosition(30, Sizeable.UNITS_PERCENTAGE, True)
                else:
                    # Measure 30% from right
                    self.rightArea.removeStyleName('measured-from-right')
                    self.leftArea.removeStyleName('measured-from-bottom')
                    self.leftArea.addStyleName('measured-from-left')
                    SplitPanelPositioningExample_this._horizontalSplitPanel.setSplitPosition(30, Sizeable.UNITS_PERCENTAGE, False)

        _0_ = _0_()
        self._measurePositionFromLeft.addListener(_0_)
        controls.addComponent(self._measurePositionFromLeft)
        controls.setComponentAlignment(self._measurePositionFromLeft, Alignment.MIDDLE_CENTER)
        self._measurePositionFromTop = OptionGroup('Vertical split position', Arrays.asList('100px from top', '100px from bottom'))
        self._measurePositionFromTop.setValue('100px from top')
        self._measurePositionFromTop.setImmediate(True)

        class _1_(Property.ValueChangeListener):

            def valueChange(self, event):
                if event.getProperty().getValue() == '100px from bottom':
                    # Measure 100px from the bottom
                    self.topArea.removeStyleName('measured-from-top')
                    if (
                        SplitPanelPositioningExample_this._measurePositionFromLeft.getValue() == '30% from left'
                    ):
                        self.rightArea.addStyleName('measured-from-bottom')
                    else:
                        self.leftArea.addStyleName('measured-from-bottom')
                    SplitPanelPositioningExample_this._verticalSplitPanel.setSplitPosition(100, Sizeable.UNITS_PIXELS, True)
                else:
                    # Measure 100px from the top
                    if (
                        SplitPanelPositioningExample_this._measurePositionFromLeft.getValue() == '30% from left'
                    ):
                        self.rightArea.removeStyleName('measured-from-bottom')
                    else:
                        self.leftArea.removeStyleName('measured-from-bottom')
                    self.topArea.addStyleName('measured-from-top')
                    SplitPanelPositioningExample_this._verticalSplitPanel.setSplitPosition(100, Sizeable.UNITS_PIXELS, False)

        _1_ = _1_()
        self._measurePositionFromTop.addListener(_1_)
        controls.addComponent(self._measurePositionFromTop)
        controls.setComponentAlignment(self._measurePositionFromTop, Alignment.MIDDLE_CENTER)
