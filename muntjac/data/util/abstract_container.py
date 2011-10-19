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

from muntjac.util import EventObject

from muntjac.data.container import \
    (IContainer, IItemSetChangeEvent, IPropertySetChangeEvent,
     IPropertySetChangeListener, IItemSetChangeListener)


class AbstractContainer(IContainer):
    """Abstract container class that manages event listeners and sending events to
    them ({@link PropertySetChangeNotifier}, {@link ItemSetChangeNotifier}).

    Note that this class provides the internal implementations for both types of
    events and notifiers as protected methods, but does not implement the
    {@link PropertySetChangeNotifier} and {@link ItemSetChangeNotifier}
    interfaces directly. This way, subclasses can choose not to implement them.
    Subclasses implementing those interfaces should also override the
    corresponding {@link #addListener()} and {@link #removeListener()} methods to
    make them public.

    @since 6.6
    """

    def __init__(self):
        # List of all Property set change event listeners.
        self._propertySetChangeListeners = None

        # List of all container Item set change event listeners.
        self._itemSetChangeListeners = None


    def addListener(self, listener):
        """Implementation of the corresponding method in
        {@link PropertySetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see PropertySetChangeNotifier#addListener(com.vaadin.data.IContainer.PropertySetChangeListener)
        ---
        Implementation of the corresponding method in
        {@link ItemSetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see ItemSetChangeNotifier#addListener(com.vaadin.data.IContainer.IItemSetChangeListener)
        """
        if isinstance(listener, IItemSetChangeListener):
            if self.getItemSetChangeListeners() is None:
                self.setItemSetChangeListeners( list() )

            self.getItemSetChangeListeners().append(listener)
        elif isinstance(listener, IPropertySetChangeListener):
            if self.getPropertySetChangeListeners() is None:
                self.setPropertySetChangeListeners(list())

            self.getPropertySetChangeListeners().append(listener)
        else:
            super(AbstractContainer, self).addListener(listener)


    def addItemSetChangeListener(self, listener):
        if self.getItemSetChangeListeners() is None:
            self.setItemSetChangeListeners( list() )

        self.getItemSetChangeListeners().append(listener)


    def addPropertySetChangeListener(self, listener):
        if self.getPropertySetChangeListeners() is None:
            self.setPropertySetChangeListeners(list())

        self.getPropertySetChangeListeners().append(listener)


    def removeListener(self, listener):
        """Implementation of the corresponding method in
        {@link PropertySetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see PropertySetChangeNotifier#removeListener(com.vaadin.data.IContainer.
             PropertySetChangeListener)
        ---
        Implementation of the corresponding method in
        {@link ItemSetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see ItemSetChangeNotifier#removeListener(com.vaadin.data.IContainer.IItemSetChangeListener)
        """
        if isinstance(listener, IItemSetChangeListener):
            if self.getItemSetChangeListeners() is not None:
                self.getItemSetChangeListeners().remove(listener)
        elif isinstance(listener, IPropertySetChangeListener):
            if self.getPropertySetChangeListeners() is not None:
                self.getPropertySetChangeListeners().remove(listener)
        else:
            super(AbstractContainer, self).removeListener(listener)


    def removeItemSetChangeListener(self, listener):
        if self.getItemSetChangeListeners() is not None:
            self.getItemSetChangeListeners().remove(listener)


    def removePropertySetChangeListener(self, listener):
        if self.getPropertySetChangeListeners() is not None:
            self.getPropertySetChangeListeners().remove(listener)


    def fireContainerPropertySetChange(self, event=None):
        """Sends a simple Property set change event to all interested listeners.
        ---
        Sends a Property set change event to all interested listeners.

        Use {@link #fireContainerPropertySetChange()} instead of this method
        unless additional information about the exact changes is available and
        should be included in the event.

        @param event
                   the property change event to send, optionally with additional
                   information
        """
        if event is None:
            event = BasePropertySetChangeEvent(self)

        if self.getPropertySetChangeListeners() is not None:
            l = list(self.getPropertySetChangeListeners())
            for listener in l:
                listener.containerPropertySetChange(event)


    def fireItemSetChange(self, event=None):
        """Sends a simple Item set change event to all interested listeners,
        indicating that anything in the contents may have changed (items added,
        removed etc.).
        ---
        Sends an Item set change event to all registered interested listeners.

        @param event
                   the item set change event to send, optionally with additional
                   information
        """
        if event is None:
            event = BaseItemSetChangeEvent(self)

        if self.getItemSetChangeListeners() is not None:
            l = list(self.getItemSetChangeListeners())
            for listener in l:
                listener.containerItemSetChange(event)


    def setPropertySetChangeListeners(self, propertySetChangeListeners):
        """Sets the property set change listener collection. For internal use only.

        @param propertySetChangeListeners
        """
        self._propertySetChangeListeners = propertySetChangeListeners


    def getPropertySetChangeListeners(self):
        """Returns the property set change listener collection. For internal use
        only.
        """
        return self._propertySetChangeListeners


    def setItemSetChangeListeners(self, itemSetChangeListeners):
        """Sets the item set change listener collection. For internal use only.

        @param itemSetChangeListeners
        """
        self._itemSetChangeListeners = itemSetChangeListeners


    def getItemSetChangeListeners(self):
        """Returns the item set change listener collection. For internal use only."""
        return self._itemSetChangeListeners


    def getListeners(self, eventType):
        if issubclass(eventType, IPropertySetChangeEvent):
            if self._propertySetChangeListeners is None:
                return list()
            else:
                return list(self._propertySetChangeListeners)

        elif issubclass(eventType, IItemSetChangeEvent):
            if self._itemSetChangeListeners is None:
                return list()
            else:
                return list(self._itemSetChangeListeners)

        return list


class BasePropertySetChangeEvent(EventObject, IContainer,
            IPropertySetChangeEvent):
    """An <code>event</code> object specifying the container whose Property
    set has changed.

    This class does not provide information about which properties were
    concerned by the change, but subclasses can provide additional
    information about the changes.
    """

    def __init__(self, source):
        super(BasePropertySetChangeEvent, self).__init__(source)


    def getContainer(self):
        return self.getSource()


class BaseItemSetChangeEvent(EventObject, IContainer, IItemSetChangeEvent):
    """An <code>event</code> object specifying the container whose Item set
    has changed.

    This class does not provide information about the exact changes
    performed, but subclasses can add provide additional information about
    the changes.
    """

    def __init__(self, source):
        super(BaseItemSetChangeEvent, self).__init__(source)


    def getContainer(self):
        return self.getSource()
