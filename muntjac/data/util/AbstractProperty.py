# -*- coding: utf-8 -*-
from __pyjamas__ import (ARGERROR,)
from com.vaadin.data.Property import (Property, ReadOnlyStatusChangeEvent, ReadOnlyStatusChangeNotifier, ValueChangeEvent, ValueChangeNotifier,)


class AbstractProperty(Property, Property, ValueChangeNotifier, Property, ReadOnlyStatusChangeNotifier):
    """Abstract base class for {@link Property} implementations.

    Handles listener management for {@link ValueChangeListener}s and
    {@link ReadOnlyStatusChangeListener}s.

    @since 6.6
    """
    # List of listeners who are interested in the read-only status changes of
    # the Property

    _readOnlyStatusChangeListeners = None
    # List of listeners who are interested in the value changes of the Property
    _valueChangeListeners = None
    # Is the Property read-only?
    _readOnly = None

    def isReadOnly(self):
        """{@inheritDoc}

        Override for additional restrictions on what is considered a read-only
        property.
        """
        return self._readOnly

    def setReadOnly(self, newStatus):
        oldStatus = self.isReadOnly()
        self._readOnly = newStatus
        if oldStatus != self.isReadOnly():
            self.fireReadOnlyStatusChange()

    def toString(self):
        """Returns the value of the <code>Property</code> in human readable textual
        format. The return value should be assignable to the
        <code>setValue</code> method if the Property is not in read-only mode.

        @return String representation of the value stored in the Property
        """
        # Events
        value = self.getValue()
        if value is None:
            return None
        return str(value)

    class ReadOnlyStatusChangeEvent(java.util.EventObject, Property, ReadOnlyStatusChangeEvent):
        """An <code>Event</code> object specifying the Property whose read-only
        status has been changed.
        """

        def __init__(self, source):
            """Constructs a new read-only status change event for this object.

            @param source
                       source object of the event.
            """
            super(ReadOnlyStatusChangeEvent, self)(source)

        def getProperty(self):
            """Gets the Property whose read-only state has changed.

            @return source Property of the event.
            """
            return self.getSource()

    def addListener(self, *args):
        """Registers a new read-only status change listener for this Property.

        @param listener
                   the new Listener to be registered.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Property.ReadOnlyStatusChangeListener):
                listener, = _0
                if self._readOnlyStatusChangeListeners is None:
                    self._readOnlyStatusChangeListeners = LinkedList()
                self._readOnlyStatusChangeListeners.add(listener)
            else:
                listener, = _0
                if self._valueChangeListeners is None:
                    self._valueChangeListeners = LinkedList()
                self._valueChangeListeners.add(listener)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Removes a previously registered read-only status change listener.

        @param listener
                   the listener to be removed.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Property.ReadOnlyStatusChangeListener):
                listener, = _0
                if self._readOnlyStatusChangeListeners is not None:
                    self._readOnlyStatusChangeListeners.remove(listener)
            else:
                listener, = _0
                if self._valueChangeListeners is not None:
                    self._valueChangeListeners.remove(listener)
        else:
            raise ARGERROR(1, 1)

    def fireReadOnlyStatusChange(self):
        """Sends a read only status change event to all registered listeners."""
        if self._readOnlyStatusChangeListeners is not None:
            l = list(self._readOnlyStatusChangeListeners)
            event = ReadOnlyStatusChangeEvent(self)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(l)):
                    break
                l[i].readOnlyStatusChange(event)

    class ValueChangeEvent(java.util.EventObject, Property, ValueChangeEvent):
        """An <code>Event</code> object specifying the Property whose value has been
        changed.
        """

        def __init__(self, source):
            """Constructs a new value change event for this object.

            @param source
                       source object of the event.
            """
            super(ValueChangeEvent, self)(source)

        def getProperty(self):
            """Gets the Property whose value has changed.

            @return source Property of the event.
            """
            return self.getSource()

    def fireValueChange(self):
        """Sends a value change event to all registered listeners."""
        if self._valueChangeListeners is not None:
            l = list(self._valueChangeListeners)
            event = ValueChangeEvent(self)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(l)):
                    break
                l[i].valueChange(event)

    def getListeners(self, eventType):
        if Property.ValueChangeEvent.isAssignableFrom(eventType):
            if self._valueChangeListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._valueChangeListeners)
        elif Property.ReadOnlyStatusChangeEvent.isAssignableFrom(eventType):
            if self._readOnlyStatusChangeListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._readOnlyStatusChangeListeners)
        return Collections.EMPTY_LIST
