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

from pyjamas.ui import Event
from pyjamas.ui import KeyboardListener

from pyjamas.Timer import Timer
from pyjamas.ui.TextBoxBase import TextBoxBase

from muntjac.terminal.gwt.client.ui.shortcut_action_handler \
    import IBeforeShortcutActionListener

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.event_id import IEventId
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.ui.field import IField
from muntjac.terminal.gwt.client.browser_info import BrowserInfo


class VTextField(TextBoxBase, IPaintable, IField,
            IBeforeShortcutActionListener):
#            KeyDownHandler, ChangeHandler, FocusHandler, BlurHandler):
    """This class represents a basic text input field with one row.

    @author: IT Mill Ltd.
    @author: Richard Lincoln
    """

    VAR_CUR_TEXT = 'curText'

    ATTR_NO_VALUE_CHANGE_BETWEEN_PAINTS = 'nvc'

    # The input node CSS classname.
    CLASSNAME = 'v-textfield'

    # This CSS classname is added to the input node on hover.
    CLASSNAME_FOCUS = 'focus'

    _CLASSNAME_PROMPT = 'prompt'
    _ATTR_INPUTPROMPT = 'prompt'
    ATTR_TEXTCHANGE_TIMEOUT = 'iet'
    VAR_CURSOR = 'c'
    ATTR_TEXTCHANGE_EVENTMODE = 'iem'
    _TEXTCHANGE_MODE_EAGER = 'EAGER'
    _TEXTCHANGE_MODE_TIMEOUT = 'TIMEOUT'

    def __init__(self, node=None):

        self.id = None
        self.client = None
        self._valueBeforeEdit = None
        self._immediate = False
        self._extraHorizontalPixels = -1
        self._extraVerticalPixels = -1
        self._maxLength = -1
        self._inputPrompt = None
        self._prompting = False
        self._lastCursorPos = -1
        self._wordwrap = True

        self._lastTextChangeString = None

        self.textChangeEventTrigger = TextChangeEventTrigger()

        self._scheduled = False
        self._listenTextChangeEvents = None
        self._textChangeEventMode = None
        self._textChangeEventTimeout = None

        if node is None:
            node = DOM.createInputText()

        super(VTextField, self)(node)
        if (BrowserInfo.get().getIEVersion() > 0
                and BrowserInfo.get().getIEVersion() < 8):
            # Fixes IE margin problem (#2058)
            DOM.setStyleAttribute(node, 'marginTop', '-1px')
            DOM.setStyleAttribute(node, 'marginBottom', '-1px')

        self.setStyleName(self.CLASSNAME)
        self.addChangeHandler(self)

        if BrowserInfo.get().isIE():
            # IE does not send change events when pressing enter in a text
            # input so we handle it using a key listener instead
            self.addKeyDownHandler(self)

        self.addFocusHandler(self)
        self.addBlurHandler(self)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)


    # TODO When GWT adds ONCUT, add it there and remove workaround. See
    # http://code.google.com/p/google-web-toolkit/issues/detail?id=4030
    #
    # Also note that the cut/paste are not totally crossbrowsers compatible.
    # E.g. in Opera mac works via context menu, but on via File->Paste/Cut.
    # Opera might need the polling method for 100% working textchanceevents.
    # Eager polling for a change is bit dum and heavy operation, so I guess we
    # should first try to survive without.
    _TEXTCHANGE_EVENTS = Event.ONPASTE | Event.KEYEVENTS | Event.ONMOUSEUP


    def onBrowserEvent(self, event):
        # TODO: optimize this so that only changes are sent + make the value
        # change event just a flag that moves the current text to value
        super(VTextField, self).onBrowserEvent(event)

        if self.client is not None:
            self.client.handleTooltipEvent(event, self)
        if (self._listenTextChangeEvents and event.getTypeInt()
                & self._TEXTCHANGE_EVENTS == event.getTypeInt()):
            self.deferTextChangeEvent()


    def getLastCommunicatedString(self):
        return self._lastTextChangeString


    def communicateTextValueToServer(self):
        text = self.getText()
        if self._prompting:
            # Input prompt visible, text is actually ""
            text = ''

        if not (text == self.getLastCommunicatedString()):
            self._lastTextChangeString = text
            self.client.updateVariable(self.id, self.VAR_CUR_TEXT, text, True)
            return True

        return False


    def deferTextChangeEvent(self):
        if (self._textChangeEventMode == self._TEXTCHANGE_MODE_TIMEOUT
                and self._scheduled):
            return
        else:
            self.textChangeEventTrigger.cancel()

        self.textChangeEventTrigger.schedule(self.getTextChangeEventTimeout())
        self._scheduled = True


    def getTextChangeEventTimeout(self):
        return self._textChangeEventTimeout


    def setReadOnly(self, readOnly):
        wasReadOnly = self.isReadOnly()

        if readOnly:
            self.setTabIndex(-1)
        elif wasReadOnly and not readOnly and self.getTabIndex() == -1:
            # Need to manually set tab index to 0 since server will not send
            # the tab index if it is 0.
            self.setTabIndex(0)

        super(VTextField, self).setReadOnly(readOnly)


    def updateFromUIDL(self, uidl, client):
        self.client = client
        self.id = uidl.getId()

        if client.updateComponent(self, uidl, True):
            return

        if uidl.getBooleanAttribute('readonly'):
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)

        self._inputPrompt = uidl.getStringAttribute(self._ATTR_INPUTPROMPT)

        self.setMaxLength(uidl.getIntAttribute('maxLength') if uidl.hasAttribute('maxLength') else -1)

        self._immediate = uidl.getBooleanAttribute('immediate')

        self._listenTextChangeEvents = client.hasEventListeners(self, 'ie')
        if self._listenTextChangeEvents:
            self._textChangeEventMode = uidl.getStringAttribute(
                    self.ATTR_TEXTCHANGE_EVENTMODE)
            if self._textChangeEventMode == self._TEXTCHANGE_MODE_EAGER:
                self._textChangeEventTimeout = 1
            else:
                self._textChangeEventTimeout = uidl.getIntAttribute(
                        self.ATTR_TEXTCHANGE_TIMEOUT)

                if self._textChangeEventTimeout < 1:
                    # Sanitize and allow lazy/timeout with timeout set to 0 to
                    # work as eager
                    self._textChangeEventTimeout = 1

            self.sinkEvents(self._TEXTCHANGE_EVENTS)
            self.attachCutEventListener(self.getElement())

        if uidl.hasAttribute('cols'):
            self.setColumns(int(uidl.getStringAttribute('cols')))

        text = uidl.getStringVariable('text')

        # We skip the text content update if field has been repainted, but text
        # has not been changed. Additional sanity check verifies there is no
        # change in the que (in which case we count more on the server side
        # value).
        if (not (uidl.getBooleanAttribute(
                self.ATTR_NO_VALUE_CHANGE_BETWEEN_PAINTS)
                and self._valueBeforeEdit is not None
                and text == self._valueBeforeEdit)):
            self.updateFieldContent(text)

        if uidl.hasAttribute('selpos'):
            pos = uidl.getIntAttribute('selpos')
            length = uidl.getIntAttribute('sellen')
            # Gecko defers setting the text so we need to defer the selection.

            class _1_(Command):

                def execute(self):
                    self.setSelectionRange(self.pos, self.length)

            _1_ = _1_()
            Scheduler.get().scheduleDeferred(_1_)

        # Here for backward compatibility; to be moved to TextArea.
        # Optimization: server does not send attribute for the default 'true'
        # state.
        if (uidl.hasAttribute('wordwrap')
                and uidl.getBooleanAttribute('wordwrap') == False):
            self.setWordwrap(False)
        else:
            self.setWordwrap(True)


    def updateFieldContent(self, text):
        self.setPrompting(self._inputPrompt is not None
                and self._focusedTextField is not self and text == '')

        if BrowserInfo.get().isFF3():
            # Firefox 3 is really sluggish when updating input attached to dom.
            # Some optimizations seems to work much better in Firefox3 if we
            # update the actual content lazily when the rest of the DOM has
            # stabilized. In tests, about ten times better performance is
            # achieved with this optimization. See for eg. #2898

            class _2_(Command):

                def execute(self):
                    if VTextField_this._prompting:
                        fieldValue = '' if self.isReadOnly() else VTextField_this._inputPrompt
                        self.addStyleDependentName(VTextField_this._CLASSNAME_PROMPT)
                    else:
                        fieldValue = self.text
                        self.removeStyleDependentName(VTextField_this._CLASSNAME_PROMPT)
                    # Avoid resetting the old value. Prevents cursor flickering
                    # which then again happens due to this Gecko hack.

                    if not (self.getText() == fieldValue):
                        self.setText(fieldValue)

            _2_ = _2_()
            Scheduler.get().scheduleDeferred(_2_)
        else:
            if self._prompting:
                fieldValue = '' if self.isReadOnly() else self._inputPrompt
                self.addStyleDependentName(self._CLASSNAME_PROMPT)
            else:
                fieldValue = text
                self.removeStyleDependentName(self._CLASSNAME_PROMPT)
            self.setText(fieldValue)

        self._lastTextChangeString = self._valueBeforeEdit = text


    def onCut(self):
        if self._listenTextChangeEvents:
            self.deferTextChangeEvent()


    def attachCutEventListener(self, el):
        JS("""
            var me = @{{self}};
            @{{el}}.oncut = function() {
                me.@com.vaadin.terminal.gwt.client.ui.VTextField::onCut()();
            };
        """)
        pass


    def detachCutEventListener(self, el):
        JS("""
            @{{el}}.oncut = null;
        """)
        pass


    def onDetach(self):
        super(VTextField, self).onDetach()
        self.detachCutEventListener(self.getElement())
        if self._focusedTextField is self:
            self._focusedTextField = None


    def onAttach(self):
        super(VTextField, self).onAttach()
        if self._listenTextChangeEvents:
            self.detachCutEventListener(self.getElement())


    def setMaxLength(self, newMaxLength):
        if newMaxLength >= 0:
            self._maxLength = newMaxLength
            if self.getElement().getTagName().toLowerCase() == 'textarea':
                # NOP no maxlength property for textarea
                pass
            else:
                self.getElement().setPropertyInt('maxLength', self._maxLength)
        elif self._maxLength != -1:
            if self.getElement().getTagName().toLowerCase() == 'textarea':
                # NOP no maxlength property for textarea
                pass
            else:
                self.getElement().removeAttribute('maxLength')
            self._maxLength = -1


    def getMaxLength(self):
        return self._maxLength


    def onChange(self, event):
        self.valueChange(False)


    def valueChange(self, blurred):
        """Called when the field value might have changed and/or the field was
        blurred. These are combined so the blur event is sent in the same batch
        as a possible value change event (these are often connected).

        @param blurred:
                   true if the field was blurred
        """
        if self.client is not None and self.id is not None:
            sendBlurEvent = False
            sendValueChange = False
            if blurred and self.client.hasEventListeners(self, IEventId.BLUR):
                sendBlurEvent = True
                self.client.updateVariable(self.id, IEventId.BLUR, '', False)
            newText = self.getText()
            if (not self._prompting and newText is not None
                    and not (newText == self._valueBeforeEdit)):
                sendValueChange = self._immediate
                self.client.updateVariable(self.id, 'text', self.getText(),
                        False)
                self._valueBeforeEdit = newText

            # also send cursor position, no public api yet but for easier
            # extension
            self.updateCursorPosition()

            if sendBlurEvent or sendValueChange:
                # Avoid sending text change event as we will simulate it on the
                # server side before value change events.
                self.textChangeEventTrigger.cancel()
                self._scheduled = False
                self.client.sendPendingVariableChanges()


    def updateCursorPosition(self):
        """Updates the cursor position variable if it has changed since the
        last update.

        @return: true iff the value was updated
        """
        if Util.isAttachedAndDisplayed(self):
            cursorPos = self.getCursorPos()
            if self._lastCursorPos != cursorPos:
                self.client.updateVariable(self.id, self.VAR_CURSOR,
                        cursorPos, False)
                self._lastCursorPos = cursorPos
                return True
        return False

    _focusedTextField = None

    @classmethod
    def flushChangesFromFocusedTextField(cls):
        if cls._focusedTextField is not None:
            cls._focusedTextField.onChange(None)


    def onFocus(self, event):
        self.addStyleDependentName(self.CLASSNAME_FOCUS)
        if self._prompting:
            self.setText('')
            self.removeStyleDependentName(self._CLASSNAME_PROMPT)
            self.setPrompting(False)
            if BrowserInfo.get().isIE6():
                # IE6 does not show the cursor when tabbing into the field
                self.setCursorPos(0)
        self._focusedTextField = self
        if self.client.hasEventListeners(self, IEventId.FOCUS):
            self.client.updateVariable(self.client.getPid(self),
                    IEventId.FOCUS, '', True)


    def onBlur(self, event):
        self.removeStyleDependentName(self.CLASSNAME_FOCUS)
        self._focusedTextField = None
        text = self.getText()
        self.setPrompting(self._inputPrompt is not None and (text is None)
                or ('' == text))
        if self._prompting:
            self.setText('' if self.isReadOnly() else self._inputPrompt)
            self.addStyleDependentName(self._CLASSNAME_PROMPT)
        self.valueChange(True)


    def setPrompting(self, prompting):
        self._prompting = prompting


    def setColumns(self, columns_or_e, c=None):
        if c is None:
            columns = columns_or_e
            self.setColumns(self.getElement(), columns)
        else:
            e = columns_or_e
            JS("""
                try {
                	switch(e.tagName.toLowerCase()) {
                		case "input":
                			//e.size = c;
                			e.style.width = c+"em";
                			break;
                		case "textarea":
                			//e.cols = c;
                			e.style.width = c+"em";
                			break;
                		default:;
                	}
                } catch (e) {}
            """)


    def getExtraHorizontalPixels(self):
        """@return: space used by components paddings and borders"""
        if self._extraHorizontalPixels < 0:
            self.detectExtraSizes()
        return self._extraHorizontalPixels


    def getExtraVerticalPixels(self):
        """@return: space used by components paddings and borders"""
        if self._extraVerticalPixels < 0:
            self.detectExtraSizes()
        return self._extraVerticalPixels


    def detectExtraSizes(self):
        """Detects space used by components paddings and borders. Used when
        relational size are used.
        """
        clone = Util.cloneNode(self.getElement(), False)
        DOM.setElemAttribute(clone, 'id', '')
        DOM.setStyleAttribute(clone, 'visibility', 'hidden')
        DOM.setStyleAttribute(clone, 'position', 'absolute')
        # due FF3 bug set size to 10px and later subtract it from extra pixels
        DOM.setStyleAttribute(clone, 'width', '10px')
        DOM.setStyleAttribute(clone, 'height', '10px')
        DOM.appendChild(DOM.getParent(self.getElement()), clone)
        self._extraHorizontalPixels = DOM.getIntElemAttribute(clone,
                'offsetWidth') - 10
        self._extraVerticalPixels = DOM.getIntElemAttribute(clone,
                'offsetHeight') - 10
        DOM.removeChild(DOM.getParent(self.getElement()), clone)


    def setHeight(self, height):
        if height.endswith('px'):
            h = int(height[:-2])
            h -= self.getExtraVerticalPixels()
            if h < 0:
                h = 0
            super(VTextField, self).setHeight(h + 'px')
        else:
            super(VTextField, self).setHeight(height)


    def setWidth(self, width):
        if width.endswith('px'):
            w = int(width[:-2])
            w -= self.getExtraHorizontalPixels()
            if w < 0:
                w = 0
            super(VTextField, self).setWidth(w + 'px')
        else:
            super(VTextField, self).setWidth(width)


    def onBeforeShortcutAction(self, e):
        # Here for backward compatibility; to be moved to TextArea
        self.valueChange(False)


    def setWordwrap(self, enabled):
        if enabled == self._wordwrap:
            return  # No change

        if enabled:
            self.getElement().removeAttribute('wrap')
            self.getElement().getStyle().clearOverflow()
        else:
            self.getElement().setAttribute('wrap', 'off')
            self.getElement().getStyle().setOverflow('auto')#Overflow.AUTO)

        if BrowserInfo.get().isSafari4():
            # Force redraw as Safari 4 does not properly update the screen
            Util.forceWebkitRedraw(self.getElement())
        elif BrowserInfo.get().isOpera():
            # Opera fails to dynamically update the wrap attribute so we detach
            # and reattach the whole TextArea.
            Util.detachAttach(self.getElement())

        self._wordwrap = enabled


    def onKeyDown(self, event):
        if event.getNativeKeyCode() == KeyboardListener.KEY_ENTER:
            self.valueChange(False)


class TextChangeEventTrigger(Timer):

    def __init__(self, tf):
        self._tf = tf

    def run(self):
        if self.isAttached():
            self._tf.updateCursorPosition()
            textChanged = self._tf.communicateTextValueToServer()
            if textChanged:
                self._tf.client.sendPendingVariableChanges()
            self._tf._scheduled = False
