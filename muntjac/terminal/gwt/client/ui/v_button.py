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

from __pyjamas__ import JS

from pyjamas import DOM

from pyjamas.ui import Event, KeyboardListener

from pyjamas.ui.FocusWidget import FocusWidget

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.event_helper import EventHelper
from muntjac.terminal.gwt.client.application_connection import ApplicationConnection
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.ui.icon import Icon
from muntjac.terminal.gwt.client.event_id import IEventId


class VButton(FocusWidget, IPaintable):#, ClickHandler, FocusHandler, BlurHandler):

    CLASSNAME = 'v-button'
    _CLASSNAME_PRESSED = 'v-pressed'

    ATTR_DISABLE_ON_CLICK = 'dc'

    # mouse movement is checked before synthesizing click event on mouseout
    MOVE_THRESHOLD = 3
    mousedownX = 0
    mousedownY = 0

    def __init__(self):
        super(VButton, self)(DOM.createDiv())

        self.id = None

        self.client = None

        self.wrapper = DOM.createSpan()

        self.errorIndicatorElement = None

        self.captionElement = DOM.createSpan()

        self.icon = None

        # Helper flag to handle special-case where the button is moved from under
        # mouse while clicking it. In this case mouse leaves the button without
        # moving.
        self.clickPending = None

        self._enabled = True

        self._tabIndex = 0

        self._disableOnClick = False

        # BELOW PRIVATE MEMBERS COPY-PASTED FROM GWT CustomButton

        # If <code>true</code>, this widget is capturing with the mouse held down.
        self._isCapturing = None

        # If <code>true</code>, this widget has focus with the space bar down.
        self._isFocusing = None

        # Used to decide whether to allow clicks to propagate up to the superclass
        # or container elements.
        self._disallowNextClick = False
        self._isHovering = None

        self._focusHandlerRegistration = None
        self._blurHandlerRegistration = None

        self._clickShortcut = 0

        self.setTabIndex(0)
        self.sinkEvents(Event.ONCLICK | Event.MOUSEEVENTS | Event.FOCUSEVENTS
                | Event.KEYEVENTS)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)

        self.setStyleName(self.CLASSNAME)

        # Add a11y role "button"
