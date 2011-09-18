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

from __pyjamas__ import (ARGERROR, PREDEC, PREINC,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.SubPartAware import (SubPartAware,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.TooltipInfo import (TooltipInfo,)
from com.vaadin.terminal.gwt.client.ContainerResizedListener import (ContainerResizedListener,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
from com.vaadin.terminal.gwt.client.ui.SimpleFocusablePanel import (SimpleFocusablePanel,)
# from com.google.gwt.user.client.ui.RootPanel import (RootPanel,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Iterator import (Iterator,)
# from java.util.List import (List,)
# from java.util.Stack import (Stack,)


class VMenuBar(SimpleFocusablePanel, Paintable, CloseHandler, ContainerResizedListener, KeyPressHandler, KeyDownHandler, FocusHandler, SubPartAware):
    # The hierarchy of VMenuBar is a bit weird as VMenuBar is the Paintable,
    # used for the root menu but also used for the sub menus.
    # Set the CSS class name to allow styling.
    CLASSNAME = 'v-menubar'
    # For server connections *
    uidlId = None
    client = None
    submenuIcon = None
    moreItem = None
    # Only used by the root menu bar
    collapsedRootItems = None
    # Construct an empty command to be used when the item has no command
    # associated
    emptyCommand = None
    OPEN_ROOT_MENU_ON_HOWER = 'ormoh'
    ATTRIBUTE_CHECKED = 'checked'
    # Widget fields *
    subMenu = None
    items = None
    containerElement = None
    popup = None
    visibleChildMenu = None
    menuVisible = False
    parentMenu = None
    selected = None
    _enabled = True
    _width = 'notinited'
    _iconLoadedExecutioner = 
    class _0_(ScheduledCommand):

        def execute(self):
            self.iLayout(True)

    _0_ = _0_()
    VLazyExecutor(100, _0_)
    _openRootOnHover = None

    def __init__(self, *args):
        # Create an empty horizontal menubar
        self.hostReference = self
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(False, None)
            # Navigation is only handled by the root bar
            self.addFocusHandler(self)
            # Firefox auto-repeat works correctly only if we use a key press
            # handler, other browsers handle it correctly when using a key down
            # handler

            if BrowserInfo.get().isGecko():
                self.addKeyPressHandler(self)
            else:
                self.addKeyDownHandler(self)
        elif _1 == 2:
            subMenu, parentMenu = _0
            self.items = list()
            self.popup = None
            self.visibleChildMenu = None
            self.containerElement = self.getElement()
            if not subMenu:
                self.setStyleName(self.CLASSNAME)
            else:
                self.setStyleName(self.CLASSNAME + '-submenu')
                self.parentMenu = parentMenu
            self.subMenu = subMenu
            self.sinkEvents(((self.Event.ONCLICK | self.Event.ONMOUSEOVER) | self.Event.ONMOUSEOUT) | self.Event.ONLOAD)
            self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        else:
            raise ARGERROR(0, 2)

    def onDetach(self):
        super(VMenuBar, self).onDetach()
        if not self.subMenu:
            self.setSelected(None)
            self.hideChildren()
            self.menuVisible = False

    def setWidth(self, width):
        # if (Util.equals(this.width, width)) {
        # return;
        # }
        self._width = width
        if BrowserInfo.get().isIE6() and width.endswith('px'):
            # IE6 sometimes measures wrong using
            # Util.setWidthExcludingPaddingAndBorder so this is extracted to a
            # special case that uses another method. Really should fix the
            # Util.setWidthExcludingPaddingAndBorder method but that will
            # probably break additional cases
            requestedPixelWidth = int(width[:-2])
            paddingBorder = Util.measureHorizontalPaddingAndBorder(self.getElement(), 0)
            w = requestedPixelWidth - paddingBorder
            if w < 0:
                w = 0
            self.getElement().getStyle().setWidth(w, self.Unit.PX)
        else:
            Util.setWidthExcludingPaddingAndBorder(self, width, 0)
        if not self.subMenu:
            # Only needed for root level menu
            self.hideChildren()
            self.setSelected(None)
            self.menuVisible = False

    def updateFromUIDL(self, uidl, client):
        """This method must be implemented to update the client-side component from
        UIDL data received from server.

        This method is called when the page is loaded for the first time, and
        every time UI changes in the component are received from the server.
        """
        # This call should be made first. Ensure correct implementation,
        # and let the containing layout manage caption, etc.
        # updateFromUIDL
        if client.updateComponent(self, uidl, True):
            return
        self._openRootOnHover = uidl.getBooleanAttribute(self.OPEN_ROOT_MENU_ON_HOWER)
        self._enabled = not uidl.getBooleanAttribute('disabled')
        # For future connections
        self.client = client
        self.uidlId = uidl.getId()
        # Empty the menu every time it receives new information
        if not self.getItems().isEmpty():
            self.clearItems()
        options = uidl.getChildUIDL(0)
        # FIXME remove in version 7
        if options.hasAttribute('submenuIcon'):
            self.submenuIcon = client.translateVaadinUri(uidl.getChildUIDL(0).getStringAttribute('submenuIcon'))
        else:
            self.submenuIcon = None
        if uidl.hasAttribute('width'):
            moreItemUIDL = options.getChildUIDL(0)
            itemHTML = str()
            if moreItemUIDL.hasAttribute('icon'):
                itemHTML.__add__('<img src=\"' + client.translateVaadinUri(moreItemUIDL.getStringAttribute('icon')) + '\" class=\"' + Icon.CLASSNAME + '\" alt=\"\" />')
            moreItemText = moreItemUIDL.getStringAttribute('text')
            if '' == moreItemText:
                moreItemText = '&#x25BA;'
            itemHTML.__add__(moreItemText)
            self.moreItem = self.GWT.create(self.CustomMenuItem)
            self.moreItem.setHTML(str(itemHTML))
            self.moreItem.setCommand(self.emptyCommand)
            self.collapsedRootItems = VMenuBar(True, client.getPaintable(self.uidlId))
            self.moreItem.setSubMenu(self.collapsedRootItems)
            self.moreItem.addStyleName(self.CLASSNAME + '-more-menuitem')
        uidlItems = uidl.getChildUIDL(1)
        itr = uidlItems.getChildIterator()
        iteratorStack = Stack()
        menuStack = Stack()
        currentMenu = self
        while itr.hasNext():
            item = itr.next()
            currentItem = None
            itemId = item.getIntAttribute('id')
            itemHasCommand = item.hasAttribute('command')
            itemIsCheckable = item.hasAttribute(self.ATTRIBUTE_CHECKED)
            itemHTML = self.buildItemHTML(item)
            cmd = None
            if not item.hasAttribute('separator'):
                if itemHasCommand or itemIsCheckable:
                    # Construct a command that fires onMenuClick(int) with the
                    # item's id-number

                    class _0_(Command):

                        def execute(self):
                            self.hostReference.onMenuClick(self.itemId)

                    _0_ = self._0_()
                    cmd = _0_
            currentItem = currentMenu.addItem(str(itemHTML), cmd)
            currentItem.updateFromUIDL(item, client)
            if item.getChildCount() > 0:
                menuStack.push(currentMenu)
                iteratorStack.push(itr)
                itr = item.getChildIterator()
                currentMenu = VMenuBar(True, currentMenu)
                if uidl.hasAttribute('style'):
                    for style in uidl.getStringAttribute('style').split(' '):
                        currentMenu.addStyleDependentName(style)
                currentItem.setSubMenu(currentMenu)
            while not itr.hasNext() and not iteratorStack.empty():
                hasCheckableItem = False
                for menuItem in currentMenu.getItems():
                    hasCheckableItem = hasCheckableItem or menuItem.isCheckable()
                if hasCheckableItem:
                    currentMenu.addStyleDependentName('check-column')
                else:
                    currentMenu.removeStyleDependentName('check-column')
                itr = iteratorStack.pop()
                currentMenu = menuStack.pop()
        # while
        self.iLayout(False)

    def buildItemHTML(self, item):
        """Build the HTML content for a menu item.

        @param item
        @return
        """
        # Construct html from the text and the optional icon
        itemHTML = str()
        if item.hasAttribute('separator'):
            itemHTML.__add__('<span>---</span>')
        else:
            # Add submenu indicator
            if item.getChildCount() > 0:
                # FIXME For compatibility reasons: remove in version 7
                bgStyle = ''
                if self.submenuIcon is not None:
                    bgStyle = ' style=\"background-image: url(' + self.submenuIcon + '); text-indent: -999px; width: 1em;\"'
                itemHTML.__add__('<span class=\"' + self.CLASSNAME + '-submenu-indicator\"' + bgStyle + '>&#x25BA;</span>')
            itemHTML.__add__('<span class=\"' + self.CLASSNAME + '-menuitem-caption\">')
            if item.hasAttribute('icon'):
                itemHTML.__add__('<img src=\"' + self.client.translateVaadinUri(item.getStringAttribute('icon')) + '\" class=\"' + Icon.CLASSNAME + '\" alt=\"\" />')
            itemText = item.getStringAttribute('text')
            itemHTML.__add__(Util.escapeHTML(itemText))
            itemHTML.__add__('</span>')
        return str(itemHTML)

    def onMenuClick(self, clickedItemId):
        """This is called by the items in the menu and it communicates the
        information to the server

        @param clickedItemId
                   id of the item that was clicked
        """
        # Updating the state to the server can not be done before
        # the server connection is known, i.e., before updateFromUIDL()
        # has been called.
        # Widget methods *
        if self.uidlId is not None and self.client is not None:
            # Communicate the user interaction parameters to server. This call
            # will initiate an AJAX request to the server.
            self.client.updateVariable(self.uidlId, 'clickedId', clickedItemId, True)

    def getItems(self):
        """Returns a list of items in this menu"""
        return self.items

    def clearItems(self):
        """Remove all the items in this menu"""
        e = self.getContainerElement()
        while self.DOM.getChildCount(e) > 0:
            self.DOM.removeChild(e, self.DOM.getChild(e, 0))
        self.items.clear()

    def getContainerElement(self):
        """Returns the containing element of the menu

        @return
        """
        return self.containerElement

    def addItem(self, *args):
        """Add a new item to this menu

        @param html
                   items text
        @param cmd
                   items command
        @return the item created
        ---
        Add a new item to this menu

        @param item
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            item, = _0
            if self.items.contains(item):
                return
            self.DOM.appendChild(self.getContainerElement(), item.getElement())
            item.setParentMenu(self)
            item.setSelected(False)
            self.items.add(item)
        elif _1 == 2:
            if isinstance(_0[0], CustomMenuItem):
                item, index = _0
                if self.items.contains(item):
                    return
                self.DOM.insertChild(self.getContainerElement(), item.getElement(), index)
                item.setParentMenu(self)
                item.setSelected(False)
                self.items.add(index, item)
            else:
                html, cmd = _0
                item = self.GWT.create(self.CustomMenuItem)
                item.setHTML(html)
                item.setCommand(cmd)
                self.addItem(item)
                return item
        else:
            raise ARGERROR(1, 2)

    def removeItem(self, item):
        """Remove the given item from this menu

        @param item
        """
        # @see
        # com.google.gwt.user.client.ui.Widget#onBrowserEvent(com.google.gwt.user
        # .client.Event)

        if self.items.contains(item):
            index = self.items.index(item)
            self.DOM.removeChild(self.getContainerElement(), self.DOM.getChild(self.getContainerElement(), index))
            self.items.remove(index)

    def onBrowserEvent(self, e):
        super(VMenuBar, self).onBrowserEvent(e)
        # Handle onload events (icon loaded, size changes)
        if self.DOM.eventGetType(e) == self.Event.ONLOAD:
            if BrowserInfo.get().isIE6():
                Util.doIE6PngFix(self.Element.as_(e.getEventTarget()))
            parent = self.getParentMenu()
            if parent is not None:
                # The onload event for an image in a popup should be sent to
                # the parent, which owns the popup
                parent.iconLoaded()
            else:
                # Onload events for images in the root menu are handled by the
                # root menu itself
                self.iconLoaded()
            return
        targetElement = self.DOM.eventGetTarget(e)
        targetItem = None
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self.items)):
                break
            item = self.items[i]
            if self.DOM.isOrHasChild(item.getElement(), targetElement):
                targetItem = item
        # Handle tooltips
        if targetItem is None and self.client is not None:
            # Handle root menubar tooltips
            self.client.handleTooltipEvent(e, self)
        elif targetItem is not None:
            # Handle item tooltips
            targetItem.onBrowserEvent(e)
        if targetItem is not None:
            _1 = self.DOM.eventGetType(e)
            _2 = False
            while True:
                if _1 == self.Event.ONCLICK:
                    _2 = True
                    if self.isEnabled() and targetItem.isEnabled():
                        self.itemClick(targetItem)
                    if self.subMenu:
                        # Prevent moving keyboard focus to child menus
                        parent = self.parentMenu
                        while parent.getParentMenu() is not None:
                            parent = parent.getParentMenu()
                        parent.setFocus(True)
                    break
                if (_2 is True) or (_1 == self.Event.ONMOUSEOVER):
                    _2 = True
                    self.LazyCloser.cancelClosing()
                    if self.isEnabled() and targetItem.isEnabled():
                        self.itemOver(targetItem)
                    break
                if (_2 is True) or (_1 == self.Event.ONMOUSEOUT):
                    _2 = True
                    self.itemOut(targetItem)
                    self.LazyCloser.schedule()
                    break
                break
        elif (
            self.subMenu and self.DOM.eventGetType(e) == self.Event.ONCLICK and self.subMenu
        ):
            # Prevent moving keyboard focus to child menus
            parent = self.parentMenu
            while parent.getParentMenu() is not None:
                parent = parent.getParentMenu()
            parent.setFocus(True)

    def isEnabled(self):
        return self._enabled

    def iconLoaded(self):
        self._iconLoadedExecutioner.trigger()

    def itemClick(self, item):
        """When an item is clicked

        @param item
        """
        if item.getCommand() is not None:
            self.setSelected(None)
            if self.visibleChildMenu is not None:
                self.visibleChildMenu.hideChildren()
            self.hideParents(True)
            self.menuVisible = False
            self.Scheduler.get().scheduleDeferred(item.getCommand())
        elif (
            item.getSubMenu() is not None and item.getSubMenu() != self.visibleChildMenu
        ):
            self.setSelected(item)
            self.showChildMenu(item)
            self.menuVisible = True
        elif not self.subMenu:
            self.setSelected(None)
            self.hideChildren()
            self.menuVisible = False

    def itemOver(self, item):
        """When the user hovers the mouse over the item

        @param item
        """
        if (
            (self._openRootOnHover or self.subMenu) or self.menuVisible and not item.isSeparator()
        ):
            self.setSelected(item)
            if not self.subMenu and self._openRootOnHover and not self.menuVisible:
                self.menuVisible = True
                # start opening menus
                self.LazyCloser.prepare(self)
        if (
            self.menuVisible and self.visibleChildMenu != item.getSubMenu() and self.popup is not None
        ):
            self.popup.hide()
        if (
            self.menuVisible and item.getSubMenu() is not None and self.visibleChildMenu != item.getSubMenu()
        ):
            self.showChildMenu(item)

    def itemOut(self, item):
        """When the mouse is moved away from an item

        @param item
        """
        if self.visibleChildMenu != item.getSubMenu():
            self.hideChildMenu(item)
            self.setSelected(None)
        elif self.visibleChildMenu is None:
            self.setSelected(None)

    class LazyCloser(Timer):
        """Used to autoclose submenus when they the menu is in a mode which opens
        root menus on mouse hover.
        """
        INSTANCE = None
        _activeRoot = None

        def run(self):
            self._activeRoot.hideChildren()
            self._activeRoot.setSelected(None)
            self._activeRoot.menuVisible = False
            self._activeRoot = None

        @classmethod
        def cancelClosing(cls):
            if cls.INSTANCE is not None:
                cls.INSTANCE.cancel()

        @classmethod
        def prepare(cls, vMenuBar):
            if cls.INSTANCE is None:
                cls.INSTANCE = cls.LazyCloser()
            if cls.INSTANCE.activeRoot == vMenuBar:
                cls.INSTANCE.cancel()
            elif cls.INSTANCE.activeRoot is not None:
                cls.INSTANCE.cancel()
                cls.INSTANCE.run()
            cls.INSTANCE.activeRoot = vMenuBar

        @classmethod
        def schedule(cls):
            if cls.INSTANCE is not None and cls.INSTANCE.activeRoot is not None:
                cls.INSTANCE.schedule(750)

    def showChildMenu(self, item):
        """Shows the child menu of an item. The caller must ensure that the item has
        a submenu.

        @param item
        """
        left = 0
        top = 0
        if self.subMenu:
            left = item.getParentMenu().getAbsoluteLeft() + item.getParentMenu().getOffsetWidth()
            top = item.getAbsoluteTop()
        else:
            left = item.getAbsoluteLeft()
            top = item.getParentMenu().getAbsoluteTop() + item.getParentMenu().getOffsetHeight()
        self.showChildMenuAt(item, top, left)

    def showChildMenuAt(self, item, top, left):
        shadowSpace = 10
        self.popup = VOverlay(True, False, True)
        self.popup.setStyleName(self.CLASSNAME + '-popup')
        self.popup.setWidget(item.getSubMenu())
        self.popup.addCloseHandler(self)
        self.popup.addAutoHidePartner(item.getElement())
        # at 0,0 because otherwise IE7 add extra scrollbars (#5547)
        self.popup.setPopupPosition(0, 0)
        item.getSubMenu().onShow()
        self.visibleChildMenu = item.getSubMenu()
        item.getSubMenu().setParentMenu(self)
        self.popup.show()
        if (
            left + self.popup.getOffsetWidth() >= RootPanel.getBodyElement().getOffsetWidth() - shadowSpace
        ):
            if self.subMenu:
                left = item.getParentMenu().getAbsoluteLeft() - self.popup.getOffsetWidth() - shadowSpace
            else:
                left = RootPanel.getBodyElement().getOffsetWidth() - self.popup.getOffsetWidth() - shadowSpace
            # Accommodate space for shadow
            if left < shadowSpace:
                left = shadowSpace
        self.popup.setPopupPosition(left, top)
        # IE7 really tests one's patience sometimes
        # Part of a fix to correct #3850
        if BrowserInfo.get().isIE7():
            self.popup.getElement().getStyle().setProperty('zoom', '')

            class _1_(Command):

                def execute(self):
                    if self.popup is None:
                        # The child menu can be hidden before this command is
                        # run.
                        return
                    if (
                        (self.popup.getElement().getStyle().getProperty('width') is None) or (self.popup.getElement().getStyle().getProperty('width') == '')
                    ):
                        self.popup.setWidth(self.popup.getOffsetWidth() + 'px')
                    self.popup.getElement().getStyle().setProperty('zoom', '1')

            _1_ = self._1_()
            self.Scheduler.get().scheduleDeferred(_1_)

    def hideChildMenu(self, item):
        """Hides the submenu of an item

        @param item
        """
        if (
            self.visibleChildMenu is not None and not (self.visibleChildMenu == item.getSubMenu())
        ):
            self.popup.hide()

    def onShow(self):
        """When the menu is shown."""
        # remove possible previous selection
        if self.selected is not None:
            self.selected.setSelected(False)
            self.selected = None
        self.menuVisible = True

    def onClose(self, event):
        """Listener method, fired when this menu is closed"""
        self.hideChildren()
        if event.isAutoClosed():
            self.hideParents(True)
            self.menuVisible = False
        self.visibleChildMenu = None
        self.popup = None

    def hideChildren(self):
        """Recursively hide all child menus"""
        if self.visibleChildMenu is not None:
            self.visibleChildMenu.hideChildren()
            self.popup.hide()

    def hideParents(self, autoClosed):
        """Recursively hide all parent menus"""
        if self.visibleChildMenu is not None:
            self.popup.hide()
            self.setSelected(None)
            self.menuVisible = not autoClosed
        if self.getParentMenu() is not None:
            self.getParentMenu().hideParents(autoClosed)

    def getParentMenu(self):
        """Returns the parent menu of this menu, or null if this is the top-level
        menu

        @return
        """
        return self.parentMenu

    def setParentMenu(self, parent):
        """Set the parent menu of this menu

        @param parent
        """
        self.parentMenu = parent

    def getSelected(self):
        """Returns the currently selected item of this menu, or null if nothing is
        selected

        @return
        """
        return self.selected

    def setSelected(self, item):
        """Set the currently selected item of this menu

        @param item
        """
        # If we had something selected, unselect
        if item != self.selected and self.selected is not None:
            self.selected.setSelected(False)
        # If we have a valid selection, select it
        if item is not None:
            item.setSelected(True)
        self.selected = item

    class CustomMenuItem(Widget, HasHTML):
        """A class to hold information on menu items"""
        # @author Jouni Koivuviita / IT Mill Ltd.
        _client = None
        html = None
        command = None
        subMenu = None
        parentMenu = None
        enabled = True
        v_isSeparator = False
        checkable = False
        checked = False

        def __init__(self, *args):
            """Default menu item {@link Widget} constructor for GWT.create().

            Use {@link #setHTML(String)} and {@link #setCommand(Command)} after
            constructing a menu item.
            ---
            Creates a menu item {@link Widget}.

            @param html
            @param cmd
            @deprecated use the default constructor and {@link #setHTML(String)}
                        and {@link #setCommand(Command)} instead
            """
            _0 = args
            _1 = len(args)
            if _1 == 0:
                self.__init__('', None)
            elif _1 == 2:
                html, cmd = _0
                self.setElement(self.DOM.createSpan())
                self.setHTML(html)
                self.setCommand(cmd)
                self.setSelected(False)
                self.setStyleName(self.CLASSNAME + '-menuitem')
                self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
            else:
                raise ARGERROR(0, 2)

        # We need spans to allow inline-block in IE

        def setSelected(self, selected):
            if selected and not self.v_isSeparator:
                self.addStyleDependentName('selected')
                # needed for IE6 to have a single style name to match for an
                # element
                if self.checkable:
                    if self.checked:
                        self.removeStyleDependentName('selected-unchecked')
                        self.addStyleDependentName('selected-checked')
                    else:
                        self.removeStyleDependentName('selected-checked')
                        self.addStyleDependentName('selected-unchecked')
            else:
                self.removeStyleDependentName('selected')
                # needed for IE6 to have a single style name to match for an
                # element
                self.removeStyleDependentName('selected-checked')
                self.removeStyleDependentName('selected-unchecked')

        def setChecked(self, checked):
            if self.checkable and not self.v_isSeparator:
                self.checked = checked
                if checked:
                    self.addStyleDependentName('checked')
                    self.removeStyleDependentName('unchecked')
                else:
                    self.addStyleDependentName('unchecked')
                    self.removeStyleDependentName('checked')
            else:
                self.checked = False

        def isChecked(self):
            return self.checked

        def setCheckable(self, checkable):
            if checkable and not self.v_isSeparator:
                self.checkable = True
            else:
                self.setChecked(False)
                self.checkable = False

        def isCheckable(self):
            # setters and getters for the fields
            return self.checkable

        def setSubMenu(self, subMenu):
            self.subMenu = subMenu

        def getSubMenu(self):
            return self.subMenu

        def setParentMenu(self, parentMenu):
            self.parentMenu = parentMenu

        def getParentMenu(self):
            return self.parentMenu

        def setCommand(self, command):
            self.command = command

        def getCommand(self):
            return self.command

        def getHTML(self):
            return self.html

        def setHTML(self, html):
            self.html = html
            self.DOM.setInnerHTML(self.getElement(), html)
            # Sink the onload event for any icons. The onload
            # events are handled by the parent VMenuBar.
            Util.sinkOnloadForImages(self.getElement())

        def getText(self):
            return self.html

        def setText(self, text):
            self.setHTML(Util.escapeHTML(text))

        def setEnabled(self, enabled):
            self.enabled = enabled
            if enabled:
                self.removeStyleDependentName('disabled')
            else:
                self.addStyleDependentName('disabled')

        def isEnabled(self):
            return self.enabled

        def setSeparator(self, separator):
            self.v_isSeparator = separator
            if separator:
                self.setStyleName(self.CLASSNAME + '-separator')
            else:
                self.setStyleName(self.CLASSNAME + '-menuitem')
                self.setEnabled(self.enabled)

        def isSeparator(self):
            return self.v_isSeparator

        def updateFromUIDL(self, uidl, client):
            self._client = client
            self.setSeparator(uidl.hasAttribute('separator'))
            self.setEnabled(not uidl.hasAttribute('disabled'))
            if not self.isSeparator() and uidl.hasAttribute(self.ATTRIBUTE_CHECKED):
                # if the selected attribute is present (either true or false),
                # the item is selectable
                self.setCheckable(True)
                self.setChecked(uidl.getBooleanAttribute(self.ATTRIBUTE_CHECKED))
            else:
                self.setCheckable(False)
            if uidl.hasAttribute('style'):
                itemStyle = uidl.getStringAttribute('style')
                self.addStyleDependentName(itemStyle)
            if uidl.hasAttribute('description'):
                description = uidl.getStringAttribute('description')
                info = TooltipInfo(description)
                root = self.findRootMenu()
                client.registerTooltip(root, self, info)

        def onBrowserEvent(self, event):
            super(CustomMenuItem, self).onBrowserEvent(event)
            if self._client is not None:
                self._client.handleTooltipEvent(event, self.findRootMenu(), self)

        def findRootMenu(self):
            menubar = self.getParentMenu()
            # Traverse up until root menu is found
            while menubar.getParentMenu() is not None:
                menubar = menubar.getParentMenu()
            return menubar

    _paddingWidth = -1

    def iLayout(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.iLayout(False)
        elif _1 == 1:
            iconLoadEvent, = _0
            if (
                (len(self.getItems()) > 1) or (self.collapsedRootItems is not None and len(self.collapsedRootItems.getItems()) > 0) and self.getElement().getStyle().getProperty('width') is not None and self.moreItem is not None
            ):
                # Measure the width of the "more" item
                morePresent = self.getItems().contains(self.moreItem)
                self.addItem(self.moreItem)
                moreItemWidth = self.moreItem.getOffsetWidth()
                if not morePresent:
                    self.removeItem(self.moreItem)
                # Measure available space
                if self._paddingWidth == -1:
                    widthBefore = self.getElement().getClientWidth()
                    self.getElement().getStyle().setProperty('padding', '0')
                    self._paddingWidth = widthBefore - self.getElement().getClientWidth()
                    self.getElement().getStyle().setProperty('padding', '')
                overflow = ''
                if BrowserInfo.get().isIE6():
                    # IE6 cannot measure available width correctly without
                    # overflow:hidden
                    overflow = self.getElement().getStyle().getProperty('overflow')
                    self.getElement().getStyle().setProperty('overflow', 'hidden')
                availableWidth = self.getElement().getClientWidth() - self._paddingWidth
                if BrowserInfo.get().isIE6():
                    # IE6 cannot measure available width correctly without
                    # overflow:hidden
                    self.getElement().getStyle().setProperty('overflow', overflow)
                # Used width includes the "more" item if present
                usedWidth = self.getConsumedWidth()
                diff = availableWidth - usedWidth
                self.removeItem(self.moreItem)
                if diff < 0:
                    # Too many items: collapse last items from root menu
                    widthNeeded = usedWidth - availableWidth
                    if not morePresent:
                        widthNeeded += moreItemWidth
                    widthReduced = 0
                    while widthReduced < widthNeeded and len(self.getItems()) > 0:
                        # Move last root menu item to collapsed menu
                        collapse = self.getItems().get(len(self.getItems()) - 1)
                        widthReduced += collapse.getOffsetWidth()
                        self.removeItem(collapse)
                        self.collapsedRootItems.addItem(collapse, 0)
                elif len(self.collapsedRootItems.getItems()) > 0:
                    # Space available for items: expand first items from collapsed
                    # menu
                    widthAvailable = diff + moreItemWidth
                    widthGrowth = 0
                    while (
                        widthAvailable > widthGrowth and len(self.collapsedRootItems.getItems()) > 0
                    ):
                        # Move first item from collapsed menu to the root menu
                        expand = self.collapsedRootItems.getItems().get(0)
                        self.collapsedRootItems.removeItem(expand)
                        self.addItem(expand)
                        widthGrowth += expand.getOffsetWidth()
                        if len(self.collapsedRootItems.getItems()) > 0:
                            widthAvailable -= moreItemWidth
                        if widthGrowth > widthAvailable:
                            self.removeItem(expand)
                            self.collapsedRootItems.addItem(expand, 0)
                        else:
                            widthAvailable = diff
                        if BrowserInfo.get().isIE6():
                            # Handle transparency for IE6 here as we cannot
                            # implement it in CustomMenuItem.onAttach because
                            # onAttach is never called for CustomMenuItem due to an
                            # invalid component hierarchy (#6203)...

                            self.reloadImages(expand.getElement())
                if len(self.collapsedRootItems.getItems()) > 0:
                    self.addItem(self.moreItem)
            # If a popup is open we might need to adjust the shadow as well if an
            # icon shown in that popup was loaded
            if self.popup is not None:
                # Forces a recalculation of the shadow size
                self.popup.show()
            if iconLoadEvent:
                # Size have changed if the width is undefined
                Util.notifyParentOfSizeChange(self, False)
        else:
            raise ARGERROR(0, 1)

    # Only collapse if there is more than one item in the root menu and the
    # menu has an explicit size

    def getConsumedWidth(self):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.KeyPressHandler#onKeyPress(com.google
        # .gwt.event.dom.client.KeyPressEvent)

        w = 0
        for item in self.getItems():
            if not self.collapsedRootItems.getItems().contains(item):
                w += item.getOffsetWidth()
        return w

    def onKeyPress(self, event):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.KeyDownHandler#onKeyDown(com.google.gwt
        # .event.dom.client.KeyDownEvent)

        if (
            self.handleNavigation(event.getNativeEvent().getKeyCode(), event.isControlKeyDown() or event.isMetaKeyDown(), event.isShiftKeyDown())
        ):
            event.preventDefault()

    def onKeyDown(self, event):
        if (
            self.handleNavigation(event.getNativeEvent().getKeyCode(), event.isControlKeyDown() or event.isMetaKeyDown(), event.isShiftKeyDown())
        ):
            event.preventDefault()

    def getNavigationUpKey(self):
        """Get the key that moves the selection upwards. By default it is the up
        arrow key but by overriding this you can change the key to whatever you
        want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_UP

    def getNavigationDownKey(self):
        """Get the key that moves the selection downwards. By default it is the down
        arrow key but by overriding this you can change the key to whatever you
        want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_DOWN

    def getNavigationLeftKey(self):
        """Get the key that moves the selection left. By default it is the left
        arrow key but by overriding this you can change the key to whatever you
        want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_LEFT

    def getNavigationRightKey(self):
        """Get the key that moves the selection right. By default it is the right
        arrow key but by overriding this you can change the key to whatever you
        want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_RIGHT

    def getNavigationSelectKey(self):
        """Get the key that selects a menu item. By default it is the Enter key but
        by overriding this you can change the key to whatever you want.

        @return
        """
        return self.KeyCodes.KEY_ENTER

    def getCloseMenuKey(self):
        """Get the key that closes the menu. By default it is the escape key but by
        overriding this yoy can change the key to whatever you want.

        @return
        """
        return self.KeyCodes.KEY_ESCAPE

    def handleNavigation(self, keycode, ctrl, shift):
        """Handles the keyboard events handled by the MenuBar

        @param event
                   The keyboard event received
        @return true iff the navigation event was handled
        """
        # If tab or shift+tab close menus
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.FocusHandler#onFocus(com.google.gwt.event
        # .dom.client.FocusEvent)

        if keycode == self.KeyCodes.KEY_TAB:
            self.setSelected(None)
            self.hideChildren()
            self.menuVisible = False
            return False
        if (ctrl or shift) or (not self.isEnabled()):
            # Do not handle tab key, nor ctrl keys
            return False
        if keycode == self.getNavigationLeftKey():
            if self.getSelected() is None:
                # If nothing is selected then select the last item
                self.setSelected(self.items[len(self.items) - 1])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            elif self.visibleChildMenu is None and self.getParentMenu() is None:
                # If this is the root menu then move to the right
                idx = self.items.index(self.getSelected())
                if idx > 0:
                    self.setSelected(self.items[idx - 1])
                else:
                    self.setSelected(self.items[len(self.items) - 1])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            elif self.visibleChildMenu is not None:
                # Redirect all navigation to the submenu
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
            elif self.getParentMenu().getParentMenu() is None:
                # Get the root menu
                root = self.getParentMenu()
                root.getSelected().getSubMenu().setSelected(None)
                root.hideChildren()
                # Get the root menus items and select the previous one
                idx = root.getItems().index(root.getSelected())
                idx = idx if idx > 0 else len(root.getItems())
                selected = root.getItems().get(PREDEC(globals(), locals(), 'idx'))
                while selected.isSeparator() or (not selected.isEnabled()):
                    idx = idx if idx > 0 else len(root.getItems())
                    selected = root.getItems().get(PREDEC(globals(), locals(), 'idx'))
                root.setSelected(selected)
                root.showChildMenu(selected)
                submenu = selected.getSubMenu()
                # Select the first item in the newly open submenu
                submenu.setSelected(submenu.getItems().get(0))
            else:
                self.getParentMenu().getSelected().getSubMenu().setSelected(None)
                self.getParentMenu().hideChildren()
            return True
        elif keycode == self.getNavigationRightKey():
            if self.getSelected() is None:
                # If nothing is selected then select the first item
                self.setSelected(self.items[0])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            elif self.visibleChildMenu is None and self.getParentMenu() is None:
                # If this is the root menu then move to the right
                idx = self.items.index(self.getSelected())
                if idx < len(self.items) - 1:
                    self.setSelected(self.items[idx + 1])
                else:
                    self.setSelected(self.items[0])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            elif (
                self.visibleChildMenu is None and self.getSelected().getSubMenu() is not None
            ):
                # If the item has a submenu then show it and move the selection
                # there
                self.showChildMenu(self.getSelected())
                self.menuVisible = True
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
            elif self.visibleChildMenu is None:
                # Get the root menu
                root = self.getParentMenu()
                while root.getParentMenu() is not None:
                    root = root.getParentMenu()
                # Hide the submenu
                root.hideChildren()
                # Get the root menus items and select the next one
                idx = root.getItems().index(root.getSelected())
                idx = idx if idx < len(root.getItems()) - 1 else -1
                selected = root.getItems().get(PREINC(globals(), locals(), 'idx'))
                while selected.isSeparator() or (not selected.isEnabled()):
                    idx = idx if idx < len(root.getItems()) - 1 else -1
                    selected = root.getItems().get(PREINC(globals(), locals(), 'idx'))
                root.setSelected(selected)
                root.showChildMenu(selected)
                submenu = selected.getSubMenu()
                # Select the first item in the newly open submenu
                submenu.setSelected(submenu.getItems().get(0))
            elif self.visibleChildMenu is not None:
                # Redirect all navigation to the submenu
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
            return True
        elif keycode == self.getNavigationUpKey():
            if self.getSelected() is None:
                # If nothing is selected then select the last item
                self.setSelected(self.items[len(self.items) - 1])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            elif self.visibleChildMenu is not None:
                # Redirect all navigation to the submenu
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
            else:
                # Select the previous item if possible or loop to the last item
                idx = self.items.index(self.getSelected())
                if idx > 0:
                    self.setSelected(self.items[idx - 1])
                else:
                    self.setSelected(self.items[len(self.items) - 1])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            return True
        elif keycode == self.getNavigationDownKey():
            if self.getSelected() is None:
                # If nothing is selected then select the first item
                self.setSelected(self.items[0])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            elif self.visibleChildMenu is None and self.getParentMenu() is None:
                # If this is the root menu the show the child menu with arrow
                # down
                self.showChildMenu(self.getSelected())
                self.menuVisible = True
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
            elif self.visibleChildMenu is not None:
                # Redirect all navigation to the submenu
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
            else:
                # Select the next item if possible or loop to the first item
                idx = self.items.index(self.getSelected())
                if idx < len(self.items) - 1:
                    self.setSelected(self.items[idx + 1])
                else:
                    self.setSelected(self.items[0])
                if self.getSelected().isSeparator() or (not self.getSelected().isEnabled()):
                    self.handleNavigation(keycode, ctrl, shift)
            return True
        elif keycode == self.getCloseMenuKey():
            self.setSelected(None)
            self.hideChildren()
            self.menuVisible = False
        elif keycode == self.getNavigationSelectKey():
            if self.visibleChildMenu is not None:
                # Redirect all navigation to the submenu
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
                self.menuVisible = False
            elif (
                self.visibleChildMenu is None and self.getSelected().getSubMenu() is not None
            ):
                # If the item has a submenu then show it and move the selection
                # there
                self.showChildMenu(self.getSelected())
                self.menuVisible = True
                self.visibleChildMenu.handleNavigation(keycode, ctrl, shift)
            else:
                command = self.getSelected().getCommand()
                if command is not None:
                    command.execute()
                self.setSelected(None)
                self.hideParents(True)
        return False

    def onFocus(self, event):
        pass

    _SUBPART_PREFIX = 'item'

    def getSubPartElement(self, subPart):
        index = int(subPart[len(self._SUBPART_PREFIX):])
        item = self.getItems().get(index)
        return item.getElement()

    def getSubPartName(self, subElement):
        if not self.getElement().isOrHasChild(subElement):
            return None
        menuItemRoot = subElement
        while (
            menuItemRoot is not None and menuItemRoot.getParentElement() is not None and menuItemRoot.getParentElement() != self.getElement()
        ):
            menuItemRoot = menuItemRoot.getParentElement()
        # "menuItemRoot" is now the root of the menu item
        itemCount = len(self.getItems())
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < itemCount):
                break
            if self.getItems().get(i).getElement() == menuItemRoot:
                name = self._SUBPART_PREFIX + i
                return name
        return None

    def onLoad(self):
        super(VMenuBar, self).onLoad()
        if BrowserInfo.get().isIE6():
            self.reloadImages(self.getElement())

    def reloadImages(self, root):
        """Force a new onload event for all images. Used only for IE6 to deal with
        PNG transparency.
        """
        imgElements = root.getElementsByTagName('img')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < imgElements.getLength()):
                break
            e = imgElements.getItem(i)
            # IE6 fires onload events for the icons before the listener
            # is attached (or never). Updating the src force another
            # onload event
            src = e.getAttribute('src')
            e.setAttribute('src', src)
