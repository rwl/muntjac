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

from pyjamas.ui.SimplePanel import SimplePanel

from muntjac.terminal.gwt.client.focusable import IFocusable


class SimpleFocusablePanel(SimplePanel, HasFocusHandlers, HasBlurHandlers,
            HasKeyDownHandlers, HasKeyPressHandlers, IFocusable):
    """Compared to FocusPanel in GWT this panel does not support eg.
    accesskeys, but is simpler by its dom hierarchy nor supports focusing
    via java api.
    """

    def __init__(self):
        # make focusable, as we don't need access key magic we don't need to
        # use FocusImpl.createFocusable
        self.setTabIndex(0)


    def addFocusHandler(self, handler):
        return self.addDomHandler(handler, FocusEvent.getType())


    def addBlurHandler(self, handler):
        return self.addDomHandler(handler, BlurEvent.getType())


    def addKeyDownHandler(self, handler):
        return self.addDomHandler(handler, KeyDownEvent.getType())


    def addKeyPressHandler(self, handler):
        return self.addDomHandler(handler, KeyPressEvent.getType())


    def addKeyUpHandler(self, handler):
        return self.addDomHandler(handler, KeyUpEvent.getType())


    def setFocus(self, focus):
        if focus:
            FocusImpl.getFocusImplForPanel().focus(self.getElement())
        else:
            FocusImpl.getFocusImplForPanel().blur(self.getElement())


    def focus(self):
        self.setFocus(True)


    def setTabIndex(self, tabIndex):
        self.getElement().setTabIndex(tabIndex)
