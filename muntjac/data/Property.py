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


class Property(object):
    """<p>
    The <code>Property</code> is a simple data object that contains one typed
    value. This interface contains methods to inspect and modify the stored value
    and its type, and the object's read-only state.
    </p>

    <p>
    The <code>Property</code> also defines the events
    <code>ReadOnlyStatusChangeEvent</code> and <code>ValueChangeEvent</code>, and
    the associated <code>listener</code> and <code>notifier</code> interfaces.
    </p>

    <p>
    The <code>Property.Viewer</code> interface should be used to attach the
    Property to an external data source. This way the value in the data source
    can be inspected using the <code>Property</code> interface.
    </p>

    <p>
    The <code>Property.editor</code> interface should be implemented if the value
    needs to be changed through the implementing class.
    </p>

    @author IT Mill Ltd
    @version @VERSION@
    @since 3.0
    """

    def getValue(self):
        """Gets the value stored in the Property. The returned object is compatible
        with the class returned by getType().

        @return the value stored in the Property
        """
        pass


    def setValue(self, newValue):
        """Sets the value of the Property.
        <p>
        Implementing this functionality is optional. If the functionality is
        missing, one should declare the Property to be in read-only mode and
        throw <code>Property.ReadOnlyException</code> in this function.
        </p>
        Note : It is not required, but highly recommended to support setting the
        value also as a <code>String</code> in addition to the native type of the
        Property (as given by the <code>getType</code> method). If the
        <code>String</code> conversion fails or is unsupported, the method should
        throw <code>Property.ConversionException</code>. The string conversion
        should at least understand the format returned by the
        <code>toString</code> method of the Property.

        @param newValue
                   New value of the Property. This should be assignable to the
                   type returned by getType, but also String type should be
                   supported

        @throws Property.ReadOnlyException
                    if the object is in read-only mode
        @throws Property.ConversionException
                    if newValue can't be converted into the Property's native
                    type directly or through String
        """
        pass


    def toString(self):
        """Returns the value of the Property in human readable textual format. The
        return value should be assignable to the <code>setValue</code> method if
        the Property is not in read-only mode.

        @return <code>String</code> representation of the value stored in the
                Property
        """
        pass


    def getType(self):
        """Returns the type of the Property. The methods <code>getValue</code> and
        <code>setValue</code> must be compatible with this type: one must be able
        to safely cast the value returned from <code>getValue</code> to the given
        type and pass any variable assignable to this type as an argument to
        <code>setValue</code>.

        @return type of the Property
        """
        pass


    def isReadOnly(self):
        """Tests if the Property is in read-only mode. In read-only mode calls to
        the method <code>setValue</code> will throw
        <code>ReadOnlyException</code> and will not modify the value of the
        Property.

        @return <code>true</code> if the Property is in read-only mode,
                <code>false</code> if it's not
        """
        pass


    def setReadOnly(self, newStatus):
        """Sets the Property's read-only mode to the specified status.

        This functionality is optional, but all properties must implement the
        <code>isReadOnly</code> mode query correctly.

        @param newStatus
                   new read-only status of the Property
        """
        pass


class ReadOnlyException(RuntimeError):
    """<code>Exception</code> object that signals that a requested Property
    modification failed because it's in read-only mode.

    @author IT Mill Ltd.
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
            super(ReadOnlyException, self)(msg)


class ConversionException(RuntimeError):
    """An exception that signals that the value passed to the
    <code>setValue</code> method couldn't be converted to the native type of
    the Property.

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
        super(ConversionException, self)(args)


class Viewer(object):
    """Interface implemented by the viewer classes capable of using a Property
    as a data source.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def setPropertyDataSource(self, newDataSource):
        """Sets the Property that serves as the data source of the viewer.

        @param newDataSource
                   the new data source Property
        """
        pass


    def getPropertyDataSource(self):
        """Gets the Property serving as the data source of the viewer.

        @return the Property serving as the viewers data source
        """
        pass


class Editor(Viewer):
    """Interface implemented by the editor classes capable of editing the
    Property.
    <p>
    Implementing this interface means that the Property serving as the data
    source of the editor can be modified through the editor. It does not
    restrict the editor from editing the Property internally, though if the
    Property is in a read-only mode, attempts to modify it will result in the
    <code>ReadOnlyException</code> being thrown.
    </p>

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """
    pass


class ValueChangeEvent(object):
    """An <code>Event</code> object specifying the Property whose value has been
    changed.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def getProperty(self):
        """Retrieves the Property that has been modified.

        @return source Property of the event
        """
        pass


class ValueChangeListener(object):
    """The <code>listener</code> interface for receiving
    <code>ValueChangeEvent</code> objects.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def valueChange(self, event):
        """Notifies this listener that the Property's value has changed.

        @param event
                   value change event object
        """
        pass


class ValueChangeNotifier(object):
    """The interface for adding and removing <code>ValueChangeEvent</code>
    listeners. If a Property wishes to allow other objects to receive
    <code>ValueChangeEvent</code> generated by it, it must implement this
    interface.
    <p>
    Note : The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def addListener(self, listener):
        """Registers a new value change listener for this Property.

        @param listener
                   the new Listener to be registered
        """
        pass


    def removeListener(self, listener):
        """Removes a previously registered value change listener.

        @param listener
                   listener to be removed
        """
        pass


class ReadOnlyStatusChangeEvent(object):
    """An <code>Event</code> object specifying the Property whose read-only
    status has been changed.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def getProperty(self):
        """Property whose read-only state has changed.

        @return source Property of the event.
        """
        pass


class ReadOnlyStatusChangeListener(object):
    """The listener interface for receiving
    <code>ReadOnlyStatusChangeEvent</code> objects.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def readOnlyStatusChange(self, event):
        """Notifies this listener that a Property's read-only status has
        changed.

        @param event
                   Read-only status change event object
        """
        pass


class ReadOnlyStatusChangeNotifier(object):
    """The interface for adding and removing
    <code>ReadOnlyStatusChangeEvent</code> listeners. If a Property wishes to
    allow other objects to receive <code>ReadOnlyStatusChangeEvent</code>
    generated by it, it must implement this interface.
    <p>
    Note : The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def addListener(self, listener):
        """Registers a new read-only status change listener for this Property.

        @param listener
                   the new Listener to be registered
        """
        pass


    def removeListener(self, listener):
        """Removes a previously registered read-only status change listener.

        @param listener
                   listener to be removed
        """
        pass
