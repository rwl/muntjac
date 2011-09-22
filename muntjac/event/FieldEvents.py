# Copyright (C) 2011 Vaadin Ltd
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

from com.vaadin.terminal.gwt.client.EventId import (EventId,)
from com.vaadin.event.ComponentEventListener import (ComponentEventListener,)
from com.vaadin.ui.Field.ValueChangeEvent import (ValueChangeEvent,)

class FieldEvents(object):
    """Interface that serves as a wrapper for {@link Field} related events."""
    pass


class FocusNotifier(Serializable):
    """The interface for adding and removing <code>FocusEvent</code> listeners.
    By implementing this interface a class explicitly announces that it will
    generate a <code>FocusEvent</code> when it receives keyboard focus.
    <p>
    Note: The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>

    @since 6.2
    @see FocusListener
    @see FocusEvent
    """

    def addListener(self, listener):
        """Adds a <code>FocusListener</code> to the Component which gets fired
        when a <code>Field</code> receives keyboard focus.

        @param listener
        @see FocusListener
        @since 6.2
        """
        pass

    def removeListener(self, listener):
        """Removes a <code>FocusListener</code> from the Component.

        @param listener
        @see FocusListener
        @since 6.2
        """
        pass

class BlurNotifier(Serializable):
    """The interface for adding and removing <code>BlurEvent</code> listeners.
    By implementing this interface a class explicitly announces that it will
    generate a <code>BlurEvent</code> when it loses keyboard focus.
    <p>
    Note: The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    <code>addListener</code> and <code>removeListener</code> methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.
    </p>

    @since 6.2
    @see BlurListener
    @see BlurEvent
    """

    def addListener(self, listener):
        """Adds a <code>BlurListener</code> to the Component which gets fired
        when a <code>Field</code> loses keyboard focus.

        @param listener
        @see BlurListener
        @since 6.2
        """
        pass

    def removeListener(self, listener):
        """Removes a <code>BlurListener</code> from the Component.

        @param listener
        @see BlurListener
        @since 6.2
        """
        pass

class FocusEvent(Component.Event):
    """<code>FocusEvent</code> class for holding additional event information.
    Fired when a <code>Field</code> receives keyboard focus.

    @since 6.2
    """
    # Identifier for event that can be used in {@link EventRouter}
    EVENT_ID = EventId.FOCUS

    def __init__(self, source):
        super(FocusEvent, self)(source)

class FocusListener(ComponentEventListener):
    """<code>FocusListener</code> interface for listening for
    <code>FocusEvent</code> fired by a <code>Field</code>.

    @see FocusEvent
    @since 6.2
    """
    focusMethod = ReflectTools.findMethod(FocusListener, 'focus', FocusEvent)

    def focus(self, event):
        """Component has been focused

        @param event
                   Component focus event.
        """
        pass

class BlurEvent(Component.Event):
    """<code>BlurEvent</code> class for holding additional event information.
    Fired when a <code>Field</code> loses keyboard focus.

    @since 6.2
    """
    # Identifier for event that can be used in {@link EventRouter}
    EVENT_ID = EventId.BLUR

    def __init__(self, source):
        super(BlurEvent, self)(source)

class BlurListener(ComponentEventListener):
    """<code>BlurListener</code> interface for listening for
    <code>BlurEvent</code> fired by a <code>Field</code>.

    @see BlurEvent
    @since 6.2
    """
    blurMethod = ReflectTools.findMethod(BlurListener, 'blur', BlurEvent)

    def blur(self, event):
        """Component has been blurred

        @param event
                   Component blur event.
        """
        pass

class TextChangeEvent(Component.Event):
    """TextChangeEvents are fired when the user is editing the text content of a
    field. Most commonly text change events are triggered by typing text with
    keyboard, but e.g. pasting content from clip board to a text field also
    triggers an event.
    <p>
    TextChangeEvents differ from {@link ValueChangeEvent}s so that they are
    triggered repeatedly while the end user is filling the field.
    ValueChangeEvents are not fired until the user for example hits enter or
    focuses another field. Also note the difference that TextChangeEvents are
    only fired if the change is triggered from the user, while
    ValueChangeEvents are also fired if the field value is set by the
    application code.
    <p>
    The {@link TextChangeNotifier}s implementation may decide when exactly
    TextChangeEvents are fired. TextChangeEvents are not necessary fire for
    example on each key press, but buffered with a small delay. The
    {@link TextField} component supports different modes for triggering
    TextChangeEvents.

    @see TextChangeListener
    @see TextChangeNotifier
    @see TextField#setTextChangeEventMode(com.vaadin.ui.TextField.TextChangeEventMode)
    @since 6.5
    """

    def __init__(self, source):
        super(TextChangeEvent, self)(source)

    def getText(self):
        """@return the text content of the field after the
                {@link TextChangeEvent}
        """
        pass

    def getCursorPosition(self):
        """@return the cursor position during after the {@link TextChangeEvent}"""
        pass

class TextChangeListener(ComponentEventListener):
    """A listener for {@link TextChangeEvent}s.

    @since 6.5
    """
    EVENT_ID = 'ie'
    EVENT_METHOD = ReflectTools.findMethod(TextChangeListener, 'textChange', TextChangeEvent)

    def textChange(self, event):
        """This method is called repeatedly while the text is edited by a user.

        @param event
                   the event providing details of the text change
        """
        pass

class TextChangeNotifier(Serializable):
    """An interface implemented by a {@link Field} supporting
    {@link TextChangeEvent}s. An example a {@link TextField} supports
    {@link TextChangeListener}s.
    """

    def addListener(self, listener):
        pass

    def removeListener(self, listener):
        pass
