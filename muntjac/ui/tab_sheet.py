# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Defines a tab sheet component."""

from warnings import warn

from muntjac.terminal.key_mapper import KeyMapper
from muntjac.terminal.paintable import IRepaintRequestListener,\
    RepaintRequestEvent

from muntjac.ui.component import IComponent, Event as ComponentEvent
from muntjac.ui.abstract_component_container import AbstractComponentContainer

from muntjac.terminal.gwt.server.communication_manager import \
    CommunicationManager


class ISelectedTabChangeListener(object):
    """Selected tab change event listener. The listener is called whenever
    another tab is selected, including when adding the first tab to a
    tabsheet.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def selectedTabChange(self, event):
        """Selected (shown) tab in tab sheet has has been changed.

        @param event: the selected tab change event.
        """
        raise NotImplementedError


_SELECTED_TAB_CHANGE_METHOD = getattr(ISelectedTabChangeListener,
        'selectedTabChange')


class TabSheet(AbstractComponentContainer):
    """TabSheet component.

    Tabs are typically identified by the component contained on the tab (see
    L{ComponentContainer}), and tab metadata (including caption, icon,
    visibility, enabledness, closability etc.) is kept in separate {@link
    ITab} instances.

    Tabs added with L{addComponent} get the caption and the
    icon of the component at the time when the component is created, and these
    are not automatically updated after tab creation.

    A tab sheet can have multiple tab selection listeners and one tab close
    handler (L{ICloseHandler}), which by default removes the tab from the
    TabSheet.

    The L{TabSheet} can be styled with the .v-tabsheet, .v-tabsheet-tabs
    and .v-tabsheet-content styles. Themes may also have pre-defined
    variations of the tab sheet presentation, such as
    L{Reindeer.TABSHEET_BORDERLESS}, L{Runo.TABSHEET_SMALL} and
    several other styles in L{Reindeer}.

    The current implementation does not load the tabs to the UI before the
    first time they are shown, but this may change in future releases.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VTabsheet, LoadStyle.EAGER)

    def __init__(self):
        """Constructs a new Tabsheet. Tabsheet is immediate by default, and
        the default close handler removes the tab being closed.
        """
        super(TabSheet, self).__init__()

        #: List of component tabs (tab contents). In addition to being on this
        #  list, there is a L{ITab} object in tabs for each tab with
        #  meta-data about the tab.
        self._components = list()

        #: Map containing information related to the tabs (caption, icon etc).
        self._tabs = dict()

        #: Selected tab content component.
        self._selected = None

        #: Mapper between server-side component instances (tab contents) and
        #  keys given to the client that identify tabs.
        self._keyMapper = KeyMapper()

        #: When true, the tab selection area is not displayed to the user.
        self._tabsHidden = None

        #: Tabs that have been shown to the user (have been painted as
        #  selected).
        self._paintedTabs = set()

        #: Handler to be called when a tab is closed.
        self._closeHandler = None

        #: expand horizontally by default
        self.setWidth(100.0, self.UNITS_PERCENTAGE)
        self.setImmediate(True)

        self.setCloseHandler(InnerHandler())


    def getComponentIterator(self):
        """Gets the component container iterator for going through all the
        components (tab contents).

        @return: the unmodifiable Iterator of the tab content components
        """
        return iter(self._components)


    def getComponentCount(self):
        """Gets the number of contained components (tabs). Consistent with
        the iterator returned by L{getComponentIterator}.

        @return: the number of contained components
        """
        return len(self._components)


    def removeComponent(self, c):
        """Removes a component and its corresponding tab.

        If the tab was selected, the first eligible (visible and enabled)
        remaining tab is selected.

        @param c: the component to be removed.
        """
        if c is not None and c in self._components:
            super(TabSheet, self).removeComponent(c)
            self._keyMapper.remove(c)
            self._components.remove(c)
            if c in self._tabs:
                del self._tabs[c]
            if c == self._selected:
                if len(self._components) == 0:
                    self._selected = None
                else:
                    # select the first enabled and visible tab, if any
                    self.updateSelection()
                    self.fireSelectedTabChange()

            self.requestRepaint()


    def removeTab(self, tab):
        """Removes a L{ITab} and the component associated with it, as
        previously added with L{addTab}, or L{addComponent}.

        If the tab was selected, the first eligible (visible and enabled)
        remaining tab is selected.

        @see: L{addTab}
        @see: L{addComponent}
        @see: L{removeComponent}
        @param tab: the ITab to remove
        """
        self.removeComponent(tab.getComponent())


    def addComponent(self, c):
        """Adds a new tab into TabSheet. IComponent caption and icon are
        copied to the tab metadata at creation time.

        @see: L{addTab}
        @param c: the component to be added.
        """
        self.addTab(c)


    def addTab(self, *args):
        """Adds a new tab into TabSheet.

        The first tab added to a tab sheet is automatically selected and a
        tab selection event is fired.

        If the component is already present in the tab sheet, changes its
        caption and icon and returns the corresponding (old) tab, preserving
        other tab metadata.

        @param args: tuple of the form
            - (c, caption, icon)
              1. the component to be added onto tab - should not be null.
              2. the caption to be set for the component and used rendered
                 in tab bar
              3. the icon to be set for the component and used rendered in
                 tab bar
            - (c, caption, icon, position)
              1. the component to be added onto tab - should not be null.
              2. the caption to be set for the component and used rendered
                 in tab bar
              3. the icon to be set for the component and used rendered in
                 tab bar
              4. the position at where the the tab should be added
            - (c)
              1. the component to be added onto tab - should not be null.
            - (c, position)
              1. the component to be added onto tab - should not be null.
              2. The position where the tab should be added
            - (c, caption)
              1. the component to be added onto tab - should not be null.
              2. the caption to be set for the component and used rendered
                 in tab bar

        @return: the created L{ITab}
        """
        nargs = len(args)
        if nargs == 1:
            c, = args
            return self.addTab(c, len(self._components))
        elif nargs == 2:
            if isinstance(args[1], basestring):
                c, caption = args
                self.addTab(c, caption, None)
            else:
                c, position = args
                if c is None:
                    return None
                elif c in self._tabs:
                    return self._tabs.get(c)
                else:
                    return self.addTab(c, c.getCaption(), c.getIcon(), position)
        elif nargs == 3:
            c, caption, icon = args
            return self.addTab(c, caption, icon, len(self._components))
        elif nargs == 4:
            c, caption, icon, position = args
            if c is None:
                return None
            elif c in self._tabs:
                tab = self._tabs.get(c)
                tab.setCaption(caption)
                tab.setIcon(icon)
                return tab
            else:
                self._components.insert(position, c)
                tab = TabSheetTabImpl(caption, icon, self)
                self._tabs[c] = tab
                if self._selected is None:
                    self._selected = c
                    self.fireSelectedTabChange()
                super(TabSheet, self).addComponent(c)
                self.requestRepaint()
                return tab
        else:
            raise ValueError, 'invalid number of arguments'


    def moveComponentsFrom(self, source):
        """Moves all components from another container to this container. The
        components are removed from the other container.

        If the source container is a L{TabSheet}, component captions and
        icons are copied from it.

        @param source:
                   the container components are removed from.
        """
        i = source.getComponentIterator()
        while True:
            try:
                c = i.next()
                caption = None
                icon = None
                if issubclass(source.__class__, TabSheet):
                    caption = source.getTabCaption(c)
                    icon = source.getTabIcon(c)
                source.removeComponent(c)
                self.addTab(c, caption, icon)
            except StopIteration:
                break


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the paint target
        @raise PaintException:
                    if the paint operation failed.
        """
        if self.areTabsHidden():
            target.addAttribute('hidetabs', True)

        target.startTag('tabs')

        orphaned = set(self._paintedTabs)

        i = self.getComponentIterator()
        while True:
            try:
                component = i.next()
                if component in orphaned:
                    orphaned.remove(component)
                tab = self._tabs.get(component)
                target.startTag('tab')
                if not tab.isEnabled() and tab.isVisible():
                    target.addAttribute('disabled', True)

                if not tab.isVisible():
                    target.addAttribute('hidden', True)

                if tab.isClosable():
                    target.addAttribute('closable', True)

                icon = tab.getIcon()
                if icon is not None:
                    target.addAttribute('icon', icon)

                caption = tab.getCaption()
                if caption is not None and len(caption) > 0:
                    target.addAttribute('caption', caption)

                description = tab.getDescription()
                if description is not None:
                    target.addAttribute('description', description)

                componentError = tab.getComponentError()
                if componentError is not None:
                    componentError.paint(target)

                target.addAttribute('key', self._keyMapper.key(component))
                if component == self._selected:
                    target.addAttribute('selected', True)
                    component.paint(target)
                    self._paintedTabs.add(component)

                elif component in self._paintedTabs:
                    component.paint(target)
                else:
                    component.requestRepaintRequests()
                target.endTag('tab')
            except StopIteration:
                break

        target.endTag('tabs')

        if self._selected is not None:
            target.addVariable(self, 'selected',
                    self._keyMapper.key(self._selected))

        # clean possibly orphaned entries in paintedTabs
        for component2 in orphaned:
            self._paintedTabs.remove(component2)


    def areTabsHidden(self):
        """Are the tab selection parts ("tabs") hidden.

        @return: true if the tabs are hidden in the UI
        """
        return self._tabsHidden


    def hideTabs(self, tabsHidden):
        """Hides or shows the tab selection parts ("tabs").

        @param tabsHidden:
                   true if the tabs should be hidden
        """
        self._tabsHidden = tabsHidden
        self.requestRepaint()


    def getTabCaption(self, c):
        """Gets tab caption. The tab is identified by the tab content
        component.

        @param c: the component in the tab
        @deprecated: Use L{getTab} and L{ITab.getCaption} instead.
        """
        warn('use getTab() and ITab.getCaption() instead', DeprecationWarning)

        info = self._tabs.get(c)
        if info is None:
            return ''
        else:
            return info.getCaption()


    def setTabCaption(self, c, caption):
        """Sets tab caption. The tab is identified by the tab content
        component.

        @param c: the component in the tab
        @param caption: the caption to set.
        @deprecated: Use L{getTab} and L{ITab.setCaption} instead.
        """
        warn('use getTab() and ITab.getCaption() instead', DeprecationWarning)

        info = self._tabs.get(c)
        if info is not None:
            info.setCaption(caption)
            self.requestRepaint()


    def getTabIcon(self, c):
        """Gets the icon for a tab. The tab is identified by the tab content
        component.

        @param c: the component in the tab
        @deprecated: Use L{getTab} and L{ITab.getIcon} instead.
        """
        warn('use getTab() and ITab.getIcon() instead', DeprecationWarning)

        info = self._tabs.get(c)
        if info is None:
            return None
        else:
            return info.getIcon()


    def setTabIcon(self, c, icon):
        """Sets icon for the given component. The tab is identified by the
        tab content component.

        @param c:
                   the component in the tab
        @param icon:
                   the icon to set
        @deprecated: Use L{getTab} and L{ITab.setIcon} instead.
        """
        warn('use getTab() and ITab.getIcon() instead', DeprecationWarning)

        info = self._tabs.get(c)
        if info is not None:
            info.setIcon(icon)
            self.requestRepaint()


    def getTab(self, arg):
        """Returns the L{ITab} (metadata) for a component. The
        L{ITab} object can be used for setting caption,icon, etc
        for the tab.

        @param arg:
                   the component or the position of the tab
        """
        if isinstance(arg, IComponent):
            c = arg
            return self._tabs.get(c)
        else:
            position = arg
            c = self._components[position]
            if c is not None:
                return self._tabs.get(c)
            return None


    def setSelectedTab(self, c):
        """Sets the selected tab. The tab is identified by the tab content
        component.
        """
        if (c is not None and c in self._components
                and c != self._selected):
            self._selected = c
            self.updateSelection()
            self.fireSelectedTabChange()
            self.requestRepaint()


    def updateSelection(self):
        """Checks if the current selection is valid, and updates the selection
        if the previously selected component is not visible and enabled. The
        first visible and enabled tab is selected if the current selection is
        empty or invalid.

        This method does not fire tab change events, but the caller should do
        so if appropriate.

        @return: true if selection was changed, false otherwise
        """
        originalSelection = self._selected

        i = self.getComponentIterator()
        while True:
            try:
                component = i.next()
                tab = self._tabs.get(component)
                # If we have no selection, if the current selection is
                # invisible or if the current selection is disabled (but
                # the whole component is not) we select this tab instead
                selectedTabInfo = None
                if self._selected is not None:
                    selectedTabInfo = self._tabs.get(self._selected)

                if (self._selected is None
                        or selectedTabInfo is None
                        or not selectedTabInfo.isVisible()
                        or not selectedTabInfo.isEnabled()):
                    # The current selection is not valid so we need to
                    # change it
                    if tab.isEnabled() and tab.isVisible():
                        self._selected = component
                        break
                    else:
                        # The current selection is not valid but this
                        # tab cannot be selected either.
                        self._selected = None
            except StopIteration:
                break

        return originalSelection != self._selected


    def getSelectedTab(self):
        """Gets the selected tab content component.

        @return: the selected tab contents
        """
        return self._selected


    def changeVariables(self, source, variables):
        if 'selected' in variables:
            select = self._keyMapper.get(variables.get('selected'))
            self.setSelectedTab(select)

        if 'close' in variables:
            tab = self._keyMapper.get(variables.get('close'))

            if tab is not None:
                self._closeHandler.onTabClose(self, tab)


    def replaceComponent(self, oldComponent, newComponent):
        """Replaces a component (tab content) with another. This can be used
        to change tab contents or to rearrange tabs. The tab position and some
        metadata are preserved when moving components within the same
        L{TabSheet}.

        If the oldComponent is not present in the tab sheet, the new one is
        added at the end.

        If the oldComponent is already in the tab sheet but the newComponent
        isn't, the old tab is replaced with a new one, and the caption and
        icon of the old one are copied to the new tab.

        If both old and new components are present, their positions are
        swapped.
        """
        if self._selected == oldComponent:
            # keep selection w/o selectedTabChange event
            self._selected = newComponent

        newTab = self._tabs.get(newComponent)
        oldTab = self._tabs.get(oldComponent)

        # Gets the captions
        oldCaption = None
        oldIcon = None
        newCaption = None
        newIcon = None

        if oldTab is not None:
            oldCaption = oldTab.getCaption()
            oldIcon = oldTab.getIcon()

        if newTab is not None:
            newCaption = newTab.getCaption()
            newIcon = newTab.getIcon()
        else:
            newCaption = newComponent.getCaption()
            newIcon = newComponent.getIcon()

        # Gets the locations
        oldLocation = -1
        newLocation = -1
        location = 0
        for component in self._components:
            if component == oldComponent:
                oldLocation = location
            if component == newComponent:
                newLocation = location
            location += 1

        if oldLocation == -1:
            self.addComponent(newComponent)
        elif newLocation == -1:
            self.removeComponent(oldComponent)
            self._keyMapper.remove(oldComponent)
            newTab = self.addTab(newComponent)
            self._components.remove(newComponent)
            self._components.append(oldLocation, newComponent)
            newTab.setCaption(oldCaption)
            newTab.setIcon(oldIcon)
        else:
            if oldLocation > newLocation:
                self._components.remove(oldComponent)
                self._components.append(newLocation, oldComponent)
                self._components.remove(newComponent)
                self._components.append(oldLocation, newComponent)
            else:
                self._components.remove(newComponent)
                self._components.append(oldLocation, newComponent)
                self._components.remove(oldComponent)
                self._components.append(newLocation, oldComponent)

            if newTab is not None:
                # This should always be true
                newTab.setCaption(oldCaption)
                newTab.setIcon(oldIcon)

            if oldTab is not None:
                # This should always be true
                oldTab.setCaption(newCaption)
                oldTab.setIcon(newIcon)

            self.requestRepaint()


    def addListener(self, listener, iface=None):
        """Adds a tab selection listener

        @param listener:
                   the Listener to be added.
        """
        if (isinstance(listener, ISelectedTabChangeListener) and
                (iface is None or
                        issubclass(iface, ISelectedTabChangeListener))):
            self.registerListener(SelectedTabChangeEvent,
                    listener, _SELECTED_TAB_CHANGE_METHOD)

        super(TabSheet, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, SelectedTabChangeEvent):
            self.registerCallback(SelectedTabChangeEvent, callback, None,
                    *args)
        else:
            super(TabSheet, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes a tab selection listener

        @param listener:
                   the Listener to be removed.
        """
        if (isinstance(listener, IRepaintRequestListener) and
                (iface is None or issubclass(iface, IRepaintRequestListener))):
            super(TabSheet, self).removeListener(listener, iface)
            if isinstance(listener, CommunicationManager):
                # clean the paintedTabs here instead of detach to avoid subtree
                # caching issues when detached-attached without render
                self._paintedTabs.clear()

        if (isinstance(listener, ISelectedTabChangeListener) and
                (iface is None or
                        issubclass(iface, ISelectedTabChangeListener))):
            self.withdrawListener(SelectedTabChangeEvent,
                    listener, _SELECTED_TAB_CHANGE_METHOD)

        super(TabSheet, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, SelectedTabChangeEvent):
            self.withdrawCallback(SelectedTabChangeEvent, callback)
        else:
            super(TabSheet, self).removeCallback(callback, eventType)


    def fireSelectedTabChange(self):
        """Sends an event that the currently selected tab has changed."""
        event = SelectedTabChangeEvent(self)
        self.fireEvent(event)


    def setCloseHandler(self, handler):
        """Provide a custom L{ICloseHandler} for this TabSheet if you
        wish to perform some additional tasks when a user clicks on a tabs
        close button, e.g. show a confirmation dialogue before removing the
        tab.

        To remove the tab, if you provide your own close handler, you must
        call L{removeComponent} yourself.

        The default ICloseHandler for TabSheet will only remove the tab.
        """
        self._closeHandler = handler


    def setTabPosition(self, tab, position):
        """Sets the position of the tab.

        @param tab:
                   The tab
        @param position:
                   The new position of the tab
        """
        oldPosition = self.getTabPosition(tab)
        self._components.remove(oldPosition)
        self._components.append(position, tab.getComponent())
        self.requestRepaint()


    def getTabPosition(self, tab):
        """Gets the position of the tab

        @param tab: The tab
        """
        try:
            return self._components.index( tab.getComponent() )
        except ValueError:
            return -1


