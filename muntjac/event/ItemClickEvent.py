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

from muntjac.event.MouseEvents import ClickEvent


class ItemClickListener(object):

    def itemClick(self, event):
        pass


class ItemClickEvent(ClickEvent):
    """Click event fired by a {@link Component} implementing
    {@link com.vaadin.data.Container} interface. ItemClickEvents happens on an
    {@link Item} rendered somehow on terminal. Event may also contain a specific
    {@link Property} on which the click event happened.

    @since 5.3
    """

    def __init__(self, source, item, itemId, propertyId, details):
        super(ItemClickEvent, self)(source, details)
        self._item = item
        self._itemId = itemId
        self._propertyId = propertyId


    def getItem(self):
        """Gets the item on which the click event occurred.

        @return item which was clicked
        """
        return self._item


    def getItemId(self):
        """Gets a possible identifier in source for clicked Item

        @return
        """
        return self._itemId


    def getPropertyId(self):
        """Returns property on which click event occurred. Returns null if source
        cannot be resolved at property leve. For example if clicked a cell in
        table, the "column id" is returned.

        @return a property id of clicked property or null if click didn't occur
                on any distinct property.
        """
        return self._propertyId

    ITEM_CLICK_METHOD = getattr(ItemClickListener, 'itemClick')


class ItemClickNotifier(object):
    """The interface for adding and removing <code>ItemClickEvent</code>
    listeners. By implementing this interface a class explicitly announces
    that it will generate an <code>ItemClickEvent</code> when one of its
    items is clicked.
    <p>
    Note: The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>

    @since 6.5
    @see ItemClickListener
    @see ItemClickEvent
    """

    def addListener(self, listener):
        """Register a listener to handle {@link ItemClickEvent}s.

        @param listener
                   ItemClickListener to be registered
        """
        pass


    def removeListener(self, listener):
        """Removes an ItemClickListener.

        @param listener
                   ItemClickListener to be removed
        """
        pass


class ItemClickSource(ItemClickNotifier):
    """Components implementing

    @link {@link Container} interface may support emitting
          {@link ItemClickEvent}s.

    @deprecated Use {@link ItemClickNotifier} instead. ItemClickSource was
                deprecated in version 6.5.
    """
    pass