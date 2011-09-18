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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.MenuItem import (MenuItem,)
# from com.google.gwt.user.client.ui.PopupListener import (PopupListener,)
# from com.google.gwt.user.client.ui.PopupPanel import (PopupPanel,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.List import (List,)


class MenuBar(Widget, PopupListener):
    """A standard menu bar widget. A menu bar can contain any number of menu items,
    each of which can either fire a {@link com.google.gwt.user.client.Command} or
    open a cascaded menu bar.

    <p>
    <img class='gallery' src='MenuBar.png'/>
    </p>

    <h3>CSS Style Rules</h3>
    <ul class='css'>
    <li>.gwt-MenuBar { the menu bar itself }</li>
    <li>.gwt-MenuBar .gwt-MenuItem { menu items }</li>
    <li>
    .gwt-MenuBar .gwt-MenuItem-selected { selected menu items }</li>
    </ul>

    <p>
    <h3>Example</h3>
    {@example com.google.gwt.examples.MenuBarExample}
    </p>

    @deprecated
    """
    _body = None
    _items = list()
    _parentMenu = None
    _popup = None
    _selectedItem = None
    _shownChildMenu = None
    _vertical = None
    _autoOpen = None

    def __init__(self, *args):
        """Creates an empty horizontal menu bar.
        ---
        Creates an empty menu bar.

        @param vertical
                   <code>true</code> to orient the menu bar vertically
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(False)
        elif _1 == 1:
            vertical, = _0
            super(MenuBar, self)()
            table = self.DOM.createTable()
            self._body = self.DOM.createTBody()
            self.DOM.appendChild(table, self._body)
            if not vertical:
                tr = self.DOM.createTR()
                self.DOM.appendChild(self._body, tr)
            self._vertical = vertical
            outer = self.DOM.createDiv()
            self.DOM.appendChild(outer, table)
            self.setElement(outer)
            self.sinkEvents((self.Event.ONCLICK | self.Event.ONMOUSEOVER) | self.Event.ONMOUSEOUT)
            self.setStyleName('gwt-MenuBar')
        else:
            raise ARGERROR(0, 1)

    def addItem(self, *args):
        """Adds a menu item to the bar.

        @param item
                   the item to be added
        ---
        Adds a menu item to the bar, that will fire the given command when it is
        selected.

        @param text
                   the item's text
        @param asHTML
                   <code>true</code> to treat the specified text as html
        @param cmd
                   the command to be fired
        @return the {@link MenuItem} object created
        ---
        Adds a menu item to the bar, that will open the specified menu when it is
        selected.

        @param text
                   the item's text
        @param asHTML
                   <code>true</code> to treat the specified text as html
        @param popup
                   the menu to be cascaded from it
        @return the {@link MenuItem} object created
        ---
        Adds a menu item to the bar, that will fire the given command when it is
        selected.

        @param text
                   the item's text
        @param cmd
                   the command to be fired
        @return the {@link MenuItem} object created
        ---
        Adds a menu item to the bar, that will open the specified menu when it is
        selected.

        @param text
                   the item's text
        @param popup
                   the menu to be cascaded from it
        @return the {@link MenuItem} object created
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            item, = _0
            if self._vertical:
                tr = self.DOM.createTR()
                self.DOM.appendChild(self._body, tr)
            else:
                tr = self.DOM.getChild(self._body, 0)
            self.DOM.appendChild(tr, item.getElement())
            item.setParentMenu(self)
            item.setSelectionStyle(False)
            self._items.add(item)
        elif _1 == 2:
            if isinstance(_0[1], Command):
                text, cmd = _0
                item = MenuItem(text, cmd)
                self.addItem(item)
                return item
            else:
                text, popup = _0
                item = MenuItem(text, popup)
                self.addItem(item)
                return item
        elif _1 == 3:
            if isinstance(_0[2], Command):
                text, asHTML, cmd = _0
                item = MenuItem(text, asHTML, cmd)
                self.addItem(item)
                return item
            else:
                text, asHTML, popup = _0
                item = MenuItem(text, asHTML, popup)
                self.addItem(item)
                return item
        else:
            raise ARGERROR(1, 3)

    def clearItems(self):
        """Removes all menu items from this menu bar."""
        container = self.getItemContainerElement()
        while self.DOM.getChildCount(container) > 0:
            self.DOM.removeChild(container, self.DOM.getChild(container, 0))
        self._items.clear()

    def getAutoOpen(self):
        """Gets whether this menu bar's child menus will open when the mouse is
        moved over it.

        @return <code>true</code> if child menus will auto-open
        """
        return self._autoOpen

    def onBrowserEvent(self, event):
        super(MenuBar, self).onBrowserEvent(event)
        item = self.findItem(self.DOM.eventGetTarget(event))
        _0 = self.DOM.eventGetType(event)
        _1 = False
        while True:
            if _0 == self.Event.ONCLICK:
                _1 = True
                if item is not None:
                    self.doItemAction(item, True)
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEOVER):
                _1 = True
                if item is not None:
                    self.itemOver(item)
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEOUT):
                _1 = True
                if item is not None:
                    self.itemOver(None)
                break
            break

    def onPopupClosed(self, sender, autoClosed):
        # If the menu popup was auto-closed, close all of its parents as well.
        if autoClosed:
            self.closeAllParents()
        # When the menu popup closes, remember that no item is
        # currently showing a popup menu.
        self.onHide()
        self._shownChildMenu = None
        self._popup = None

    def removeItem(self, item):
        """Removes the specified menu item from the bar.

        @param item
                   the item to be removed
        """
        idx = self._items.index(item)
        if idx == -1:
            return
        container = self.getItemContainerElement()
        self.DOM.removeChild(container, self.DOM.getChild(container, idx))
        self._items.remove(idx)

    def setAutoOpen(self, autoOpen):
        """Sets whether this menu bar's child menus will open when the mouse is
        moved over it.

        @param autoOpen
                   <code>true</code> to cause child menus to auto-open
        """
        self._autoOpen = autoOpen

    def getItems(self):
        """Returns a list containing the <code>MenuItem</code> objects in the menu
        bar. If there are no items in the menu bar, then an empty
        <code>List</code> object will be returned.

        @return a list containing the <code>MenuItem</code> objects in the menu
                bar
        """
        return self._items

    def getSelectedItem(self):
        """Returns the <code>MenuItem</code> that is currently selected
        (highlighted) by the user. If none of the items in the menu are currently
        selected, then <code>null</code> will be returned.

        @return the <code>MenuItem</code> that is currently selected, or
                <code>null</code> if no items are currently selected
        """
        return self._selectedItem

    def onDetach(self):
        # When the menu is detached, make sure to close all of its children.
        # Closes all parent menu popups.
        if self._popup is not None:
            self._popup.hide()
        super(MenuBar, self).onDetach()

    def closeAllParents(self):
        # Performs the action associated with the given menu item. If the item has
        # a popup associated with it, the popup will be shown. If it has a command
        # associated with it, and 'fireCommand' is true, then the command will be
        # fired. Popups associated with other items will be hidden.
        # 
        # @param item the item whose popup is to be shown. @param fireCommand
        # <code>true</code> if the item's command should be fired,
        # <code>false</code> otherwise.

        curMenu = self
        while curMenu is not None:
            curMenu.close()
            if curMenu.parentMenu is None and curMenu.selectedItem is not None:
                curMenu.selectedItem.setSelectionStyle(False)
                curMenu.selectedItem = None
            curMenu = curMenu.parentMenu

    def doItemAction(self, item, fireCommand):
        # If the given item is already showing its menu, we're done.
        if (
            self._shownChildMenu is not None and item.getSubMenu() == self._shownChildMenu
        ):
            return
        # If another item is showing its menu, then hide it.
        if self._shownChildMenu is not None:
            self._shownChildMenu.onHide()
            self._popup.hide()
        # If the item has no popup, optionally fire its command.
        if item.getSubMenu() is None:
            if fireCommand:
                # Close this menu and all of its parents.
                self.closeAllParents()
                # Fire the item's command.
                cmd = item.getCommand()
                if cmd is not None:
                    self.Scheduler.get().scheduleDeferred(cmd)
            return
        # Ensure that the item is selected.
        self.selectItem(item)
        # Create a new popup for this item, and position it next to
        # the item (below if this is a horizontal menu bar, to the
        # right if it's a vertical bar).

        class _0_(VOverlay):
            self.setWidget(self.item.getSubMenu())
            self.item.getSubMenu().onShow()

            def onEventPreview(self, event):
                # Hook the popup panel's event preview. We use this to keep it
                # from
                # auto-hiding when the parent menu is clicked.
                _0 = self.DOM.eventGetType(event)
                _1 = False
                while True:
                    if _0 == self.Event.ONCLICK:
                        _1 = True
                        target = self.DOM.eventGetTarget(event)
                        parentMenuElement = self.item.getParentMenu().getElement()
                        if self.DOM.isOrHasChild(parentMenuElement, target):
                            return False
                        break
                    break
                return super(_0_, self).onEventPreview(event)

        _0_ = self._0_(True)
        self._popup = _0_
        self._popup.addPopupListener(self)
        if self._vertical:
            self._popup.setPopupPosition(item.getAbsoluteLeft() + item.getOffsetWidth(), item.getAbsoluteTop())
        else:
            self._popup.setPopupPosition(item.getAbsoluteLeft(), item.getAbsoluteTop() + item.getOffsetHeight())
        self._shownChildMenu = item.getSubMenu()
        item.getSubMenu().parentMenu = self
        # Show the popup, ensuring that the menubar's event preview remains on
        # top
        # of the popup's.
        self._popup.show()

    def itemOver(self, item):
        if item is None:
            # Don't clear selection if the currently selected item's menu is
            # showing.
            if (
                self._selectedItem is not None and self._shownChildMenu == self._selectedItem.getSubMenu()
            ):
                return
        # Style the item selected when the mouse enters.
        self.selectItem(item)
        # If child menus are being shown, or this menu is itself
        # a child menu, automatically show an item's child menu
        # when the mouse enters.
        if item is not None:
            if (
                ((self._shownChildMenu is not None) or (self._parentMenu is not None)) or self._autoOpen
            ):
                self.doItemAction(item, False)

    def selectItem(self, item):
        if item == self._selectedItem:
            return
        if self._selectedItem is not None:
            self._selectedItem.setSelectionStyle(False)
        if item is not None:
            item.setSelectionStyle(True)
        self._selectedItem = item

    def close(self):
        """Closes this menu (if it is a popup)."""
        if self._parentMenu is not None:
            self._parentMenu.popup.hide()

    def findItem(self, hItem):
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._items)):
                break
            item = self._items[i]
            if self.DOM.isOrHasChild(item.getElement(), hItem):
                return item
        return None

    def getItemContainerElement(self):
        # This method is called when a menu bar is hidden, so that it can hide any
        # child popups that are currently being shown.

        if self._vertical:
            return self._body
        else:
            return self.DOM.getChild(self._body, 0)

    def onHide(self):
        # This method is called when a menu bar is shown.
        if self._shownChildMenu is not None:
            self._shownChildMenu.onHide()
            self._popup.hide()

    def onShow(self):
        # Select the first item when a menu is shown.
        if len(self._items) > 0:
            self.selectItem(self._items[0])