class SelectedTabChangeEvent(ComponentEvent):
    """Selected tab change event. This event is sent when the selected
    (shown) tab in the tab sheet is changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source):
        """New instance of selected tab change event

        @param source:
                   the Source of the event.
        """
        super(SelectedTabChangeEvent, self).__init__(source)


    def getTabSheet(self):
        """TabSheet where the event occurred.

        @return: the Source of the event.
        """
        return self.getSource()


class ITab(object):
    """ITab meta-data for a component in a L{TabSheet}.

    The meta-data includes the tab caption, icon, visibility and enabledness,
    closability, description (tooltip) and an optional component error shown
    in the tab.

    Tabs are identified by the component contained on them in most cases, and
    the meta-data can be obtained with L{TabSheet.getTab}.
    """

    def isVisible(self):
        """Returns the visible status for the tab. An invisible tab is not
        shown in the tab bar and cannot be selected.

        @return: true for visible, false for hidden
        """
        raise NotImplementedError


    def setVisible(self, visible):
        """Sets the visible status for the tab. An invisible tab is not shown
        in the tab bar and cannot be selected, selection is changed
        automatically when there is an attempt to select an invisible tab.

        @param visible:
                   true for visible, false for hidden
        """
        raise NotImplementedError


    def isClosable(self):
        """Returns the closability status for the tab.

        @return: true if the tab is allowed to be closed by the end user,
                 false for not allowing closing
        """
        raise NotImplementedError


    def setClosable(self, closable):
        """Sets the closability status for the tab. A closable tab can be
        closed by the user through the user interface. This also controls
        if a close button is shown to the user or not.

        Note! Currently only supported by TabSheet, not Accordion.

        @param closable:
                   true if the end user is allowed to close the tab, false
                   for not allowing to close. Should default to false.
        """
        raise NotImplementedError


    def isEnabled(self):
        """Returns the enabled status for the tab. A disabled tab is shown as
        such in the tab bar and cannot be selected.

        @return: true for enabled, false for disabled
        """
        raise NotImplementedError


    def setEnabled(self, enabled):
        """Sets the enabled status for the tab. A disabled tab is shown as
        such in the tab bar and cannot be selected.

        @param enabled:
                   true for enabled, false for disabled
        """
        raise NotImplementedError


    def setCaption(self, caption):
        """Sets the caption for the tab.

        @param caption:
                   the caption to set
        """
        raise NotImplementedError


    def getCaption(self):
        """Gets the caption for the tab."""
        raise NotImplementedError


    def getIcon(self):
        """Gets the icon for the tab."""
        raise NotImplementedError


    def setIcon(self, icon):
        """Sets the icon for the tab.

        @param icon:
                   the icon to set
        """
        raise NotImplementedError


    def getDescription(self):
        """Gets the description for the tab. The description can be used to
        briefly describe the state of the tab to the user, and is typically
        shown as a tooltip when hovering over the tab.

        @return: the description for the tab
        """
        raise NotImplementedError


    def setDescription(self, description):
        """Sets the description for the tab. The description can be used to
        briefly describe the state of the tab to the user, and is typically
        shown as a tooltip when hovering over the tab.

        @param description:
                   the new description string for the tab.
        """
        raise NotImplementedError


    def setComponentError(self, componentError):
        """Sets an error indicator to be shown in the tab. This can be used
        e.g. to communicate to the user that there is a problem in the
        contents of the tab.

        @see: L{AbstractComponent.setComponentError}

        @param componentError:
                   error message or null for none
        """
        raise NotImplementedError


    def getComponentError(self):
        """Gets the curent error message shown for the tab.

        @see: L{AbstractComponent.setComponentError}

        @return: message or null if none
        """
        raise NotImplementedError


    def getComponent(self):
        """Get the component related to the ITab"""
        raise NotImplementedError


class TabSheetTabImpl(ITab):
    """TabSheet's implementation of L{ITab} - tab metadata."""

    def __init__(self, caption, icon, sheet):
        self._sheet = sheet

        self._enabled = True
        self._visible = True
        self._closable = False
        self._description = None
        self._componentError = None

        if caption is None:
            caption = ''
        self._caption = caption
        self._icon = icon


    def getCaption(self):
        """Returns the tab caption. Can never be null."""
        return self._caption


    def setCaption(self, caption):
        self._caption = caption
        self._sheet.requestRepaint()


    def getIcon(self):
        return self._icon


    def setIcon(self, icon):
        self._icon = icon
        self._sheet.requestRepaint()


    def isEnabled(self):
        return self._enabled


    def setEnabled(self, enabled):
        self._enabled = enabled
        if self._sheet.updateSelection():
            self._sheet.fireSelectedTabChange()
        self._sheet.requestRepaint()


    def isVisible(self):
        return self._visible


    def setVisible(self, visible):
        self._visible = visible
        if self._sheet.updateSelection():
            self._sheet.fireSelectedTabChange()
        self._sheet.requestRepaint()


    def isClosable(self):
        return self._closable


    def setClosable(self, closable):
        self._closable = closable
        self._sheet.requestRepaint()


    def close(self):
        pass


    def getDescription(self):
        return self._description


    def setDescription(self, description):
        self._description = description
        self._sheet.requestRepaint()


    def getComponentError(self):
        return self._componentError


    def setComponentError(self, componentError):
        self._componentError = componentError
        self._sheet.requestRepaint()


    def getComponent(self):
        for k, v in self._sheet._tabs.iteritems():
            if v == self:
                return k
        return None


class ICloseHandler(object):
    """ICloseHandler is used to process tab closing events. Default behavior
    is to remove the tab from the TabSheet.

    @author: Jouni Koivuviita / Vaadin Ltd.
    @author: Richard Lincoln
    """

    def onTabClose(self, tabsheet, tabContent):
        """Called when a user has pressed the close icon of a tab in the
        client side widget.

        @param tabsheet:
                   the TabSheet to which the tab belongs to
        @param tabContent:
                   the component that corresponds to the tab whose close
                   button was clicked
        """
        raise NotImplementedError


class InnerHandler(ICloseHandler):

    def onTabClose(self, tabsheet, c):
        tabsheet.removeComponent(c)