#        Accessibility.setRole(self.getElement(), Accessibility.ROLE_BUTTON)
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

        self._focusHandlerRegistration = EventHelper.updateFocusHandler(self,
                client, self._focusHandlerRegistration)
        self._blurHandlerRegistration = EventHelper.updateBlurHandler(self,
                client, self._blurHandlerRegistration)

        # Save details
        self.client = client
        self.id = uidl.getId()

        # Set text
        self.setText(uidl.getStringAttribute('caption'))

        self._disableOnClick = uidl.hasAttribute(self.ATTR_DISABLE_ON_CLICK)

        # handle error
        if uidl.hasAttribute('error'):
            if self.errorIndicatorElement is None:
                self.errorIndicatorElement = DOM.createSpan()
                self.errorIndicatorElement.setClassName('v-errorindicator')
            self.wrapper.insertBefore(self.errorIndicatorElement,
                    self.captionElement)

            # Fix for IE6, IE7
            if BrowserInfo.get().isIE6() or BrowserInfo.get().isIE7():
                self.errorIndicatorElement.setInnerText(' ')

        elif self.errorIndicatorElement is not None:
            self.wrapper.removeChild(self.errorIndicatorElement)
            self.errorIndicatorElement = None

        if uidl.hasAttribute('icon'):
            if self.icon is None:
                self.icon = Icon(client)
                self.wrapper.insertBefore(self.icon.getElement(),
                        self.captionElement)
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

        if DOM.eventGetType(event) == Event.ONLOAD:
            Util.notifyParentOfSizeChange(self, True)

        # Should not act on button if disabled.
        if not self.isEnabled():
            # This can happen when events are bubbled up from non-disabled
            # children
            return

        typ = DOM.eventGetType(event)
        if typ == Event.ONCLICK:
            if self._disallowNextClick:
                event.stopPropagation()
                self._disallowNextClick = False
        elif typ == Event.ONMOUSEDOWN:
            if DOM.isOrHasChild(self.getElement(), DOM.eventGetTarget(event)):
                # This was moved from mouseover, which iOS sometimes skips.
                # We're certainly hovering at this point, and we don't actually
                # need that information before this point.
                self.setHovering(True)

            if event.getButton() == Event.BUTTON_LEFT:
                # save mouse position to detect movement before synthesizing
                # event later
                self.mousedownX = event.getClientX()
                self.mousedownY = event.getClientY()

                self._disallowNextClick = True
                self.clickPending = True
                self.setFocus(True)
                DOM.setCapture(self.getElement())
                self._isCapturing = True
                # Prevent dragging (on some browsers);
                # DOM.eventPreventDefault(event);
                if BrowserInfo.get().isIE() or BrowserInfo.get().isOpera():
                    self.addStyleName(self._CLASSNAME_PRESSED)

        elif typ == Event.ONMOUSEUP:
            if self._isCapturing:
                self._isCapturing = False
                DOM.releaseCapture(self.getElement())
                if self.isHovering() and event.getButton() == Event.BUTTON_LEFT:
                    # Click ok
                    self._disallowNextClick = False

                if BrowserInfo.get().isIE() or BrowserInfo.get().isOpera():
                    self.removeStyleName(self._CLASSNAME_PRESSED)

        elif typ == Event.ONMOUSEMOVE:
            self.clickPending = False
            if self._isCapturing:
                # Prevent dragging (on other browsers);
                DOM.eventPreventDefault(event)

        elif typ == Event.ONMOUSEOUT:
            to = event.getRelatedTarget()
            if (self.getElement().isOrHasChild(DOM.eventGetTarget(event))
                    and (to is None) or (not self.getElement().isOrHasChild(to))):
                if (self.clickPending and
                        abs(self.mousedownX - event.getClientX()) < self.MOVE_THRESHOLD
                        and abs(self.mousedownY - event.getClientY()) < self.MOVE_THRESHOLD):
                    self.onClick()
                    break

                self.clickPending = False
                if self._isCapturing:
                    pass

                self.setHovering(False)
                if BrowserInfo.get().isIE() or BrowserInfo.get().isOpera():
                    self.removeStyleName(self._CLASSNAME_PRESSED)

        elif typ == Event.ONBLUR:
            if self._isFocusing:
                self._isFocusing = False

        elif typ == Event.ONLOSECAPTURE:
            if self._isCapturing:
                self._isCapturing = False


        super(VButton, self).onBrowserEvent(event)

        # Synthesize clicks based on keyboard events AFTER the normal key
        # handling.
        if event.getTypeInt() & Event.KEYEVENTS != 0:
            if typ == Event.ONKEYDOWN:
                if event.getKeyCode() == 32:
                    self._isFocusing = True
                    event.preventDefault()

            elif typ == Event.ONKEYUP:
                if self._isFocusing and event.getKeyCode() == 32:
                    self._isFocusing = False
                    # If click shortcut is space then the shortcut handler will
                    # take care of the click.

                    if self._clickShortcut != 32:
                        self.onClick()
                    event.preventDefault()

            elif typ == Event.ONKEYPRESS:
                if event.getKeyCode() == KeyboardListener.KEY_ENTER:
                    # If click shortcut is enter then the shortcut handler will
                    # take care of the click.

                    if self._clickShortcut != KeyboardListener.KEY_ENTER:
                        self.onClick()
                    event.preventDefault()


    def setHovering(self, hovering):
        if hovering != self.isHovering():
            self._isHovering = hovering


    def isHovering(self):
        return self._isHovering

    # ALL BELOW COPY-PASTED FROM GWT CustomButton

    def onClick(self, event=None):
        """Called internally when the user finishes clicking on this button.
        The default behavior is to fire the click event to listeners.
        Subclasses that override L{onClickStart} should override this method
        to restore the normal widget display.

        To add custom code for a click event, override L{onClick} instead of
        this.
        """
        if event is None:
            # Allow the click we're about to synthesize to pass through to
            # the superclass and containing elements. Element.dispatchEvent()
            # is synchronous, so we simply set and clear the flag within this
            # method.

            self._disallowNextClick = False
            # Mouse coordinates are not always available (e.g., when the click
            # is caused by a keyboard event).
            evt = DOM.createClickEvent(1, 0, 0, 0, 0, False, False,
                    False, False)

            self.getElement().dispatchEvent(evt)
        else:
            if (self.id is None) or (self.client is None):
                return
            if BrowserInfo.get().isSafari():
                self.setFocus(True)

            if self._disableOnClick:
                self.setEnabled(False)
                self.client.updateVariable(self.id, 'disabledOnClick', True,
                        False)

            self.client.updateVariable(self.id, 'state', True, False)

            # Add mouse details
            details = MouseEventDetails(event.getNativeEvent(),
                    self.getElement())
            self.client.updateVariable(self.id, 'mousedetails',
                    details.serialize(), True)

            self.clickPending = False


    def setEnabled(self, enabled):
        """Sets whether this button is enabled.

        @param enabled:
                   True to enable the button, False to disable it
        """
        if self.isEnabled() != enabled:
            self._enabled = enabled
            if not enabled:
                self.cleanupCaptureState()
