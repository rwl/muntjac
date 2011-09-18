# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
from com.vaadin.terminal.gwt.client.EventHelper import (EventHelper,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
# from com.google.gwt.event.dom.client.KeyCodes import (KeyCodes,)
# from com.google.gwt.user.client.ui.Accessibility import (Accessibility,)
# from com.google.gwt.user.client.ui.FocusWidget import (FocusWidget,)


class VButton(FocusWidget, Paintable, ClickHandler, FocusHandler, BlurHandler):
    CLASSNAME = 'v-button'
    _CLASSNAME_PRESSED = 'v-pressed'
    # mouse movement is checked before synthesizing click event on mouseout
    MOVE_THRESHOLD = 3
    mousedownX = 0
    mousedownY = 0
    id = None
    client = None
    wrapper = DOM.createSpan()
    errorIndicatorElement = None
    captionElement = DOM.createSpan()
    icon = None
    # Helper flag to handle special-case where the button is moved from under
    # mouse while clicking it. In this case mouse leaves the button without
    # moving.

    clickPending = None
    _enabled = True
    _tabIndex = 0
    # BELOW PRIVATE MEMBERS COPY-PASTED FROM GWT CustomButton
    # If <code>true</code>, this widget is capturing with the mouse held down.
    _isCapturing = None
    # If <code>true</code>, this widget has focus with the space bar down.
    _isFocusing = None
    # Used to decide whether to allow clicks to propagate up to the superclass
    # or container elements.

    _disallowNextClick = False
    _isHovering = None
    _focusHandlerRegistration = None
    _blurHandlerRegistration = None
    _clickShortcut = 0

    def __init__(self):
        super(VButton, self)(self.DOM.createDiv())
        self.setTabIndex(0)
        self.sinkEvents(((self.Event.ONCLICK | self.Event.MOUSEEVENTS) | self.Event.FOCUSEVENTS) | self.Event.KEYEVENTS)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        self.setStyleName(self.CLASSNAME)
        # Add a11y role "button"
        Accessibility.setRole(self.getElement(), Accessibility.ROLE_BUTTON)
        self.wrapper.setClassName(self.getStylePrimaryName() + '-wrap')
        self.getElement().appendChild(self.wrapper)
        self.captionElement.setClassName(self.getStylePrimaryName() + '-caption')
        self.wrapper.appendChild(self.captionElement)
        self.addClickHandler(self)

    def updateFromUIDL(self, uidl, client):
        # Ensure correct implementation,
        # but don't let container manage caption etc.
        if client.updateComponent(self, uidl, False):
            return
        self._focusHandlerRegistration = EventHelper.updateFocusHandler(self, client, self._focusHandlerRegistration)
        self._blurHandlerRegistration = EventHelper.updateBlurHandler(self, client, self._blurHandlerRegistration)
        # Save details
        self.client = client
        self.id = uidl.getId()
        # Set text
        self.setText(uidl.getStringAttribute('caption'))
        # handle error
        if uidl.hasAttribute('error'):
            if self.errorIndicatorElement is None:
                self.errorIndicatorElement = self.DOM.createSpan()
                self.errorIndicatorElement.setClassName('v-errorindicator')
            self.wrapper.insertBefore(self.errorIndicatorElement, self.captionElement)
            # Fix for IE6, IE7
            if BrowserInfo.get().isIE6() or BrowserInfo.get().isIE7():
                self.errorIndicatorElement.setInnerText(' ')
        elif self.errorIndicatorElement is not None:
            self.wrapper.removeChild(self.errorIndicatorElement)
            self.errorIndicatorElement = None
        if uidl.hasAttribute('icon'):
            if self.icon is None:
                self.icon = Icon(client)
                self.wrapper.insertBefore(self.icon.getElement(), self.captionElement)
            self.icon.setUri(uidl.getStringAttribute('icon'))
        elif self.icon is not None:
            self.wrapper.removeChild(self.icon.getElement())
            self.icon = None
        if uidl.hasAttribute('keycode'):
            self._clickShortcut = uidl.getIntAttribute('keycode')

    def setText(self, text):
        self.captionElement.setInnerText(text)

    def onBrowserEvent(self, event):
        # Copy-pasted from GWT CustomButton, some minor modifications done:
        # 
        # -for IE/Opera added CLASSNAME_PRESSED
        # 
        # -event.preventDefault() commented from ONMOUSEDOWN (Firefox won't apply
        # :active styles if it is present)
        # 
        # -Tooltip event handling added
        # 
        # -onload event handler added (for icon handling)

        if self.client is not None:
            self.client.handleTooltipEvent(event, self)
        if self.DOM.eventGetType(event) == self.Event.ONLOAD:
            Util.notifyParentOfSizeChange(self, True)
        # Should not act on button if disabled.
        if not self.isEnabled():
            # This can happen when events are bubbled up from non-disabled
            # children
            return
        type = self.DOM.eventGetType(event)
        _0 = type
        _1 = False
        while True:
            if _0 == self.Event.ONCLICK:
                _1 = True
                if self._disallowNextClick:
                    event.stopPropagation()
                    self._disallowNextClick = False
                    return
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEDOWN):
                _1 = True
                if self.DOM.isOrHasChild(self.getElement(), self.DOM.eventGetTarget(event)):
                    # This was moved from mouseover, which iOS sometimes skips.
                    # We're certainly hovering at this point, and we don't actually
                    # need that information before this point.
                    self.setHovering(True)
                if event.getButton() == self.Event.BUTTON_LEFT:
                    # save mouse position to detect movement before synthesizing
                    # event later
                    self.mousedownX = event.getClientX()
                    self.mousedownY = event.getClientY()
                    self._disallowNextClick = True
                    self.clickPending = True
                    self.setFocus(True)
                    self.DOM.setCapture(self.getElement())
                    self._isCapturing = True
                    # Prevent dragging (on some browsers);
                    # DOM.eventPreventDefault(event);
                    if BrowserInfo.get().isIE() or BrowserInfo.get().isOpera():
                        self.addStyleName(self._CLASSNAME_PRESSED)
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEUP):
                _1 = True
                if self._isCapturing:
                    self._isCapturing = False
                    self.DOM.releaseCapture(self.getElement())
                    if self._isHovering() and event.getButton() == self.Event.BUTTON_LEFT:
                        # Click ok
                        self._disallowNextClick = False
                    if BrowserInfo.get().isIE() or BrowserInfo.get().isOpera():
                        self.removeStyleName(self._CLASSNAME_PRESSED)
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEMOVE):
                _1 = True
                self.clickPending = False
                if self._isCapturing:
                    # Prevent dragging (on other browsers);
                    self.DOM.eventPreventDefault(event)
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEOUT):
                _1 = True
                to = event.getRelatedTarget()
                if (
                    self.getElement().isOrHasChild(self.DOM.eventGetTarget(event)) and (to is None) or (not self.getElement().isOrHasChild(to))
                ):
                    if (
                        self.clickPending and self.Math.abs(self.mousedownX - event.getClientX()) < self.MOVE_THRESHOLD and self.Math.abs(self.mousedownY - event.getClientY()) < self.MOVE_THRESHOLD
                    ):
                        self.onClick()
                        break
                    self.clickPending = False
                    if self._isCapturing:
                        pass
                    self.setHovering(False)
                    if BrowserInfo.get().isIE() or BrowserInfo.get().isOpera():
                        self.removeStyleName(self._CLASSNAME_PRESSED)
                break
            if (_1 is True) or (_0 == self.Event.ONBLUR):
                _1 = True
                if self._isFocusing:
                    self._isFocusing = False
                break
            if (_1 is True) or (_0 == self.Event.ONLOSECAPTURE):
                _1 = True
                if self._isCapturing:
                    self._isCapturing = False
                break
            break
        super(VButton, self).onBrowserEvent(event)
        # Synthesize clicks based on keyboard events AFTER the normal key
        # handling.
        if event.getTypeInt() & self.Event.KEYEVENTS != 0:
            _2 = type
            _3 = False
            while True:
                if _2 == self.Event.ONKEYDOWN:
                    _3 = True
                    if event.getKeyCode() == 32:
                        self._isFocusing = True
                        event.preventDefault()
                    break
                if (_3 is True) or (_2 == self.Event.ONKEYUP):
                    _3 = True
                    if self._isFocusing and event.getKeyCode() == 32:
                        self._isFocusing = False
                        # If click shortcut is space then the shortcut handler will
                        # take care of the click.

                        if self._clickShortcut != 32:
                            self.onClick()
                        event.preventDefault()
                    break
                if (_3 is True) or (_2 == self.Event.ONKEYPRESS):
                    _3 = True
                    if event.getKeyCode() == KeyCodes.KEY_ENTER:
                        # If click shortcut is enter then the shortcut handler will
                        # take care of the click.

                        if self._clickShortcut != KeyCodes.KEY_ENTER:
                            self.onClick()
                        event.preventDefault()
                    break
                break

    def setHovering(self, hovering):
        if hovering != self._isHovering():
            self._isHovering = hovering

    def isHovering(self):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.ClickHandler#onClick(com.google.gwt.event
        # .dom.client.ClickEvent)

        return self._isHovering

    def onClick(self, *args):
        """None
        ---
        Called internally when the user finishes clicking on this button. The
        default behavior is to fire the click event to listeners. Subclasses that
        override {@link #onClickStart()} should override this method to restore
        the normal widget display.
        <p>
        To add custom code for a click event, override
        {@link #onClick(ClickEvent)} instead of this.
        """
        # ALL BELOW COPY-PASTED FROM GWT CustomButton
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self._disallowNextClick = False
            # Mouse coordinates are not always available (e.g., when the click is
            # caused by a keyboard event).
            evt = self.Document.get().createClickEvent(1, 0, 0, 0, 0, False, False, False, False)
            self.getElement().dispatchEvent(evt)
        elif _1 == 1:
            event, = _0
            if (self.id is None) or (self.client is None):
                return
            if BrowserInfo.get().isSafari():
                _VButton_this.setFocus(True)
            self.client.updateVariable(self.id, 'state', True, False)
            # Add mouse details
            details = MouseEventDetails(event.getNativeEvent(), self.getElement())
            self.client.updateVariable(self.id, 'mousedetails', details.serialize(), True)
            self.clickPending = False
        else:
            raise ARGERROR(0, 1)

    # Allow the click we're about to synthesize to pass through to the
    # superclass and containing elements. Element.dispatchEvent() is
    # synchronous, so we simply set and clear the flag within this method.

    def setEnabled(self, enabled):
        """Sets whether this button is enabled.

        @param enabled
                   <code>true</code> to enable the button, <code>false</code> to
                   disable it
        """
        if self.isEnabled() != enabled:
            self._enabled = enabled
            if not enabled:
                self.cleanupCaptureState()
                Accessibility.removeState(self.getElement(), Accessibility.STATE_PRESSED)
                super(VButton, self).setTabIndex(-1)
                self.addStyleName('v-disabled')
            else:
                Accessibility.setState(self.getElement(), Accessibility.STATE_PRESSED, 'false')
                super(VButton, self).setTabIndex(self._tabIndex)
                self.removeStyleName('v-disabled')

    def isEnabled(self):
        return self._enabled

    def setTabIndex(self, index):
        super(VButton, self).setTabIndex(index)
        self._tabIndex = index

    def cleanupCaptureState(self):
        """Resets internal state if this button can no longer service events. This
        can occur when the widget becomes detached or disabled.
        """
        if self._isCapturing or self._isFocusing:
            self.DOM.releaseCapture(self.getElement())
            self._isCapturing = False
            self._isFocusing = False

    def setWidth(self, width):
        if BrowserInfo.get().isIE6() or BrowserInfo.get().isIE7():
            if width is not None and len(width) > 2:
                # Assume pixel values are always sent from
                # ApplicationConnection
                w = int(width[:-2])
                w -= self.getHorizontalBorderAndPaddingWidth(self.getElement())
                if w < 0:
                    # validity check for IE
                    w = 0
                width = w + 'px'
        super(VButton, self).setWidth(width)

    @classmethod
    def getHorizontalBorderAndPaddingWidth(cls, elem):
        # -{
        #         // THIS METHOD IS ONLY USED FOR INTERNET EXPLORER, IT DOESN'T WORK WITH OTHERS
        # 
        #     	var convertToPixel = function(elem, value) {
        #     	    // From the awesome hack by Dean Edwards
        #             // http://erik.eae.net/archives/2007/07/27/18.54.15/#comment-102291
        # 
        #             // Remember the original values
        #             var left = elem.style.left, rsLeft = elem.runtimeStyle.left;
        # 
        #             // Put in the new values to get a computed value out
        #             elem.runtimeStyle.left = elem.currentStyle.left;
        #             elem.style.left = value || 0;
        #             var ret = elem.style.pixelLeft;
        # 
        #             // Revert the changed values
        #             elem.style.left = left;
        #             elem.runtimeStyle.left = rsLeft;
        # 
        #             return ret;
        #     	}
        # 
        #      	var ret = 0;
        # 
        #         var sides = ["Right","Left"];
        #         for(var i=0; i<2; i++) {
        #             var side = sides[i];
        #             var value;
        #             // Border -------------------------------------------------------
        #             if(elem.currentStyle["border"+side+"Style"] != "none") {
        #                 value = elem.currentStyle["border"+side+"Width"];
        #                 if ( !/^\d+(px)?$/i.test( value ) && /^\d/.test( value ) ) {
        #                     ret += convertToPixel(elem, value);
        #                 } else if(value.length > 2) {
        #                     ret += parseInt(value.substr(0, value.length-2));
        #                 }
        #             }
        # 
        #             // Padding -------------------------------------------------------
        #             value = elem.currentStyle["padding"+side];
        #             if ( !/^\d+(px)?$/i.test( value ) && /^\d/.test( value ) ) {
        #                 ret += convertToPixel(elem, value);
        #             } else if(value.length > 2) {
        #                 ret += parseInt(value.substr(0, value.length-2));
        #             }
        #         }
        # 
        #     	return ret;
        #     }-

        pass

    def onFocus(self, arg0):
        self.client.updateVariable(self.id, EventId.FOCUS, '', True)

    def onBlur(self, arg0):
        self.client.updateVariable(self.id, EventId.BLUR, '', True)
