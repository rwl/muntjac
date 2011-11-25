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

from pyjamas import DOM, Window
from pyjamas.Timer import Timer

from pyjamas.ui import Event
from pyjamas.ui.FlowPanel import FlowPanel

from muntjac.terminal.gwt.client.v_error_message import VErrorMessage
from muntjac.terminal.gwt.client.ui.v_overlay import VOverlay


class VTooltip(VOverlay):

    _CLASSNAME = 'v-tooltip'

    _MARGIN = 4

    TOOLTIP_EVENTS = (Event.ONKEYDOWN | Event.ONMOUSEOVER | Event.ONMOUSEOUT
            | Event.ONMOUSEMOVE | Event.ONCLICK)

    MAX_WIDTH = 500

    _QUICK_OPEN_TIMEOUT = 1000
    _CLOSE_TIMEOUT = 300
    _OPEN_DELAY = 750
    _QUICK_OPEN_DELAY = 100

    def __init__(self, client):
        self._em = VErrorMessage()
        self._description = DOM.createDiv()
        self._tooltipOwner = None
        self._closing = False
        self._opening = False
        self._ac = None

        #: Open next tooltip faster. Disabled after 2 sec of
        #  showTooltip-silence.
        self._justClosed = False

        #: If this is "additional" tooltip, this field contains the key for it
        self._tooltipKey = None

        super(VTooltip, self)(False, False, True)
        self._ac = client
        self.setStyleName(self._CLASSNAME)
        layout = FlowPanel()
        self.setWidget(layout)
        layout.add(self._em)
        DOM.setElemAttribute(self._description, 'className',
                self._CLASSNAME + '-text')
        DOM.appendChild(layout.getElement(), self._description)
        self.setSinkShadowEvents(self, True)


    def show(self, info):
        """Show a popup containing the information in the "info" tooltip.
        """
        hasContent = False
        if info.getErrorUidl() is not None:
            self._em.setVisible(True)
            self._em.updateFromUIDL(info.getErrorUidl())
            hasContent = True
        else:
            self._em.setVisible(False)

        if (info.getTitle() is not None) and (info.getTitle() != ''):
            DOM.setInnerHTML(self._description, info.getTitle())
            DOM.setStyleAttribute(self._description, 'display', '')
            hasContent = True
        else:
            DOM.setInnerHTML(self._description, '')
            DOM.setStyleAttribute(self._description, 'display', 'none')

        if hasContent:

            class _0_(PositionCallback):

                def setPosition(self, offsetWidth, offsetHeight):
                    if offsetWidth > self.MAX_WIDTH:
                        self.setWidth(self.MAX_WIDTH + 'px')

                    # Check new height and width with reflowed content
                    offsetWidth = self.getOffsetWidth()
                    offsetHeight = self.getOffsetHeight()

                    x = self.tooltipEventMouseX + 10 + self.Window.getScrollLeft()
                    y = self.tooltipEventMouseY + 10 + self.Window.getScrollTop()
                    if ((x + offsetWidth + self.MARGIN) -
                            Window.getScrollLeft() > Window.getClientWidth()):
                        x = Window.getClientWidth() - offsetWidth - self.MARGIN
                    if ((y + offsetHeight + self.MARGIN) -
                            Window.getScrollTop() > Window.getClientHeight()):
                        y = self.tooltipEventMouseY - 5 - offsetHeight
                        if y - self.Window.getScrollTop() < 0:
                            # tooltip does not fit on top of the mouse either,
                            # put it at the top of the screen
                            y = self.Window.getScrollTop()
                    self.setPopupPosition(x, y)
                    self.sinkEvents(Event.ONMOUSEOVER | Event.ONMOUSEOUT)

            _0_ = self._0_()
            self.setPopupPositionAndShow(_0_)
        else:
            self.hide()


    def showTooltip(self, owner, event, key):
        if (self._closing and (self._tooltipOwner == owner)
                and self._tooltipKey == key):
            # return to same tooltip, cancel closing
            self.closeTimer.cancel()
            self._closing = False
            self.justClosedTimer.cancel()
            self._justClosed = False
            return

        if self._closing:
            self.closeNow()

        self.updatePosition(event)
        if self._opening:
            self.showTimer.cancel()

        self._tooltipOwner = owner
        self._tooltipKey = key

        # Schedule timer for showing the tooltip according to if it was
        # recently closed or not.
        if self._justClosed:
            self.showTimer.schedule(self._QUICK_OPEN_DELAY)
        else:
            self.showTimer.schedule(self._OPEN_DELAY)

        self._opening = True


    def closeNow(self):
        if self._closing:
            self.hide()
            self._tooltipOwner = None
            self.setWidth('')
            self._closing = False


    class showTimer(Timer):

        def run(self):
            info = self.ac.getTooltipTitleInfo(self.tooltipOwner, self.tooltipKey)
            if None is not info:
                self.show(info)
            self.opening = False


    class closeTimer(Timer):

        def run(self):
            self.closeNow()
            self.justClosedTimer.schedule(2000)
            self.justClosed = True


    class justClosedTimer(Timer):

        def run(self):
            self.justClosed = False


    def hideTooltip(self):
        if self._opening:
            self.showTimer.cancel()
            self._opening = False
            self._tooltipOwner = None

        if not self.isAttached():
            return

        if self._closing:
            # already about to close
            return

        self.closeTimer.schedule(self._CLOSE_TIMEOUT)
        self._closing = True
        self._justClosed = True
        self.justClosedTimer.schedule(self._QUICK_OPEN_TIMEOUT)


    _tooltipEventMouseX = None
    _tooltipEventMouseY = None


    def updatePosition(self, event):
        self._tooltipEventMouseX = DOM.eventGetClientX(event)
        self._tooltipEventMouseY = DOM.eventGetClientY(event)


    def handleTooltipEvent(self, event, owner, key):
        etype = DOM.eventGetType(event)
        if VTooltip.TOOLTIP_EVENTS & etype == etype:
            if etype == Event.ONMOUSEOVER:
                self.showTooltip(owner, event, key)
            elif etype == Event.ONMOUSEMOVE:
                self.updatePosition(event)
            else:
                self.hideTooltip()
        else:
            # non-tooltip event, hide tooltip
            self.hideTooltip()


    def onBrowserEvent(self, event):
        etype = DOM.eventGetType(event)
        # cancel closing event if tooltip is mouseovered; the user might want
        # to scroll of cut&paste
        if etype == Event.ONMOUSEOVER:
            self.closeTimer.cancel()
            self._closing = False
            break
        elif etype == Event.ONMOUSEOUT:
            self.hideTooltip()
