# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VCheckBox import (VCheckBox,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ApplicationConnection import (ApplicationConnection,)
from com.vaadin.terminal.gwt.client.ui.VOptionGroupBase import (VOptionGroupBase,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
# from com.google.gwt.user.client.ui.CheckBox import (CheckBox,)
# from com.google.gwt.user.client.ui.FocusWidget import (FocusWidget,)
# from com.google.gwt.user.client.ui.Focusable import (Focusable,)
# from com.google.gwt.user.client.ui.RadioButton import (RadioButton,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.Map import (Map,)


class VOptionGroup(VOptionGroupBase, FocusHandler, BlurHandler):
    HTML_CONTENT_ALLOWED = 'usehtml'
    CLASSNAME = 'v-select-optiongroup'
    _panel = None
    _optionsToKeys = None
    _sendFocusEvents = False
    _sendBlurEvents = False
    _focusHandlers = None
    _blurHandlers = None
    # private final LoadHandler iconLoadHandler = new LoadHandler() {
    # public void onLoad(LoadEvent event) {
    # if (BrowserInfo.get().isIE6()) {
    # Util.doIE6PngFix((Element) Element.as(event.getNativeEvent()
    # .getEventTarget()));
    # }
    # Util.notifyParentOfSizeChange(VOptionGroup.this, true);
    # }
    # };
    # used to check whether a blur really was a blur of the complete
    # optiongroup: if a control inside this optiongroup gains focus right after
    # blur of another control inside this optiongroup (meaning: if onFocus
    # fires after onBlur has fired), the blur and focus won't be sent to the
    # server side as only a focus change inside this optiongroup occured

    _blurOccured = False
    _htmlContentAllowed = False

    def __init__(self):
        super(VOptionGroup, self)(self.CLASSNAME)
        self._panel = self.optionsContainer
        self._optionsToKeys = dict()

    def updateFromUIDL(self, uidl, client):
        # Return true if no elements were changed, false otherwise.
        self._htmlContentAllowed = uidl.hasAttribute(self.HTML_CONTENT_ALLOWED)
        super(VOptionGroup, self).updateFromUIDL(uidl, client)
        self._sendFocusEvents = client.hasEventListeners(self, EventId.FOCUS)
        self._sendBlurEvents = client.hasEventListeners(self, EventId.BLUR)
        if self._focusHandlers is not None:
            for reg in self._focusHandlers:
                reg.removeHandler()
            self._focusHandlers.clear()
            self._focusHandlers = None
            for reg in self._blurHandlers:
                reg.removeHandler()
            self._blurHandlers.clear()
            self._blurHandlers = None
        if self._sendFocusEvents or self._sendBlurEvents:
            self._focusHandlers = list()
            self._blurHandlers = list()
            # add focus and blur handlers to checkboxes / radio buttons
            for wid in self._panel:
                if isinstance(wid, CheckBox):
                    self._focusHandlers.add(wid.addFocusHandler(self))
                    self._blurHandlers.add(wid.addBlurHandler(self))

    def buildOptions(self, uidl):
        self._panel.clear()
        _0 = True
        it = uidl.getChildIterator()
        while True:
            if _0 is True:
                _0 = False
            if not it.hasNext():
                break
            opUidl = it.next()
            itemHtml = opUidl.getStringAttribute('caption')
            if not self._htmlContentAllowed:
                itemHtml = Util.escapeHTML(itemHtml)
            icon = opUidl.getStringAttribute('icon')
            if icon is not None and len(icon) != 0:
                iconUrl = self.client.translateVaadinUri(icon)
                itemHtml = '<img src=\"' + iconUrl + '\" class=\"' + Icon.CLASSNAME + '\" alt=\"\" />' + itemHtml
            if self.isMultiselect():
                op = VCheckBox()
                op.setHTML(itemHtml)
            else:
                op = RadioButton(self.id, itemHtml, True)
                op.setStyleName('v-radiobutton')
            if icon is not None and len(icon) != 0:
                Util.sinkOnloadForImages(op.getElement())
                op.addHandler(self.iconLoadHandler, LoadEvent.getType())
            op.addStyleName(self.CLASSNAME_OPTION)
            op.setValue(opUidl.getBooleanAttribute('selected'))
            enabled = not opUidl.getBooleanAttribute('disabled') and not self.isReadonly() and not self.isDisabled()
            op.setEnabled(enabled)
            self.setStyleName(op.getElement(), ApplicationConnection.DISABLED_CLASSNAME, not enabled)
            op.addClickHandler(self)
            self._optionsToKeys.put(op, opUidl.getStringAttribute('key'))
            self._panel.add(op)

    def getSelectedItems(self):
        return list([None] * len(self.selectedKeys))

    def onClick(self, event):
        super(VOptionGroup, self).onClick(event)
        if isinstance(event.getSource(), CheckBox):
            selected = event.getSource().getValue()
            key = self._optionsToKeys[event.getSource()]
            if not self.isMultiselect():
                self.selectedKeys.clear()
            if selected:
                self.selectedKeys.add(key)
            else:
                self.selectedKeys.remove(key)
            self.client.updateVariable(self.id, 'selected', self.getSelectedItems(), self.isImmediate())

    def setTabIndex(self, tabIndex):
        _0 = True
        iterator = self._panel
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            widget = iterator.next()
            widget.setTabIndex(tabIndex)

    def focus(self):
        iterator = self._panel
        if iterator.hasNext():
            iterator.next().setFocus(True)

    def onFocus(self, arg0):
        if not self._blurOccured:
            # no blur occured before this focus event
            # panel was blurred => fire the event to the server side if
            # requested by server side
            if self._sendFocusEvents:
                self.client.updateVariable(self.id, EventId.FOCUS, '', True)
        else:
            # blur occured before this focus event
            # another control inside the panel (checkbox / radio box) was
            # blurred => do not fire the focus and set blurOccured to false, so
            # blur will not be fired, too
            self._blurOccured = False

    def onBlur(self, arg0):
        self._blurOccured = True
        if self._sendBlurEvents:

            class _0_(Command):

                def execute(self):
                    # check whether blurOccured still is true and then send the
                    # event out to the server
                    if VOptionGroup_this._blurOccured:
                        self.client.updateVariable(self.id, EventId.BLUR, '', True)
                        VOptionGroup_this._blurOccured = False

            _0_ = _0_()
            Scheduler.get().scheduleDeferred(_0_)
