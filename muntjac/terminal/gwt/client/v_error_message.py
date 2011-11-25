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
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.HTML import HTML

from muntjac.terminal.gwt.client.ui.v_overlay import VOverlay


class VErrorMessage(FlowPanel):

    CLASSNAME = 'v-errormessage'

    def __init__(self):
        super(VErrorMessage, self).__init__()
        self.setStyleName(self.CLASSNAME)


    def updateFromUIDL(self, uidl):
        self.clear()
        if uidl.getChildCount() == 0:
            self.add(HTML(' '))
        else:
            for child in uidl.getChildIterator():
                if isinstance(child, basestring):
                    errorMessage = child
                    self.add(HTML(errorMessage))
                else:
                    try:
                        childError = VErrorMessage()
                        childError.updateFromUIDL(child)
                        self.add(childError)
                    except Exception:
                        self.add(HTML(child.getXMLAsString()))


    def showAt(self, indicatorElement):
        """Shows this error message next to given element.
        """
        errorContainer = self.getParent()
        if errorContainer is None:
            errorContainer = VOverlay()
            errorContainer.setWidget(self)

        pos = (DOM.getAbsoluteLeft(indicatorElement)
               + (2 * DOM.getIntElemAttribute(indicatorElement,
                                              'offsetHeight')),
               DOM.getAbsoluteTop(indicatorElement)
               + (2 * DOM.getIntElemAttribute(indicatorElement,
                                              'offsetHeight')))
        errorContainer.setPopupPosition(pos)
        errorContainer.show()


    def hide(self):
        errorContainer = self.getParent()
        if errorContainer is not None:
            errorContainer.hide()
