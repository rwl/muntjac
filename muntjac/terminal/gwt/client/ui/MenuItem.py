# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.MenuBar import (MenuBar,)


class MenuItem(UIObject, HasHTML):
    """A widget that can be placed in a
    {@link com.google.gwt.user.client.ui.MenuBar}. Menu items can either fire a
    {@link com.google.gwt.user.client.Command} when they are clicked, or open a
    cascading sub-menu.

    @deprecated
    """
    _DEPENDENT_STYLENAME_SELECTED_ITEM = 'selected'
    _command = None
    _parentMenu = None
    _subMenu = None

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
        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[1], Command):
                text, cmd = _0
                self.__init__(text, False)
                self.setCommand(cmd)
            elif isinstance(_0[1], MenuBar):
                text, subMenu = _0
                self.__init__(text, False)
                self.setSubMenu(subMenu)
            else:
                text, asHTML = _0
                self.setElement(DOM.createTD())
                self.setSelectionStyle(False)
                if asHTML:
                    self.setHTML(text)
                else:
                    self.setText(text)
                self.setStyleName('gwt-MenuItem')
        elif _1 == 3:
            if isinstance(_0[2], Command):
                text, asHTML, cmd = _0
                self.__init__(text, asHTML)
                self.setCommand(cmd)
            else:
                text, asHTML, subMenu = _0
                self.__init__(text, asHTML)
                self.setSubMenu(subMenu)
        else:
            raise ARGERROR(2, 3)

    def getCommand(self):
        """Gets the command associated with this item.

        @return this item's command, or <code>null</code> if none exists
        """
        return self._command

    def getHTML(self):
        return DOM.getInnerHTML(self.getElement())

    def getParentMenu(self):
        """Gets the menu that contains this item.

        @return the parent menu, or <code>null</code> if none exists.
        """
        return self._parentMenu

    def getSubMenu(self):
        """Gets the sub-menu associated with this item.

        @return this item's sub-menu, or <code>null</code> if none exists
        """
        return self._subMenu

    def getText(self):
        return DOM.getInnerText(self.getElement())

    def setCommand(self, cmd):
        """Sets the command associated with this item.

        @param cmd
                   the command to be associated with this item
        """
        self._command = cmd

    def setHTML(self, html):
        DOM.setInnerHTML(self.getElement(), html)

    def setSubMenu(self, subMenu):
        """Sets the sub-menu associated with this item.

        @param subMenu
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
