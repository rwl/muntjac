# Copyright (C) 2011 Vaadin Ltd.
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

"""Abstract base class for property implementations."""

from muntjac.data import property as prop
from muntjac.util import EventObject


class AbstractProperty(prop.IProperty, prop.IValueChangeNotifier,
            prop.IReadOnlyStatusChangeNotifier):
    """Abstract base class for L{IProperty} implementations.

    Handles listener management for L{ValueChangeListener}s and
    L{IReadOnlyStatusChangeListener}s.
    """

    def __init__(self):
        #: List of listeners who are interested in the read-only status
        #  changes of the IProperty
        self._readOnlyStatusChangeListeners = list()

        #: List of listeners who are interested in the value changes of
        #  the IProperty
        self._valueChangeListeners = list()

        #: Is the IProperty read-only?
        self._readOnly = None

        self._readOnlyStatusChangeCallbacks = dict()

        self._valueChangeCallbacks = dict()



    def isReadOnly(self):
        """Override for additional restrictions on what is considered a
        read-only property.
        """
        return self._readOnly


    def setReadOnly(self, newStatus):
        oldStatus = self.isReadOnly()
        self._readOnly = newStatus
        if oldStatus != self.isReadOnly():
            self.fireReadOnlyStatusChange()


    def __str__(self):
        """Returns the value of the C{IProperty} in human readable
        textual format. The return value should be assignable to the
        C{setValue} method if the IProperty is not in read-only mode.

        @return: String representation of the value stored in the IProperty
        """
        value = self.getValue()
        if value is None:
            return None
        return str(value)


    def addListener(self, listener, iface=None):
        """Registers a new read-only status change listener for this IProperty.

        @param listener:
                   the new Listener to be registered.
        """
        if (isinstance(listener, prop.IReadOnlyStatusChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IReadOnlyStatusChangeListener))):

            self._readOnlyStatusChangeListeners.append(listener)

        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IValueChangeListener))):

            self._valueChangeListeners.append(listener)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            self._readOnlyStatusChangeCallbacks[callback] = args

        elif issubclass(eventType, prop.ValueChangeEvent):
            self._valueChangeCallbacks[callback] = args

        else:
            super(AbstractProperty, self).addCallback(callback,
                    eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes a previously registered read-only status change listener.

        @param listener:
                   the listener to be removed.
        """
        if (isinstance(listener, prop.IReadOnlyStatusChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IReadOnlyStatusChangeListener))):
            if listener in self._readOnlyStatusChangeListeners:
                self._readOnlyStatusChangeListeners.remove(listener)

        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or
                        issubclass(iface, prop.IValueChangeListener))):
            if listener in self._valueChangeListeners:
                self._valueChangeListeners.remove(listener)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            if callback in self._readOnlyStatusChangeCallbacks:
                del self._readOnlyStatusChangeCallbacks[callback]

        elif issubclass(eventType, prop.ValueChangeEvent):
            if callback in self._valueChangeCallbacks:
                del self._valueChangeCallbacks[callback]

        else:
            super(AbstractProperty, self).removeCallback(callback, eventType)


    def fireReadOnlyStatusChange(self):
        """Sends a read only status change event to all registered listeners.
        """
        event = prop.IReadOnlyStatusChangeEvent(self)
        for listener in self._readOnlyStatusChangeListeners:
            listener.readOnlyStatusChange(event)

        for callback, args in self._readOnlyStatusChangeCallbacks.iteritems():
            callback(event, *args)


    def fireValueChange(self):
        """Sends a value change event to all registered listeners."""
        event = ValueChangeEvent(self)
        for listener in self._valueChangeListeners:
            listener.valueChange(event)

        for callback, args in self._valueChangeCallbacks.iteritems():
            callback(event, *args)


    def getListeners(self, eventType):
        if issubclass(eventType, prop.ValueChangeEvent):
            return list(self._valueChangeListeners)

        elif issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            return list(self._readOnlyStatusChangeListeners)

        return list()


    def getCallbacks(self, eventType):
        if issubclass(eventType, ValueChangeEvent):
            return dict(self._valueChangeCallbacks)

        elif issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            return dict(self._readOnlyStatusChangeCallbacks)

        return dict()


class IReadOnlyStatusChangeEvent(EventObject, prop.IProperty,
            prop.IReadOnlyStatusChangeEvent):
    """An C{Event} object specifying the IProperty whose read-only
    status has been changed.
    """

    def __init__(self, source):
        """Constructs a new read-only status change event for this object.

        @param source:
                   source object of the event.
        """
        super(IReadOnlyStatusChangeEvent, self).__init__(source)


    def getProperty(self):
        """Gets the IProperty whose read-only state has changed.

        @return: source IProperty of the event.
        """
        return self.getSource()


class ValueChangeEvent(EventObject, prop.ValueChangeEvent):
    """An C{Event} object specifying the IProperty whose value has
    been changed.
    """

    def __init__(self, source):
        """Constructs a new value change event for this object.

        @param source:
                   source object of the event.
        """
        super(ValueChangeEvent, self).__init__(source)


    def getProperty(self):
        """Gets the IProperty whose value has changed.

        @return: source IProperty of the event.
        """
        return self.getSource()
