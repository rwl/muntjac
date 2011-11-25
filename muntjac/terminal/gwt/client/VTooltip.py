# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.VErrorMessage import (VErrorMessage,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from com.google.gwt.user.client.ui.FlowPanel import (FlowPanel,)


class VTooltip(VOverlay):
    """TODO open for extension"""
    _CLASSNAME = 'v-tooltip'
    _MARGIN = 4
    TOOLTIP_EVENTS = (((Event.ONKEYDOWN | Event.ONMOUSEOVER) | Event.ONMOUSEOUT) | Event.ONMOUSEMOVE) | Event.ONCLICK
    MAX_WIDTH = 500
    _QUICK_OPEN_TIMEOUT = 1000
    _CLOSE_TIMEOUT = 300
    _OPEN_DELAY = 750
    _QUICK_OPEN_DELAY = 100
    _em = VErrorMessage()
    _description = DOM.createDiv()
    _tooltipOwner = None
    _closing = False
    _opening = False
    _ac = None
    # Open next tooltip faster. Disabled after 2 sec of showTooltip-silence.
    _justClosed = False
    # If this is "additional" tooltip, this field contains the key for it
    _tooltipKey = None

    def __init__(self, client):
        super(VTooltip, self)(False, False, True)
        self._ac = client
        self.setStyleName(self._CLASSNAME)
        layout = FlowPanel()
        self.setWidget(layout)
        layout.add(self._em)
        DOM.setElementProperty(self._description, 'className', self._CLASSNAME + '-text')
        DOM.appendChild(layout.getElement(), self._description)
        self.setSinkShadowEvents(True)

    def show(self, info):
        """Show a popup containing the information in the "info" tooltip

        @param info
        """
        hasContent = False
        if info.getErrorUidl() is not None:
            self._em.setVisible(True)
            self._em.updateFromUIDL(info.getErrorUidl())
            hasContent = True
        else:
            self._em.setVisible(False)
        if info.getTitle() is not None and not ('' == info.getTitle()):
            DOM.setInnerHTML(self._description, info.getTitle())
            DOM.setStyleAttribute(self._description, 'display', '')
            hasContent = True
        else:
            DOM.setInnerHTML(self._description, '')
            DOM.setStyleAttribute(self._description, 'display', 'none')
        if hasContent:

            class _0_(self.PositionCallback):

                def setPosition(self, offsetWidth, offsetHeight):
                    if offsetWidth > VTooltip_this.MAX_WIDTH:
                        self.setWidth(VTooltip_this.MAX_WIDTH + 'px')
                        # Check new height and width with reflowed content
                        offsetWidth = self.getOffsetWidth()
                        offsetHeight = self.getOffsetHeight()
                    x = VTooltip_this._tooltipEventMouseX + 10 + Window.getScrollLeft()
                    y = VTooltip_this._tooltipEventMouseY + 10 + Window.getScrollTop()
                    if (
                        (x + offsetWidth + VTooltip_this._MARGIN) - Window.getScrollLeft() > Window.getClientWidth()
                    ):
                        x = Window.getClientWidth() - offsetWidth - VTooltip_this._MARGIN
                    if (
                        (y + offsetHeight + VTooltip_this._MARGIN) - Window.getScrollTop() > Window.getClientHeight()
                    ):
                        y = VTooltip_this._tooltipEventMouseY - 5 - offsetHeight
                        if y - Window.getScrollTop() < 0:
                            # tooltip does not fit on top of the mouse either,
                            # put it at the top of the screen
                            y = Window.getScrollTop()
                    self.setPopupPosition(x, y)
                    self.sinkEvents(Event.ONMOUSEOVER | Event.ONMOUSEOUT)

            _0_ = _0_()
            self.setPopupPositionAndShow(_0_)
        else:
            self.hide()

    def showTooltip(self, owner, event, key):
        if self._closing and self._tooltipOwner == owner and self._tooltipKey == key:
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
            info = VTooltip_this._ac.getTooltipTitleInfo(VTooltip_this._tooltipOwner, VTooltip_this._tooltipKey)
            if None is not info:
                VTooltip_this.show(info)
            VTooltip_this._opening = False

    class closeTimer(Timer):

        def run(self):
            VTooltip_this.closeNow()
            VTooltip_this.justClosedTimer.schedule(2000)
            VTooltip_this._justClosed = True

    class justClosedTimer(Timer):

        def run(self):
            VTooltip_this._justClosed = False

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
        type = DOM.eventGetType(event)
        if VTooltip.TOOLTIP_EVENTS & type == type:
            if type == Event.ONMOUSEOVER:
                self.showTooltip(owner, event, key)
            elif type == Event.ONMOUSEMOVE:
                self.updatePosition(event)
            else:
                self.hideTooltip()
        else:
            # non-tooltip event, hide tooltip
            self.hideTooltip()

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        # cancel closing event if tooltip is mouseovered; the user might want
        # to scroll of cut&paste
        _0 = type
        _1 = False
        while True:
            if _0 == Event.ONMOUSEOVER:
                _1 = True
                self.closeTimer.cancel()
                self._closing = False
                break
            if (_1 is True) or (_0 == Event.ONMOUSEOUT):
                _1 = True
                self.hideTooltip()
                break
            if True:
                _1 = True
            break
