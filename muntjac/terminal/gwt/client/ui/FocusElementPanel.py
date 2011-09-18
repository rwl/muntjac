# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.SimpleFocusablePanel import (SimpleFocusablePanel,)


class FocusElementPanel(SimpleFocusablePanel):
    """A panel that contains an always visible 0x0 size element that holds the focus
    for all browsers but IE6.
    """
    _focusElement = None

    def __init__(self):
        self._focusElement = self.Document.get().createDivElement()

    def setWidget(self, w):
        super(FocusElementPanel, self).setWidget(w)
        if not BrowserInfo.get().isIE6():
            if self._focusElement.getParentElement() is None:
                style = self._focusElement.getStyle()
                style.setPosition(self.Position.FIXED)
                style.setTop(0, self.Unit.PX)
                style.setLeft(0, self.Unit.PX)
                self.getElement().appendChild(self._focusElement)
                # Sink from focusElement too as focus and blur don't bubble
                self.DOM.sinkEvents(self._focusElement, self.Event.FOCUSEVENTS)
                # revert to original, not focusable
                self.getElement().setPropertyObject('tabIndex', None)
            else:
                self.moveFocusElementAfterWidget()

    def moveFocusElementAfterWidget(self):
        """Helper to keep focus element always in domChild[1]. Aids testing."""
        self.getElement().insertAfter(self._focusElement, self.getWidget().getElement())

    def setFocus(self, focus):
        if BrowserInfo.get().isIE6():
            super(FocusElementPanel, self).setFocus(focus)
        elif focus:
            self.FocusImpl.getFocusImplForPanel().focus(self._focusElement)
        else:
            self.FocusImpl.getFocusImplForPanel().blur(self._focusElement)

    def setTabIndex(self, tabIndex):
        if BrowserInfo.get().isIE6():
            super(FocusElementPanel, self).setTabIndex(tabIndex)
        else:
            self.getElement().setTabIndex(-1)
            if self._focusElement is not None:
                self._focusElement.setTabIndex(tabIndex)
