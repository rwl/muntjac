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

from __pyjamas__ import (POSTDEC,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.Set import (Set,)


class VTabsheetBase(ComplexPanel, Container):
    _id = None
    _client = None
    tabKeys = list()
    activeTabIndex = 0
    disabled = None
    readonly = None
    disabledTabKeys = set()
    cachedUpdate = False

    def __init__(self, classname):
        self.setElement(self.DOM.createDiv())
        self.setStyleName(classname)

    def updateFromUIDL(self, uidl, client):
        self._client = client
        # Ensure correct implementation
        self.cachedUpdate = client.updateComponent(self, uidl, True)
        if self.cachedUpdate:
            return
        # Update member references
        self._id = uidl.getId()
        self.disabled = uidl.hasAttribute('disabled')
        # Render content
        tabs = uidl.getChildUIDL(0)
        # Paintables in the TabSheet before update
        oldPaintables = list()
        _0 = True
        iterator = self.getPaintableIterator()
        while True:
            if _0 is True:
                _0 = False
            if not iterator.hasNext():
                break
            oldPaintables.add(iterator.next())
        # Clear previous values
        self.tabKeys.clear()
        self.disabledTabKeys.clear()
        index = 0
        _1 = True
        it = tabs.getChildIterator()
        while True:
            if _1 is True:
                _1 = False
            if not it.hasNext():
                break
            tab = it.next()
            key = tab.getStringAttribute('key')
            selected = tab.getBooleanAttribute('selected')
            hidden = tab.getBooleanAttribute('hidden')
            if tab.getBooleanAttribute('disabled'):
                self.disabledTabKeys.add(key)
            self.tabKeys.add(key)
            if selected:
                self.activeTabIndex = index
            self.renderTab(tab, index, selected, hidden)
            index += 1
        tabCount = self.getTabCount()
        while POSTDEC(globals(), locals(), 'tabCount') > index:
            self.removeTab(index)
        _2 = True
        i = 0
        while True:
            if _2 is True:
                _2 = False
            else:
                i += 1
            if not (i < self.getTabCount()):
                break
            p = self.getTab(i)
            oldPaintables.remove(p)
        # Perform unregister for any paintables removed during update
        _3 = True
        iterator = oldPaintables
        while True:
            if _3 is True:
                _3 = False
            if not iterator.hasNext():
                break
            oldPaintable = iterator.next()
            if isinstance(oldPaintable, Paintable):
                w = oldPaintable
                if w.isAttached():
                    w.removeFromParent()
                client.unregisterPaintable(oldPaintable)

    def getPaintableIterator(self):
        """@return a list of currently shown Paintables

                Apparently can be something else than Paintable as
                {@link #updateFromUIDL(UIDL, ApplicationConnection)} checks if
                instanceof Paintable. Therefore set to <Object>
        """
        pass

    def clearPaintables(self):
        """Clears current tabs and contents"""
        pass

    def renderTab(self, tabUidl, index, selected, hidden):
        """Implement in extending classes. This method should render needed elements
        and set the visibility of the tab according to the 'selected' parameter.
        """
        pass

    def selectTab(self, index, contentUidl):
        """Implement in extending classes. This method should render any previously
        non-cached content and set the activeTabIndex property to the specified
        index.
        """
        pass

    def getTabCount(self):
        """Implement in extending classes. This method should return the number of
        tabs currently rendered.
        """
        pass

    def getTab(self, index):
        """Implement in extending classes. This method should return the Paintable
        corresponding to the given index.
        """
        pass

    def removeTab(self, index):
        """Implement in extending classes. This method should remove the rendered
        tab with the specified index.
        """
        pass
