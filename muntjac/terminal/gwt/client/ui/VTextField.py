# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.ShortcutActionHandler import (ShortcutActionHandler,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.user.client.ui.TextBoxBase import (TextBoxBase,)
BeforeShortcutActionListener = ShortcutActionHandler.BeforeShortcutActionListener


class VTextField(TextBoxBase, Paintable, Field, ChangeHandler, FocusHandler, BlurHandler, BeforeShortcutActionListener, KeyDownHandler):
    """This class represents a basic text input field with one row.

    @author IT Mill Ltd.
    """
    VAR_CUR_TEXT = 'curText'
    ATTR_NO_VALUE_CHANGE_BETWEEN_PAINTS = 'nvc'
    # The input node CSS classname.
    CLASSNAME = 'v-textfield'
    # This CSS classname is added to the input node on hover.
    CLASSNAME_FOCUS = 'focus'
    id = None
    client = None
    _valueBeforeEdit = None
    _immediate = False
    _extraHorizontalPixels = -1
    _extraVerticalPixels = -1
    _maxLength = -1
    _CLASSNAME_PROMPT = 'prompt'
    _ATTR_INPUTPROMPT = 'prompt'
    ATTR_TEXTCHANGE_TIMEOUT = 'iet'
    VAR_CURSOR = 'c'
    ATTR_TEXTCHANGE_EVENTMODE = 'iem'
    _TEXTCHANGE_MODE_EAGER = 'EAGER'
    _TEXTCHANGE_MODE_TIMEOUT = 'TIMEOUT'
    _inputPrompt = None
    _prompting = False
    _lastCursorPos = -1
    _wordwrap = True

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(DOM.createInputText())
        elif _1 == 1:
            node, = _0
            super(VTextField, self)(node)
            if (
                BrowserInfo.get().getIEVersion() > 0 and BrowserInfo.get().getIEVersion() < 8
            ):
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
        else:
            raise ARGERROR(0, 1)

    # TODO When GWT adds ONCUT, add it there and remove workaround. See
    # http://code.google.com/p/google-web-toolkit/issues/detail?id=4030
    # 
    # Also note that the cut/paste are not totally crossbrowsers compatible.
    # E.g. in Opera mac works via context menu, but on via File->Paste/Cut.
    # Opera might need the polling method for 100% working textchanceevents.
    # Eager polling for a change is bit dum and heavy operation, so I guess we
    # should first try to survive without.

    _TEXTCHANGE_EVENTS = (Event.ONPASTE | Event.KEYEVENTS) | Event.ONMOUSEUP

    def onBrowserEvent(self, event):
        # TODO optimize this so that only changes are sent + make the value change
        # event just a flag that moves the current text to value

        super(VTextField, self).onBrowserEvent(event)
        if self.client is not None:
            self.client.handleTooltipEvent(event, self)
        if (
            self._listenTextChangeEvents and event.getTypeInt() & self._TEXTCHANGE_EVENTS == event.getTypeInt()
        ):
            self.deferTextChangeEvent()

    _lastTextChangeString = None

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

    class textChangeEventTrigger(Timer):

        def run(self):
            if self.isAttached():
                VTextField_this.updateCursorPosition()
                textChanged = VTextField_this.communicateTextValueToServer()
                if textChanged:
                    VTextField_this.client.sendPendingVariableChanges()
                VTextField_this._scheduled = False

    _scheduled = False
    _listenTextChangeEvents = None
    _textChangeEventMode = None
    _textChangeEventTimeout = None

    def deferTextChangeEvent(self):
        if (
            self._textChangeEventMode == self._TEXTCHANGE_MODE_TIMEOUT and self._scheduled
        ):
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
            self._textChangeEventMode = uidl.getStringAttribute(self.ATTR_TEXTCHANGE_EVENTMODE)
            if self._textChangeEventMode == self._TEXTCHANGE_MODE_EAGER:
                self._textChangeEventTimeout = 1
            else:
                self._textChangeEventTimeout = uidl.getIntAttribute(self.ATTR_TEXTCHANGE_TIMEOUT)
                if self._textChangeEventTimeout < 1:
                    # Sanitize and allow lazy/timeout with timeout set to 0 to
                    # work as eager
                    self._textChangeEventTimeout = 1
            self.sinkEvents(self._TEXTCHANGE_EVENTS)
            self.attachCutEventListener(self.getElement())
        if uidl.hasAttribute('cols'):
            self.setColumns(int(uidl.getStringAttribute('cols')).intValue())
        text = uidl.getStringVariable('text')
        # We skip the text content update if field has been repainted, but text has
        # not been changed. Additional sanity check verifies there is no change
        # in the que (in which case we count more on the server side value).

        if (
            not (uidl.getBooleanAttribute(self.ATTR_NO_VALUE_CHANGE_BETWEEN_PAINTS) and self._valueBeforeEdit is not None and text == self._valueBeforeEdit)
        ):
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
        if (
            uidl.hasAttribute('wordwrap') and uidl.getBooleanAttribute('wordwrap') == False
        ):
            self.setWordwrap(False)
        else:
            self.setWordwrap(True)

    def updateFieldContent(self, text):
        self.setPrompting(self._inputPrompt is not None and self._focusedTextField is not self and text == '')
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

        @param blurred
                   true if the field was blurred
        """
        if self.client is not None and self.id is not None:
            sendBlurEvent = False
            sendValueChange = False
            if blurred and self.client.hasEventListeners(self, EventId.BLUR):
                sendBlurEvent = True
                self.client.updateVariable(self.id, EventId.BLUR, '', False)
            newText = self.getText()
            if (
                not self._prompting and newText is not None and not (newText == self._valueBeforeEdit)
            ):
                sendValueChange = self._immediate
                self.client.updateVariable(self.id, 'text', self.getText(), False)
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
        """Updates the cursor position variable if it has changed since the last
        update.

        @return true iff the value was updated
        """
        if Util.isAttachedAndDisplayed(self):
            cursorPos = self.getCursorPos()
            if self._lastCursorPos != cursorPos:
                self.client.updateVariable(self.id, self.VAR_CURSOR, cursorPos, False)
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
        if self.client.hasEventListeners(self, EventId.FOCUS):
            self.client.updateVariable(self.client.getPid(self), EventId.FOCUS, '', True)

    def onBlur(self, event):
        self.removeStyleDependentName(self.CLASSNAME_FOCUS)
        self._focusedTextField = None
        text = self.getText()
        self.setPrompting(self._inputPrompt is not None and (text is None) or ('' == text))
        if self._prompting:
            self.setText('' if self.isReadOnly() else self._inputPrompt)
            self.addStyleDependentName(self._CLASSNAME_PROMPT)
        self.valueChange(True)

    def setPrompting(self, prompting):
        self._prompting = prompting

    def setColumns(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            columns, = _0
            self.setColumns(self.getElement(), columns)
        elif _1 == 2:
            e, c = _0
        else:
            raise ARGERROR(1, 2)

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
        """@return space used by components paddings and borders"""
        if self._extraHorizontalPixels < 0:
            self.detectExtraSizes()
        return self._extraHorizontalPixels

    def getExtraVerticalPixels(self):
        """@return space used by components paddings and borders"""
        if self._extraVerticalPixels < 0:
            self.detectExtraSizes()
        return self._extraVerticalPixels

    def detectExtraSizes(self):
        """Detects space used by components paddings and borders. Used when
        relational size are used.
        """
        clone = Util.cloneNode(self.getElement(), False)
        DOM.setElementAttribute(clone, 'id', '')
        DOM.setStyleAttribute(clone, 'visibility', 'hidden')
        DOM.setStyleAttribute(clone, 'position', 'absolute')
        # due FF3 bug set size to 10px and later subtract it from extra pixels
        DOM.setStyleAttribute(clone, 'width', '10px')
        DOM.setStyleAttribute(clone, 'height', '10px')
        DOM.appendChild(DOM.getParent(self.getElement()), clone)
        self._extraHorizontalPixels = DOM.getElementPropertyInt(clone, 'offsetWidth') - 10
        self._extraVerticalPixels = DOM.getElementPropertyInt(clone, 'offsetHeight') - 10
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
            return
            # No change
        if enabled:
            self.getElement().removeAttribute('wrap')
            self.getElement().getStyle().clearOverflow()
        else:
            self.getElement().setAttribute('wrap', 'off')
            self.getElement().getStyle().setOverflow(Overflow.AUTO)
        if BrowserInfo.get().isSafari4():
            # Force redraw as Safari 4 does not properly update the screen
            Util.forceWebkitRedraw(self.getElement())
        elif BrowserInfo.get().isOpera():
            # Opera fails to dynamically update the wrap attribute so we detach
            # and reattach the whole TextArea.
            Util.detachAttach(self.getElement())
        self._wordwrap = enabled

    def onKeyDown(self, event):
        if event.getNativeKeyCode() == KeyCodes.KEY_ENTER:
            self.valueChange(False)
