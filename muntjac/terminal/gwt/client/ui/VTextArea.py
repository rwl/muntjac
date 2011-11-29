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
