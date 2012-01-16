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

"""A simple data object that contains one typed value."""


class IProperty(object):
    """The C{IProperty} is a simple data object that contains one typed value.
    This interface contains methods to inspect and modify the stored value
    and its type, and the object's read-only state.

    The C{IProperty} also defines the events C{IReadOnlyStatusChangeEvent} and
    C{ValueChangeEvent}, and the associated C{listener} and C{notifier}
    interfaces.

    The C{IViewer} interface should be used to attach the IProperty to an
    external data source. This way the value in the data source can be
    inspected using the C{IProperty} interface.

    The C{IProperty.editor} interface should be implemented if the value
    needs to be changed through the implementing class.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def getValue(self):
        """Gets the value stored in the IProperty. The returned object is
        compatible with the class returned by getType().

        @return: the value stored in the IProperty
        """
        raise NotImplementedError


    def setValue(self, newValue):
        """Sets the value of the IProperty.

        Implementing this functionality is optional. If the functionality is
        missing, one should declare the IProperty to be in read-only mode and
        throw C{ReadOnlyException} in this function.

        Note: It is not required, but highly recommended to support setting the
        value also as a C{String} in addition to the native type of the
        IProperty (as given by the C{getType} method). If the
        string conversion fails or is unsupported, the method should
        throw C{ConversionException}. The string conversion
        should at least understand the format returned by the
        C{__str__} method of the IProperty.

        @param newValue:
                   New value of the IProperty. This should be assignable to the
                   type returned by getType, but also String type should be
                   supported

        @raise ReadOnlyException:
                    if the object is in read-only mode
        @raise ConversionException:
                    if newValue can't be converted into the IProperty's native
                    type directly or through String
        """
        raise NotImplementedError


    def __str__(self):
        """Returns the value of the IProperty in human readable textual format.
        The return value should be assignable to the C{setValue} method if
        the IProperty is not in read-only mode.

        @return: String representation of the value stored in the IProperty
        """
        raise NotImplementedError


    def getType(self):
        """Returns the type of the IProperty. The methods C{getValue} and
        C{setValue} must be compatible with this type: one must be able
        to safely cast the value returned from C{getValue} to the given
        type and pass any variable assignable to this type as an argument to
        C{setValue}.

        @return: type of the IProperty
        """
        raise NotImplementedError


    def isReadOnly(self):
        """Tests if the IProperty is in read-only mode. In read-only mode calls
        to the method C{setValue} will throw
        C{ReadOnlyException} and will not modify the value of the
        IProperty.

        @return: C{True} if the IProperty is in read-only mode, C{False} if
                it's not
        """
        raise NotImplementedError


    def setReadOnly(self, newStatus):
        """Sets the IProperty's read-only mode to the specified status.

        This functionality is optional, but all properties must implement the
        C{isReadOnly} mode query correctly.

        @param newStatus:
                   new read-only status of the IProperty
        """
        raise NotImplementedError


class ReadOnlyException(RuntimeError):
    """C{Exception} object that signals that a requested IProperty
    modification failed because it's in read-only mode.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, msg=None):
        """Constructs a new C{ReadOnlyException} with the specified
        detail message.

        @param msg:
                   the detail message
        """
        if msg is not None:
            super(ReadOnlyException, self).__init__(msg)


class ConversionException(RuntimeError):
    """An exception that signals that the value passed to the
    C{setValue} method couldn't be converted to the native type of
    the IProperty.

    @author: Vaadin Ltd.
    @version: 1.1.0
    """

    def __init__(self, *args):
        """Constructs a new C{ConversionException} with the specified
        detail message and cause.

        @param args: tuple of the form
              - ()
              - (msg)
                1. the detail message
              - (cause)
                1. The cause of the the conversion failure
              - (msg, cause)
                1. the detail message
                2. The cause of the the conversion failure
        """
        super(ConversionException, self).__init__(*args)


class IViewer(object):
    """Interface implemented by the viewer classes capable of using a IProperty
    as a data source.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def setPropertyDataSource(self, newDataSource):
        """Sets the IProperty that serves as the data source of the viewer.

        @param newDataSource:
                   the new data source IProperty
        """
        raise NotImplementedError


    def getPropertyDataSource(self):
        """Gets the IProperty serving as the data source of the viewer.

        @return: the IProperty serving as the viewers data source
        """
        raise NotImplementedError


class IEditor(IViewer):
    """Interface implemented by the editor classes capable of editing the
    IProperty.

    Implementing this interface means that the IProperty serving as the data
    source of the editor can be modified through the editor. It does not
    restrict the editor from editing the IProperty internally, though if the
    IProperty is in a read-only mode, attempts to modify it will result in the
    C{ReadOnlyException} being thrown.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """
    pass


class ValueChangeEvent(object):
    """An C{Event} object specifying the IProperty whose value has been
    changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def getProperty(self):
        """Retrieves the IProperty that has been modified.

        @return: source IProperty of the event
        """
        raise NotImplementedError


class IValueChangeListener(object):
    """The C{listener} interface for receiving
    C{ValueChangeEvent} objects.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def valueChange(self, event):
        """Notifies this listener that the IProperty's value has changed.

        @param event:
                   value change event object
        """
        raise NotImplementedError


class IValueChangeNotifier(object):
    """The interface for adding and removing C{ValueChangeEvent}
    listeners. If a IProperty wishes to allow other objects to receive
    C{ValueChangeEvent} generated by it, it must implement this
    interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def addListener(self, listener, iface=None):
        """Registers a new value change listener for this IProperty.

        @param listener:
                   the new Listener to be registered
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Removes a previously registered value change listener.

        @param listener:
                   listener to be removed
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


class IReadOnlyStatusChangeEvent(object):
    """An C{Event} object specifying the IProperty whose read-only
    status has been changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def getProperty(self):
        """IProperty whose read-only state has changed.

        @return: source IProperty of the event.
        """
        raise NotImplementedError


class IReadOnlyStatusChangeListener(object):
    """The listener interface for receiving C{IReadOnlyStatusChangeEvent}
    objects.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def readOnlyStatusChange(self, event):
        """Notifies this listener that a IProperty's read-only status has
        changed.

        @param event:
                   Read-only status change event object
        """
        raise NotImplementedError


class IReadOnlyStatusChangeNotifier(object):
    """The interface for adding and removing C{IReadOnlyStatusChangeEvent}
    listeners. If a IProperty wishes to allow other objects to receive
    C{IReadOnlyStatusChangeEvent} generated by it, it must implement this
    interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def addListener(self, listener, iface=None):
        """Registers a new read-only status change listener for this IProperty.

        @param listener:
                   the new Listener to be registered
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Removes a previously registered read-only status change listener.

        @param listener:
                   listener to be removed
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError
