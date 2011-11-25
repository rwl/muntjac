# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.VTextField import (VTextField,)


class VTextArea(VTextField):
    """This class represents a multiline textfield (textarea).

    TODO consider replacing this with a RichTextArea based implementation. IE
    does not support CSS height for textareas in Strict mode :-(

    @author IT Mill Ltd.
    """
    CLASSNAME = 'v-textarea'

    def __init__(self):
        super(VTextArea, self)(DOM.createTextArea())
        self.setStyleName(self.CLASSNAME)

    def updateFromUIDL(self, uidl, client):
        # Call parent renderer explicitly
        super(VTextArea, self).updateFromUIDL(uidl, client)
        if uidl.hasAttribute('rows'):
            self.setRows(uidl.getIntAttribute('rows'))
        if self.getMaxLength() >= 0:
            self.sinkEvents(Event.ONKEYUP)

    def setRows(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            rows, = _0
            self.setRows(self.getElement(), rows)
        elif _1 == 2:
            e, r = _0
        else:
            raise ARGERROR(1, 2)

    JS("""
    try {
        if(e.tagName.toLowerCase() == "textarea")
                e.rows = r;
    } catch (e) {}
    """)

    def onBrowserEvent(self, event):
        if self.getMaxLength() >= 0 and event.getTypeInt() == Event.ONKEYUP:

            class _0_(Command):

                def execute(self):
                    if len(self.getText()) > self.getMaxLength():
                        self.setText(self.getText()[:self.getMaxLength()])

            _0_ = _0_()
            Scheduler.get().scheduleDeferred(_0_)
        super(VTextArea, self).onBrowserEvent(event)
