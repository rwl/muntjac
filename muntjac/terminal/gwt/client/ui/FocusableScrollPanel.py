# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.SimpleFocusablePanel import (SimpleFocusablePanel,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.event.dom.client.HasScrollHandlers import (HasScrollHandlers,)
# from com.google.gwt.user.client.ui.ScrollPanel import (ScrollPanel,)


class FocusableScrollPanel(SimpleFocusablePanel, HasScrollHandlers, ScrollHandler):
    """A scrollhandlers similar to {@link ScrollPanel}."""

    def __init__(self, *args):
        # Prevent IE standard mode bug when a AbsolutePanel is contained.
        _0 = args
        _1 = len(args)
        if _1 == 0:
            style = self.getElement().getStyle()
            style.setOverflow(Overflow.AUTO)
            style.setProperty('zoom', '1')
            style.setPosition(Position.RELATIVE)
        elif _1 == 1:
            useFakeFocusElement, = _0
            self.__init__()
            if useFakeFocusElement:
                self._focusElement = Document.get().createDivElement()
        else:
            raise ARGERROR(0, 1)

    _focusElement = None

    def useFakeFocusElement(self):
        return self._focusElement is not None

    def setWidget(self, w):
        super(FocusableScrollPanel, self).setWidget(w)
        if self.useFakeFocusElement():
            if self._focusElement.getParentElement() is None:
                style = self._focusElement.getStyle()
                if BrowserInfo.get().isIE6():
                    style.setOverflow(Overflow.HIDDEN)
                    style.setHeight(0, Unit.PX)
                    style.setWidth(0, Unit.PX)
                    style.setPosition(Position.ABSOLUTE)
                    self.addScrollHandler(self)
                else:
                    style.setPosition(Position.FIXED)
                    style.setTop(0, Unit.PX)
                    style.setLeft(0, Unit.PX)
                self.getElement().appendChild(self._focusElement)
                # Sink from focusElemet too as focusa and blur don't bubble
                DOM.sinkEvents(self._focusElement, Event.FOCUSEVENTS)
                # revert to original, not focusable
                self.getElement().setPropertyObject('tabIndex', None)
            else:
                self.moveFocusElementAfterWidget()

    def moveFocusElementAfterWidget(self):
        """Helper to keep focus element always in domChild[1]. Aids testing."""
        self.getElement().insertAfter(self._focusElement, self.getWidget().getElement())

    def setFocus(self, focus):
        if self.useFakeFocusElement():
            if focus:
                FocusImpl.getFocusImplForPanel().focus(self._focusElement)
            else:
                FocusImpl.getFocusImplForPanel().blur(self._focusElement)
        else:
            super(FocusableScrollPanel, self).setFocus(focus)

    def setTabIndex(self, tabIndex):
        if self.useFakeFocusElement():
            self.getElement().setTabIndex(-1)
            if self._focusElement is not None:
                self._focusElement.setTabIndex(tabIndex)
        else:
            super(FocusableScrollPanel, self).setTabIndex(tabIndex)

    def addScrollHandler(self, handler):
        return self.addDomHandler(handler, ScrollEvent.getType())

    def getHorizontalScrollPosition(self):
        """Gets the horizontal scroll position.

        @return the horizontal scroll position, in pixels
        """
        return self.getElement().getScrollLeft()

    def getScrollPosition(self):
        """Gets the vertical scroll position.

        @return the vertical scroll position, in pixels
        """
        return self.getElement().getScrollTop()

    def setHorizontalScrollPosition(self, position):
        """Sets the horizontal scroll position.

        @param position
                   the new horizontal scroll position, in pixels
        """
        self.getElement().setScrollLeft(position)

    def setScrollPosition(self, position):
        """Sets the vertical scroll position.

        @param position
                   the new vertical scroll position, in pixels
        """
        self.getElement().setScrollTop(position)

    def onScroll(self, event):

        class _0_(ScheduledCommand):

            def execute(self):
                FocusableScrollPanel_this._focusElement.getStyle().setTop(FocusableScrollPanel_this.getScrollPosition(), Unit.PX)
                FocusableScrollPanel_this._focusElement.getStyle().setLeft(FocusableScrollPanel_this.getHorizontalScrollPosition(), Unit.PX)

        _0_ = _0_()
        Scheduler.get().scheduleDeferred(_0_)
