# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.SimpleFocusablePanel import (SimpleFocusablePanel,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.dom.client.Style.Position import (Position,)
# from com.google.gwt.dom.client.Style.Unit import (Unit,)
# from com.google.gwt.user.client.ui.impl.FocusImpl import (FocusImpl,)


class FocusElementPanel(SimpleFocusablePanel):
    """A panel that contains an always visible 0x0 size element that holds the focus
    for all browsers but IE6.
    """
    _focusElement = None

    def __init__(self):
        self._focusElement = Document.get().createDivElement()

    def setWidget(self, w):
        super(FocusElementPanel, self).setWidget(w)
        if not BrowserInfo.get().isIE6():
            if self._focusElement.getParentElement() is None:
                style = self._focusElement.getStyle()
                style.setPosition(Position.FIXED)
                style.setTop(0, Unit.PX)
                style.setLeft(0, Unit.PX)
                self.getElement().appendChild(self._focusElement)
                # Sink from focusElement too as focus and blur don't bubble
                DOM.sinkEvents(self._focusElement, Event.FOCUSEVENTS)
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
            FocusImpl.getFocusImplForPanel().focus(self._focusElement)
        else:
            FocusImpl.getFocusImplForPanel().blur(self._focusElement)

    def setTabIndex(self, tabIndex):
        if BrowserInfo.get().isIE6():
            super(FocusElementPanel, self).setTabIndex(tabIndex)
        else:
            self.getElement().setTabIndex(-1)
            if self._focusElement is not None:
                self._focusElement.setTabIndex(tabIndex)

    def getFocusElement(self):
        """@return the focus element"""
        return self._focusElement
