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

from pyjamas.ui.UIObject import UIObject

from muntjac.terminal.gwt.client.ui.menu_bar import MenuBar


class MenuItem(UIObject, HasHTML):
    """A widget that can be placed in a
    L{pyjamas.ui.MenuBar.MenuBar}. Menu items can either fire a
    L{com.google.gwt.user.client.Command} when they are clicked, or open a
    cascading sub-menu.

    @deprecated:
    """

    _DEPENDENT_STYLENAME_SELECTED_ITEM = 'selected'

    def __init__(self, *args):
        """Constructs a new menu item that fires a command when it is selected.

        @param text
                   the item's text
        @param cmd
                   the command to be fired when it is selected
        ---
        Constructs a new menu item that fires a command when it is selected.

        @param text
                   the item's text
        @param asHTML
                   <code>true</code> to treat the specified text as html
        @param cmd
                   the command to be fired when it is selected
        ---
        Constructs a new menu item that cascades to a sub-menu when it is
        selected.

        @param text
                   the item's text
        @param subMenu
                   the sub-menu to be displayed when it is selected
        ---
        Constructs a new menu item that cascades to a sub-menu when it is
        selected.

        @param text
                   the item's text
        @param asHTML
                   <code>true</code> to treat the specified text as html
        @param subMenu
                   the sub-menu to be displayed when it is selected
        """
        self._command = None
        self._parentMenu = None
        self._subMenu = None

        args = args
        nargs = len(args)
        if nargs == 2:
            if isinstance(args[1], bool):
                text, asHTML = args
                self.setElement(DOM.createTD())
                self.setSelectionStyle(False)
                if asHTML:
                    self.setHTML(text)
                else:
                    self.setText(text)
                self.setStyleName('gwt-MenuItem')
            elif isinstance(args[1], MenuBar):
                text, subMenu = args
                self.__init__(text, False)
                self.setSubMenu(subMenu)
            else:
                text, cmd = args
                self.__init__(text, False)
                self.setCommand(cmd)
        elif nargs == 3:
            if isinstance(args[2], MenuBar):
                text, asHTML, subMenu = args
                self.__init__(text, asHTML)
                self.setSubMenu(subMenu)
            else:
                text, asHTML, cmd = args
                self.__init__(text, asHTML)
                self.setCommand(cmd)
        else:
            raise ValueError


    def getCommand(self):
        """Gets the command associated with this item.

        @return: this item's command, or C{None} if none exists
        """
        return self._command


    def getHTML(self):
        return DOM.getInnerHTML(self.getElement())


    def getParentMenu(self):
        """Gets the menu that contains this item.

        @return: the parent menu, or C{None} if none exists.
        """
        return self._parentMenu


    def getSubMenu(self):
        """Gets the sub-menu associated with this item.

        @return this item's sub-menu, or C{None} if none exists
        """

        return self._subMenu


    def getText(self):
        return DOM.getInnerText(self.getElement())


    def setCommand(self, cmd):
        """Sets the command associated with this item.

        @param cmd:
                   the command to be associated with this item
        """
        self._command = cmd


    def setHTML(self, html):
        DOM.setInnerHTML(self.getElement(), html)


    def setSubMenu(self, subMenu):
        """Sets the sub-menu associated with this item.

        @param subMenu:
                   this item's new sub-menu
        """
        self._subMenu = subMenu


    def setText(self, text):
        DOM.setInnerText(self.getElement(), text)


    def setParentMenu(self, parentMenu):
        self._parentMenu = parentMenu


    def setSelectionStyle(self, selected):
        if selected:
            self.addStyleDependentName(self._DEPENDENT_STYLENAME_SELECTED_ITEM)
        else:
            self.removeStyleDependentName(self._DEPENDENT_STYLENAME_SELECTED_ITEM)