#                Accessibility.removeState(self.getElement(),
#                        Accessibility.STATE_PRESSED)
                super(VButton, self).setTabIndex(-1)
                self.addStyleName(ApplicationConnection.DISABLED_CLASSNAME)
            else:
#                Accessibility.setState(self.getElement(),
#                        Accessibility.STATE_PRESSED, 'false')
                super(VButton, self).setTabIndex(self._tabIndex)
                self.removeStyleName(ApplicationConnection.DISABLED_CLASSNAME)


    def isEnabled(self):
        return self._enabled


    def setTabIndex(self, index):
        super(VButton, self).setTabIndex(index)
        self._tabIndex = index


    def cleanupCaptureState(self):
        """Resets internal state if this button can no longer service events.
        This can occur when the widget becomes detached or disabled.
        """
        if self._isCapturing or self._isFocusing:
            DOM.releaseCapture(self.getElement())
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
        JS("""
            // THIS METHOD IS ONLY USED FOR INTERNET EXPLORER, IT DOESN'T WORK WITH OTHERS

        	var convertToPixel = function(@{{elem}}, value) {
        	    // From the awesome hack by Dean Edwards
                // http://erik.eae.net/archives/2007/07/27/18.54.15/#comment-102291

                // Remember the original values
                var left = @{{elem}}.style.left, rsLeft = @{{elem}}.runtimeStyle.left;

                // Put in the new values to get a computed value out
                @{{elem}}.runtimeStyle.left = @{{elem}}.currentStyle.left;
                @{{elem}}.style.left = value || 0;
                var ret = @{{elem}}.style.pixelLeft;

                // Revert the changed values
                @{{elem}}.style.left = left;
                @{{elem}}.runtimeStyle.left = rsLeft;

                return ret;
        	}

         	var ret = 0;

            var sides = ["Right","Left"];
            for(var i=0; i<2; i++) {
                var side = sides[i];
                var value;
                // Border -------------------------------------------------------
                if(@{{elem}}.currentStyle["border"+side+"Style"] != "none") {
                    value = @{{elem}}.currentStyle["border"+side+"Width"];
                    if ( !/^\d+(px)?$/i.test( value ) && /^\d/.test( value ) ) {
                        ret += convertToPixel(@{{elem}}, value);
                    } else if(value.length > 2) {
                        ret += parseInt(value.substr(0, value.length-2));
                    }
                }

                // Padding -------------------------------------------------------
                value = @{{elem}}.currentStyle["padding"+side];
                if ( !/^\d+(px)?$/i.test( value ) && /^\d/.test( value ) ) {
                    ret += convertToPixel(@{{elem}}, value);
                } else if(value.length > 2) {
                    ret += parseInt(value.substr(0, value.length-2));
                }
            }

        	return ret;
        """)
        pass


    def onFocus(self, arg0):
        self.client.updateVariable(self.id, IEventId.FOCUS, '', True)


    def onBlur(self, arg0):
        self.client.updateVariable(self.id, IEventId.BLUR, '', True)
