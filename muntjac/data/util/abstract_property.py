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
        self._readOnlyStatusChangeListeners = None

        #: List of listeners who are interested in the value changes of
        #  the IProperty
        self._valueChangeListeners = None

        #: Is the IProperty read-only?
        self._readOnly = None


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
                (iface is None or iface == prop.IReadOnlyStatusChangeListener)):
            if self._readOnlyStatusChangeListeners is None:
                self._readOnlyStatusChangeListeners = list()

            self._readOnlyStatusChangeListeners.append( (listener, tuple()) )

        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or iface == prop.IValueChangeListener)):
            if self._valueChangeListeners is None:
                self._valueChangeListeners = list()

            self._valueChangeListeners.append( (listener, tuple()) )


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if eventType == prop.IReadOnlyStatusChangeEvent:
            if self._readOnlyStatusChangeListeners is None:
                self._readOnlyStatusChangeListeners = list()

            self._readOnlyStatusChangeListeners.append( (callback, args) )

        elif eventType == prop.ValueChangeEvent:
            if self._valueChangeListeners is None:
                self._valueChangeListeners = list()

            self._valueChangeListeners.append( (callback, args) )

        else:
            super(AbstractProperty, self).addCallback(callback, eventType,
                    *args)


    def removeListener(self, listener, iface=None):
        """Removes a previously registered read-only status change listener.

        @param listener:
                   the listener to be removed.
        """
        if (isinstance(listener, prop.IReadOnlyStatusChangeListener) and
            (iface is None or iface == prop.IReadOnlyStatusChangeListener)):
            if self._readOnlyStatusChangeListeners is not None:
                for i, (l, _) in enumerate(
                        self._readOnlyStatusChangeListeners[:]):
                    if listener == l:
                        del self._readOnlyStatusChangeListeners[i]
                        break

        if (isinstance(listener, prop.IValueChangeListener) and
                (iface is None or iface == prop.IValueChangeListener)):
            if self._valueChangeListeners is not None:
                for i, (l, _) in enumerate(self._valueChangeListeners[:]):
                    if listener == l:
                        del self._valueChangeListeners[i]
                        break


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if eventType == prop.IReadOnlyStatusChangeEvent:
            if self._readOnlyStatusChangeListeners is not None:
                for i, (l, _) in enumerate(
                        self._readOnlyStatusChangeListeners[:]):
                    if callback == l:
                        del self._readOnlyStatusChangeListeners[i]
                        break

        elif eventType == prop.ValueChangeEvent:
            if self._valueChangeListeners is not None:
                for i, (l, _) in enumerate(self._valueChangeListeners[:]):
                    if callback == l:
                        del self._valueChangeListeners[i]
                        break

        else:
            super(AbstractProperty, self).removeCallback(callback, eventType)


    def fireReadOnlyStatusChange(self):
        """Sends a read only status change event to all registered listeners.
        """
        if self._readOnlyStatusChangeListeners is not None:
            l = list(self._readOnlyStatusChangeListeners)
            event = prop.IReadOnlyStatusChangeEvent(self)
            for listener, args in l:
                if isinstance(listener, prop.IReadOnlyStatusChangeListener):
                    listener.readOnlyStatusChange(event)
                else:
                    listener(event, *args)


    def fireValueChange(self):
        """Sends a value change event to all registered listeners."""
        if self._valueChangeListeners is not None:
            l = list(self._valueChangeListeners)
            event = ValueChangeEvent(self)
            for listener, args in l:
                if isinstance(listener, prop.IValueChangeListener):
                    listener.valueChange(event)
                else:
                    listener(event, *args)


    def getListeners(self, eventType):
        if issubclass(eventType, ValueChangeEvent):
            if self._valueChangeListeners is None:
                return list()
            else:
                return list(self._valueChangeListeners)
        elif issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            if self._readOnlyStatusChangeListeners is None:
                return list()
            else:
                return list(self._readOnlyStatusChangeListeners)
        return list()


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
