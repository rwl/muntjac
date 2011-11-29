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

from muntjac.terminal.gwt.client.ui.simple_focusable_panel \
    import SimpleFocusablePanel

from muntjac.terminal.gwt.client.browser_info import BrowserInfo


class FocusElementPanel(SimpleFocusablePanel):
    """A panel that contains an always visible 0x0 size element that holds
    the focus for all browsers but IE6.
    """

    def __init__(self):
        self._focusElement = DOM.createDiv()


    def setWidget(self, w):
        super(FocusElementPanel, self).setWidget(w)
        if not BrowserInfo.get().isIE6():
            if self._focusElement.getParentElement() is None:
                style = self._focusElement.getStyle()
                style.setPosition('fixed')
                style.setTop(0, 'px')
                style.setLeft(0, 'px')
                self.getElement().appendChild(self._focusElement)
                # Sink from focusElement too as focus and blur don't bubble
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
