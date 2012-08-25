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

"""Abstract container class that manages event listeners and sending events
to them."""

from muntjac.util import EventObject

from muntjac.data.container import \
    (IContainer, IItemSetChangeEvent, IPropertySetChangeEvent,
     IPropertySetChangeListener, IItemSetChangeListener)


class AbstractContainer(IContainer):
    """Abstract container class that manages event listeners and sending events
    to them (L{PropertySetChangeNotifier}, L{ItemSetChangeNotifier}).

    Note that this class provides the internal implementations for both types
    of events and notifiers as protected methods, but does not implement the
    L{IPropertySetChangeNotifier} and L{ItemSetChangeNotifier} interfaces
    directly. This way, subclasses can choose not to implement them.
    Subclasses implementing those interfaces should also override the
    corresponding L{addListener} and L{removeListener} methods to make them
    public.
    """

    def __init__(self):
        #: List of all Property set change event listeners.
        self._propertySetChangeListeners = list()

        #: List of all container Item set change event listeners.
        self._itemSetChangeListeners = list()

        self._propertySetChangeCallbacks = dict()

        self._itemSetChangeCallbacks = dict()


    def addListener(self, listener, iface=None):
        """Implementation of the corresponding method in
        L{IPropertySetChangeNotifier} and L{ItemSetChangeNotifier}, override
        and implement the interface to use this.

        @see: L{IPropertySetChangeNotifier.addListener}
        @see: L{IItemSetChangeNotifier.addListener}
        """
        if (isinstance(listener, IItemSetChangeListener) and
                (iface is None or issubclass(iface, IItemSetChangeListener))):

            self.getItemSetChangeListeners().append(listener)

        if (isinstance(listener, IPropertySetChangeListener) and
                (iface is None or
                        issubclass(iface, IPropertySetChangeListener))):

            self.getPropertySetChangeListeners().append(listener)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, IItemSetChangeEvent):
            self._itemSetChangeCallbacks[callback] = args

        elif issubclass(eventType, IPropertySetChangeEvent):
            self._propertySetChangeCallbacks[callback] = args

        else:
            super(AbstractContainer, self).addCallback(callback,
                    eventType, args)


    def removeListener(self, listener, iface=None):
        """Implementation of the corresponding method in
        L{IPropertySetChangeNotifier} and L{ItemSetChangeNotifier}, override
        and implement the interface to use this.

        @see: L{IPropertySetChangeNotifier.removeListener}
        @see: L{ItemSetChangeNotifier.removeListener}
        """
        if (isinstance(listener, IItemSetChangeListener) and
                (iface is None or issubclass(iface, IItemSetChangeListener))):
            if listener in self.getItemSetChangeListeners():
                self.getItemSetChangeListeners().remove(listener)

        if (isinstance(listener, IPropertySetChangeListener) and
                (iface is None or
                        issubclass(iface, IPropertySetChangeListener))):
            if listener in self.getPropertySetChangeListeners():
                self.getPropertySetChangeListeners().remove(listener)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if (issubclass(eventType, IItemSetChangeEvent) and
                callback in self._itemSetChangeCallbacks):
            del self._itemSetChangeCallbacks[callback]

        elif (issubclass(eventType, IPropertySetChangeEvent) and
                callback in self._propertySetChangeCallbacks):
            del self._propertySetChangeCallbacks[callback]

        else:
            super(AbstractContainer, self).removeCallback(callback, eventType)


    def fireContainerPropertySetChange(self, event=None):
        """Sends a simple Property set change event to all interested
        listeners.

        Use L{fireContainerPropertySetChange} instead of this method
        unless additional information about the exact changes is available and
        should be included in the event.

        @param event:
                   the property change event to send, optionally with
                   additional information
        """
        if event is None:
            event = BasePropertySetChangeEvent(self)

        for listener in self.getPropertySetChangeListeners():
            listener.containerPropertySetChange(event)

        for callback, args in self._propertySetChangeCallbacks.iteritems():
            callback(event, *args)


    def fireItemSetChange(self, event=None):
        """Sends a simple Item set change event to all interested listeners,
        indicating that anything in the contents may have changed (items added,
        removed etc.).

        @param event:
                   the item set change event to send, optionally with
                   additional information
        """
        if event is None:
            event = BaseItemSetChangeEvent(self)

        for listener in self.getItemSetChangeListeners():
            listener.containerItemSetChange(event)

        for callback, args in self._itemSetChangeCallbacks.iteritems():
            callback(event, *args)


    def setPropertySetChangeListeners(self, propertySetChangeListeners):
        """Sets the property set change listener collection. For internal
        use only.
        """
        self._propertySetChangeListeners = propertySetChangeListeners


    def getPropertySetChangeListeners(self):
        """Returns the property set change listener collection. For internal
        use only.
        """
        return self._propertySetChangeListeners


    def setItemSetChangeListeners(self, itemSetChangeListeners):
        """Sets the item set change listener collection. For internal use only.
        """
        self._itemSetChangeListeners = itemSetChangeListeners


    def getItemSetChangeListeners(self):
        """Returns the item set change listener collection. For internal use
        only."""
        return self._itemSetChangeListeners


    def getListeners(self, eventType):
        if issubclass(eventType, IPropertySetChangeEvent):
            return list(self._propertySetChangeListeners)

        elif issubclass(eventType, IItemSetChangeEvent):
            return list(self._itemSetChangeListeners)

        return list()


    def getCallbacks(self, eventType):
        if issubclass(eventType, IPropertySetChangeEvent):
            return dict(self._propertySetChangeCallbacks)

        elif issubclass(eventType, IItemSetChangeEvent):
            return dict(self._itemSetChangeCallbacks)

        return dict()


class BasePropertySetChangeEvent(EventObject, IContainer,
            IPropertySetChangeEvent):
    """An C{event} object specifying the container whose Property
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
    """An C{event} object specifying the container whose Item set
    has changed.

    This class does not provide information about the exact changes
    performed, but subclasses can add provide additional information about
    the changes.
    """

    def __init__(self, source):
        super(BaseItemSetChangeEvent, self).__init__(source)


    def getContainer(self):
        return self.getSource()
