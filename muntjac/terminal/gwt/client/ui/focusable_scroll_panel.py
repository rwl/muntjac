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

from pyjamas import DOM

from pyjamas.ui import Event

from muntjac.terminal.gwt.client.ui.SimpleFocusablePanel \
    import SimpleFocusablePanel

from muntjac.terminal.gwt.client.BrowserInfo import BrowserInfo


class FocusableScrollPanel(SimpleFocusablePanel, HasScrollHandlers,
            ScrollHandler):
    """A scrollhandlers similar to L{ScrollPanel}."""

    def __init__(self, useFakeFocusElement=False):
        # Prevent IE standard mode bug when a AbsolutePanel is contained.
        style = self.getElement().getStyle()
        style.setOverflow('auto')
        style.setProperty('zoom', '1')
        style.setPosition('relative')

        if useFakeFocusElement:
            self._focusElement = DOM.createDiv()
        else:
            self._focusElement = None


    def useFakeFocusElement(self):
        return self._focusElement is not None


    def setWidget(self, w):
        super(FocusableScrollPanel, self).setWidget(w)
        if self.useFakeFocusElement():
            if self._focusElement.getParentElement() is None:
                style = self._focusElement.getStyle()
                if BrowserInfo.get().isIE6():
                    style.setOverflow('hidden')
                    style.setHeight(0, 'px')
                    style.setWidth(0, 'px')
                    style.setPosition('absolute')
                    self.addScrollHandler(self)
                else:
                    style.setPosition('fixed')
                    style.setTop(0, 'px')
                    style.setLeft(0, 'px')
                self.getElement().appendChild(self._focusElement)
                # Sink from focusElemet too as focusa and blur don't bubble
                DOM.sinkEvents(self._focusElement, Event.FOCUSEVENTS)
                # revert to original, not focusable
                self.getElement().setPropertyObject('tabIndex', None)
            else:
                self.moveFocusElementAfterWidget()


    def moveFocusElementAfterWidget(self):
        """Helper to keep focus element always in domChild[1]. Aids testing."""
        self.getElement().insertAfter(self._focusElement,
                self.getWidget().getElement())


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

        @return: the horizontal scroll position, in pixels
        """
        return self.getElement().getScrollLeft()


    def getScrollPosition(self):
        """Gets the vertical scroll position.

        @return: the vertical scroll position, in pixels
        """
        return self.getElement().getScrollTop()


    def setHorizontalScrollPosition(self, position):
        """Sets the horizontal scroll position.

        @param position:
                   the new horizontal scroll position, in pixels
        """
        self.getElement().setScrollLeft(position)


    def setScrollPosition(self, position):
        """Sets the vertical scroll position.

        @param position:
                   the new vertical scroll position, in pixels
        """
        self.getElement().setScrollTop(position)


    def onScroll(self, event):
        Scheduler.get().scheduleDeferred(ScrollCommand(self))


class ScrollCommand(ScheduledCommand):

    def __init__(self, panel):
        self._panel = panel

    def execute(self):
        self._panel._focusElement.getStyle().setTop(
                self._panel.getScrollPosition(), 'px')
        self._panel._focusElement.getStyle().setLeft(
                self._panel.getHorizontalScrollPosition(), 'px')
