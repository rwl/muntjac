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

from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from java.util.Iterator import (Iterator,)


class VErrorMessage(FlowPanel):
    CLASSNAME = 'v-errormessage'

    def __init__(self):
        super(VErrorMessage, self)()
        self.setStyleName(self.CLASSNAME)

    def updateFromUIDL(self, uidl):
        self.clear()
        if uidl.getChildCount() == 0:
            self.add(self.HTML(' '))
        else:
            _0 = True
            it = uidl.getChildIterator()
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                child = it.next()
                if isinstance(child, str):
                    errorMessage = child
                    self.add(self.HTML(errorMessage))
                else:
                    # TODO XML type error, check if this can even happen
                    # anymore??
                    try:
                        childError = VErrorMessage()
                        childError.updateFromUIDL(child)
                        self.add(childError)
                    except Exception, e:
                        xml = child
                        self.add(self.HTML(xml.getXMLAsString()))

    def showAt(self, indicatorElement):
        """Shows this error message next to given element.

        @param indicatorElement
        """
        errorContainer = self.getParent()
        if errorContainer is None:
            errorContainer = VOverlay()
            errorContainer.setWidget(self)
        errorContainer.setPopupPosition(self.DOM.getAbsoluteLeft(indicatorElement) + (2 * self.DOM.getElementPropertyInt(indicatorElement, 'offsetHeight')), self.DOM.getAbsoluteTop(indicatorElement) + (2 * self.DOM.getElementPropertyInt(indicatorElement, 'offsetHeight')))
        errorContainer.show()

    def hide(self):
        errorContainer = self.getParent()
        if errorContainer is not None:
            errorContainer.hide()
