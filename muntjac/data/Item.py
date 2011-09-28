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


class Item(object):
    """<p>
    Provides a mechanism for handling a set of Properties, each associated to a
    locally unique non-null identifier. The interface is split into subinterfaces
    to enable a class to implement only the functionalities it needs.
    </p>

    @author IT Mill Ltd
    @version @VERSION@
    @since 3.0
    """

    def getItemProperty(self, idd):
        """Gets the Property corresponding to the given Property ID stored in the
        Item. If the Item does not contain the Property, <code>null</code> is
        returned.

        @param id
                   identifier of the Property to get
        @return the Property with the given ID or <code>null</code>
        """
        pass


    def getItemPropertyIds(self):
        """Gets the collection of IDs of all Properties stored in the Item.

        @return unmodifiable collection containing IDs of the Properties stored
                the Item
        """
        pass


    def addItemProperty(self, idd, prop):
        """Tries to add a new Property into the Item.

        <p>
        This functionality is optional.
        </p>

        @param id
                   ID of the new Property
        @param property
                   the Property to be added and associated with the id
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        @throws UnsupportedOperationException
                    if the operation is not supported.
        """
        pass


    def removeItemProperty(self, idd):
        """Removes the Property identified by ID from the Item.

        <p>
        This functionality is optional.
        </p>

        @param id
                   ID of the Property to be removed
        @return <code>true</code> if the operation succeeded
        @throws UnsupportedOperationException
                    if the operation is not supported. <code>false</code> if not
        """
        pass


class Viewer(object):
    """Interface implemented by viewer classes capable of using an Item as a
    data source.
    """

    def setItemDataSource(self, newDataSource):
        """Sets the Item that serves as the data source of the viewer.

        @param newDataSource
                   The new data source Item
        """
        pass


    def getItemDataSource(self):
        """Gets the Item serving as the data source of the viewer.

        @return data source Item
        """
        pass


class Editor(Viewer):
    """Interface implemented by the <code>Editor</code> classes capable of
    editing the Item. Implementing this interface means that the Item serving
    as the data source of the editor can be modified through it.
    <p>
    Note : Not implementing the <code>Item.Editor</code> interface does not
    restrict the class from editing the contents of an internally.
    </p>
    """
    pass


class PropertySetChangeEvent(object):
    """An <code>Event</code> object specifying the Item whose contents has been
    changed through the <code>Property</code> interface.
    <p>
    Note: The values stored in the Properties may change without triggering
    this event.
    </p>
    """

    def getItem(self):
        """Retrieves the Item whose contents has been modified.

        @return source Item of the event
        """
        pass


class PropertySetChangeListener(object):
    """The listener interface for receiving <code>PropertySetChangeEvent</code>
    objects.
    """

    def itemPropertySetChange(self, event):
        """Notifies this listener that the Item's property set has changed.

        @param event
                   Property set change event object
        """
        pass


class PropertySetChangeNotifier(object):
    """The interface for adding and removing <code>PropertySetChangeEvent</code>
    listeners. By implementing this interface a class explicitly announces
    that it will generate a <code>PropertySetChangeEvent</code> when its
    Property set is modified.
    <p>
    Note : The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>
    """

    def addListener(self, listener):
        """Registers a new property set change listener for this Item.

        @param listener
                   The new Listener to be registered.
        """
        pass


    def removeListener(self, listener):
        """Removes a previously registered property set change listener.

        @param listener
                   Listener to be removed.
        """
        pass
