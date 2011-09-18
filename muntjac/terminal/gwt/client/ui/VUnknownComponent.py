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

from com.vaadin.terminal.gwt.client.VUIDLBrowser import (VUIDLBrowser,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
# from com.google.gwt.user.client.ui.Tree import (Tree,)


class VUnknownComponent(Composite, Paintable):
    _caption = com.google.gwt.user.client.ui.Label()
    _uidlTree = None
    _panel = None
    _serverClassName = 'unkwnown'

    def __init__(self):
        self._panel = self.VerticalPanel()
        self._panel.add(self._caption)
        self.initWidget(self._panel)
        self.setStyleName('vaadin-unknown')
        self._caption.setStyleName('vaadin-unknown-caption')

    def setServerSideClassName(self, serverClassName):
        self._serverClassName = serverClassName

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, False):
            return
        self.setCaption('Widgetset does not contain implementation for ' + self._serverClassName + '. Check its @ClientWidget mapping, widgetsets ' + 'GWT module description file and re-compile your' + ' widgetset. In case you have downloaded a vaadin' + ' add-on package, you might want to refer to ' + '<a href=\'http://vaadin.com/using-addons\'>add-on ' + 'instructions</a>. Unrendered UIDL:')
        if self._uidlTree is not None:
            self._uidlTree.removeFromParent()
        self._uidlTree = VUIDLBrowser(uidl, client.getConfiguration())
        self._panel.add(self._uidlTree)

    def setCaption(self, c):
        self._caption.getElement().setInnerHTML(c)
