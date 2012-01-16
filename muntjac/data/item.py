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

"""Provides a mechanism for handling a set of Properties."""


class IItem(object):
    """Provides a mechanism for handling a set of Properties, each associated
    to a locally unique non-null identifier. The interface is split into
    subinterfaces to enable a class to implement only the functionalities it
    needs.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def getItemProperty(self, idd):
        """Gets the Property corresponding to the given Property ID stored in
        the IItem. If the IItem does not contain the Property, C{None} is
        returned.

        @param idd:
                   identifier of the Property to get
        @return: the Property with the given ID or C{None}
        """
        raise NotImplementedError


    def getItemPropertyIds(self):
        """Gets the collection of IDs of all Properties stored in the IItem.

        @return: iterable containing IDs of the Properties stored
                the IItem
        """
        raise NotImplementedError


    def addItemProperty(self, idd, prop):
        """Tries to add a new Property into the IItem.

        This functionality is optional.

        @param idd:
                   ID of the new Property
        @param prop:
                   the Property to be added and associated with the id
        @return: C{True} if the operation succeeded, C{False}
                if not
        @raise NotImplementedError:
                    if the operation is not supported.
        """
        raise NotImplementedError


    def removeItemProperty(self, idd):
        """Removes the Property identified by ID from the IItem.

        This functionality is optional.

        @param idd:
                   ID of the Property to be removed
        @return: C{True} if the operation succeeded C{False} if not
        @raise NotImplementedError:
                    if the operation is not supported.
        """
        raise NotImplementedError


class IViewer(object):
    """Interface implemented by viewer classes capable of using an IItem as a
    data source.
    """

    def setItemDataSource(self, newDataSource):
        """Sets the IItem that serves as the data source of the viewer.

        @param newDataSource:
                   The new data source IItem
        """
        raise NotImplementedError


    def getItemDataSource(self):
        """Gets the IItem serving as the data source of the viewer.

        @return: data source IItem
        """
        raise NotImplementedError


class IEditor(IViewer):
    """Interface implemented by the C{IEditor} classes capable of editing the
    IItem. Implementing this interface means that the IItem serving as the
    data source of the editor can be modified through it.

    Note: Not implementing the C{IEditor} interface does not restrict the class
    from editing the contents of an internally.
    """
    pass


class IPropertySetChangeEvent(object):
    """An C{Event} object specifying the IItem whose contents has been
    changed through the C{Property} interface.

    Note: The values stored in the Properties may change without triggering
    this event.
    """

    def getItem(self):
        """Retrieves the IItem whose contents has been modified.

        @return: source IItem of the event
        """
        raise NotImplementedError


class IPropertySetChangeListener(object):
    """The listener interface for receiving C{IPropertySetChangeEvent}
    objects.
    """

    def itemPropertySetChange(self, event):
        """Notifies this listener that the IItem's property set has changed.

        @param event:
                   Property set change event object
        """
        raise NotImplementedError


class IPropertySetChangeNotifier(object):
    """The interface for adding and removing C{IPropertySetChangeEvent}
    listeners. By implementing this interface a class explicitly announces
    that it will generate a C{IPropertySetChangeEvent} when its
    Property set is modified.
    """

    def addListener(self, listener, iface=None):
        """Registers a new property set change listener for this IItem.

        @param listener:
                   The new Listener to be registered.
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Removes a previously registered property set change listener.

        @param listener:
                   Listener to be removed.
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError
