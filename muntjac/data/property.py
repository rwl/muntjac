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


class IProperty(object):
    """The <code>IProperty</code> is a simple data object that contains one typed
    value. This interface contains methods to inspect and modify the stored value
    and its type, and the object's read-only state.

    The <code>IProperty</code> also defines the events
    <code>IReadOnlyStatusChangeEvent</code> and <code>ValueChangeEvent</code>, and
    the associated <code>listener</code> and <code>notifier</code> interfaces.

    The <code>IProperty.IViewer</code> interface should be used to attach the
    IProperty to an external data source. This way the value in the data source
    can be inspected using the <code>IProperty</code> interface.

    The <code>IProperty.editor</code> interface should be implemented if the value
    needs to be changed through the implementing class.

    @author IT Mill Ltd
    @version @VERSION@
    @since 3.0
    """

    def getValue(self):
        """Gets the value stored in the IProperty. The returned object is compatible
        with the class returned by getType().

        @return the value stored in the IProperty
        """
        raise NotImplementedError


    def setValue(self, newValue):
        """Sets the value of the IProperty.

        Implementing this functionality is optional. If the functionality is
        missing, one should declare the IProperty to be in read-only mode and
        throw <code>IProperty.ReadOnlyException</code> in this function.

        Note : It is not required, but highly recommended to support setting the
        value also as a <code>String</code> in addition to the native type of the
        IProperty (as given by the <code>getType</code> method). If the
        <code>String</code> conversion fails or is unsupported, the method should
        throw <code>IProperty.ConversionException</code>. The string conversion
        should at least understand the format returned by the
        <code>toString</code> method of the IProperty.

        @param newValue
                   New value of the IProperty. This should be assignable to the
                   type returned by getType, but also String type should be
                   supported

        @throws IProperty.ReadOnlyException
                    if the object is in read-only mode
        @throws IProperty.ConversionException
                    if newValue can't be converted into the IProperty's native
                    type directly or through String
        """
        raise NotImplementedError


    def toString(self):
        """Returns the value of the IProperty in human readable textual format. The
        return value should be assignable to the <code>setValue</code> method if
        the IProperty is not in read-only mode.

        @return <code>String</code> representation of the value stored in the
                IProperty
        """
        raise NotImplementedError


    def getType(self):
        """Returns the type of the IProperty. The methods <code>getValue</code> and
        <code>setValue</code> must be compatible with this type: one must be able
        to safely cast the value returned from <code>getValue</code> to the given
        type and pass any variable assignable to this type as an argument to
        <code>setValue</code>.

        @return type of the IProperty
        """
        raise NotImplementedError


    def isReadOnly(self):
        """Tests if the IProperty is in read-only mode. In read-only mode calls to
        the method <code>setValue</code> will throw
        <code>ReadOnlyException</code> and will not modify the value of the
        IProperty.

        @return <code>true</code> if the IProperty is in read-only mode,
                <code>false</code> if it's not
        """
        raise NotImplementedError


    def setReadOnly(self, newStatus):
        """Sets the IProperty's read-only mode to the specified status.

        This functionality is optional, but all properties must implement the
        <code>isReadOnly</code> mode query correctly.

        @param newStatus
                   new read-only status of the IProperty
        """
        raise NotImplementedError


class ReadOnlyException(RuntimeError):
    """<code>Exception</code> object that signals that a requested IProperty
    modification failed because it's in read-only mode.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, msg=None):
        """Constructs a new <code>ReadOnlyException</code> without a detail
        message.
        ---
        Constructs a new <code>ReadOnlyException</code> with the specified
        detail message.

        @param msg
                   the detail message
        """
        if msg is not None:
            super(ReadOnlyException, self).__init__(msg)


class ConversionException(RuntimeError):
    """An exception that signals that the value passed to the
    <code>setValue</code> method couldn't be converted to the native type of
    the IProperty.

    @author IT Mill Ltd
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, *args):
        """Constructs a new <code>ConversionException</code> without a detail
        message.
        ---
        Constructs a new <code>ConversionException</code> with the specified
        detail message.

        @param msg
                   the detail message
        ---
        Constructs a new <code>ConversionException</code> from another
        exception.

        @param cause
                   The cause of the the conversion failure
        ---
        Constructs a new <code>ConversionException</code> with the specified
        detail message and cause.

        @param message
                   the detail message
        @param cause
                   The cause of the the conversion failure
        """
        super(ConversionException, self).__init__(args)


class IViewer(object):
    """Interface implemented by the viewer classes capable of using a IProperty
    as a data source.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def setPropertyDataSource(self, newDataSource):
        """Sets the IProperty that serves as the data source of the viewer.

        @param newDataSource
                   the new data source IProperty
        """
        raise NotImplementedError


    def getPropertyDataSource(self):
        """Gets the IProperty serving as the data source of the viewer.

        @return the IProperty serving as the viewers data source
        """
        raise NotImplementedError


class IEditor(IViewer):
    """Interface implemented by the editor classes capable of editing the
    IProperty.

    Implementing this interface means that the IProperty serving as the data
    source of the editor can be modified through the editor. It does not
    restrict the editor from editing the IProperty internally, though if the
    IProperty is in a read-only mode, attempts to modify it will result in the
    <code>ReadOnlyException</code> being thrown.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """
    pass


class ValueChangeEvent(object):
    """An <code>Event</code> object specifying the IProperty whose value has been
    changed.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def getProperty(self):
        """Retrieves the IProperty that has been modified.

        @return source IProperty of the event
        """
        raise NotImplementedError


class IValueChangeListener(object):
    """The <code>listener</code> interface for receiving
    <code>ValueChangeEvent</code> objects.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def valueChange(self, event):
        """Notifies this listener that the IProperty's value has changed.

        @param event
                   value change event object
        """
        raise NotImplementedError


class IValueChangeNotifier(object):
    """The interface for adding and removing <code>ValueChangeEvent</code>
    listeners. If a IProperty wishes to allow other objects to receive
    <code>ValueChangeEvent</code> generated by it, it must implement this
    interface.

    Note : The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def addListener(self, listener):
        """Registers a new value change listener for this IProperty.

        @param listener
                   the new Listener to be registered
        """
        raise NotImplementedError


    def removeListener(self, listener):
        """Removes a previously registered value change listener.

        @param listener
                   listener to be removed
        """
        raise NotImplementedError


class IReadOnlyStatusChangeEvent(object):
    """An <code>Event</code> object specifying the IProperty whose read-only
    status has been changed.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def getProperty(self):
        """IProperty whose read-only state has changed.

        @return source IProperty of the event.
        """
        raise NotImplementedError


class IReadOnlyStatusChangeListener(object):
    """The listener interface for receiving
    <code>IReadOnlyStatusChangeEvent</code> objects.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def readOnlyStatusChange(self, event):
        """Notifies this listener that a IProperty's read-only status has
        changed.

        @param event
                   Read-only status change event object
        """
        raise NotImplementedError


class IReadOnlyStatusChangeNotifier(object):
    """The interface for adding and removing
    <code>IReadOnlyStatusChangeEvent</code> listeners. If a IProperty wishes to
    allow other objects to receive <code>IReadOnlyStatusChangeEvent</code>
    generated by it, it must implement this interface.

    Note : The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def addListener(self, listener):
        """Registers a new read-only status change listener for this IProperty.

        @param listener
                   the new Listener to be registered
        """
        raise NotImplementedError


    def removeListener(self, listener):
        """Removes a previously registered read-only status change listener.

        @param listener
                   listener to be removed
        """
        raise NotImplementedError
