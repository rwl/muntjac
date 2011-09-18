# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
from com.vaadin.data.Container import (Container, ItemSetChangeEvent, PropertySetChangeEvent,)
# from java.io.Serializable import (Serializable,)


class AbstractContainer(Container):
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
    # List of all Property set change event listeners.
    _propertySetChangeListeners = None
    # List of all container Item set change event listeners.
    _itemSetChangeListeners = None

    class BasePropertySetChangeEvent(EventObject, Container, PropertySetChangeEvent, Serializable):
        """An <code>event</code> object specifying the container whose Property set
        has changed.

        This class does not provide information about which properties were
        concerned by the change, but subclasses can provide additional
        information about the changes.
        """

        def __init__(self, source):
            super(BasePropertySetChangeEvent, self)(source)

        def getContainer(self):
            return self.getSource()

    class BaseItemSetChangeEvent(EventObject, Container, ItemSetChangeEvent, Serializable):
        """An <code>event</code> object specifying the container whose Item set has
        changed.

        This class does not provide information about the exact changes
        performed, but subclasses can add provide additional information about
        the changes.
        """
        # PropertySetChangeNotifier

        def __init__(self, source):
            super(BaseItemSetChangeEvent, self)(source)

        def getContainer(self):
            return self.getSource()

    def addListener(self, *args):
        """Implementation of the corresponding method in
        {@link PropertySetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see PropertySetChangeNotifier#addListener(com.vaadin.data.Container.PropertySetChangeListener)
        ---
        Implementation of the corresponding method in
        {@link ItemSetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see ItemSetChangeNotifier#addListener(com.vaadin.data.Container.ItemSetChangeListener)
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.ItemSetChangeListener):
                listener, = _0
                if self.getItemSetChangeListeners() is None:
                    self.setItemSetChangeListeners(LinkedList())
                self.getItemSetChangeListeners().add(listener)
            else:
                listener, = _0
                if self.getPropertySetChangeListeners() is None:
                    self.setPropertySetChangeListeners(LinkedList())
                self.getPropertySetChangeListeners().add(listener)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Implementation of the corresponding method in
        {@link PropertySetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see PropertySetChangeNotifier#removeListener(com.vaadin.data.Container.
             PropertySetChangeListener)
        ---
        Implementation of the corresponding method in
        {@link ItemSetChangeNotifier}, override with the corresponding public
        method and implement the interface to use this.

        @see ItemSetChangeNotifier#removeListener(com.vaadin.data.Container.ItemSetChangeListener)
        """
        # ItemSetChangeNotifier
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Container.ItemSetChangeListener):
                listener, = _0
                if self.getItemSetChangeListeners() is not None:
                    self.getItemSetChangeListeners().remove(listener)
            else:
                listener, = _0
                if self.getPropertySetChangeListeners() is not None:
                    self.getPropertySetChangeListeners().remove(listener)
        else:
            raise ARGERROR(1, 1)

    def fireContainerPropertySetChange(self, *args):
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
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.fireContainerPropertySetChange(self.BasePropertySetChangeEvent(self))
        elif _1 == 1:
            event, = _0
            if self.getPropertySetChangeListeners() is not None:
                l = list(self.getPropertySetChangeListeners())
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(l)):
                        break
                    l[i].containerPropertySetChange(event)
        else:
            raise ARGERROR(0, 1)

    def fireItemSetChange(self, *args):
        """Sends a simple Item set change event to all interested listeners,
        indicating that anything in the contents may have changed (items added,
        removed etc.).
        ---
        Sends an Item set change event to all registered interested listeners.

        @param event
                   the item set change event to send, optionally with additional
                   information
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.fireItemSetChange(self.BaseItemSetChangeEvent(self))
        elif _1 == 1:
            event, = _0
            if self.getItemSetChangeListeners() is not None:
                l = list(self.getItemSetChangeListeners())
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(l)):
                        break
                    l[i].containerItemSetChange(event)
        else:
            raise ARGERROR(0, 1)

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
        if Container.PropertySetChangeEvent.isAssignableFrom(eventType):
            if self._propertySetChangeListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._propertySetChangeListeners)
        elif Container.ItemSetChangeEvent.isAssignableFrom(eventType):
            if self._itemSetChangeListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._itemSetChangeListeners)
        return Collections.EMPTY_LIST
