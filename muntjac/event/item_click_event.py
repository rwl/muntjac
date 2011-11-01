# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.event.mouse_events import ClickEvent


class IItemClickListener(object):

    def itemClick(self, event):
        raise NotImplementedError


ITEM_CLICK_METHOD = getattr(IItemClickListener, 'itemClick')


class ItemClickEvent(ClickEvent):
    """Click event fired by a L{Component} implementing L{IContainer}
    interface. ItemClickEvents happens on an L{IItem} rendered somehow
    on terminal. Event may also contain a specific L{Property} on which
    the click event happened.
    """

    def __init__(self, source, item, itemId, propertyId, details):
        super(ItemClickEvent, self).__init__(source, details)
        self._item = item
        self._itemId = itemId
        self._propertyId = propertyId


    def getItem(self):
        """Gets the item on which the click event occurred.

        @return: item which was clicked
        """
        return self._item


    def getItemId(self):
        """Gets a possible identifier in source for clicked Item.
        """
        return self._itemId


    def getPropertyId(self):
        """Returns property on which click event occurred. Returns C{None} if
        source cannot be resolved at property leve. For example if clicked a
        cell in table, the "column id" is returned.

        @return: a property id of clicked property or null if click didn't
                occur on any distinct property.
        """
        return self._propertyId


class IItemClickNotifier(object):
    """The interface for adding and removing C{ItemClickEvent} listeners. By
    implementing this interface a class explicitly announces that it will
    generate an C{ItemClickEvent} when one of its items is clicked.

    @see: L{ItemClickListener}
    @see: L{ItemClickEvent}
    """

    def addListener(self, listener, iface):
        """Register a listener to handle L{ItemClickEvent}s.FieldEvents,

        @param listener:
                   ItemClickListener to be registered
        """
        if iface == IItemClickListener:
            raise NotImplementedError
        else:
            super(IItemClickNotifier, self).addListener(listener, iface)


    def addItemClickListener(self, listener):
        self.addListener(listener, IItemClickListener)


    def removeListener(self, listener, iface):
        """Removes an ItemClickListener.

        @param listener:
                   ItemClickListener to be removed
        """
        if iface == IItemClickListener:
            raise NotImplementedError
        else:
            super(IItemClickNotifier, self).removeListener(listener, iface)


    def removeItemClickListener(self, listener):
        self.removeListener(listener, IItemClickListener)


class IItemClickSource(IItemClickNotifier):
    """Components implementing L{Container} interface may support emitting
    L{ItemClickEvent}s.

    @deprecated: Use L{ItemClickNotifier} instead.
    """
    pass
