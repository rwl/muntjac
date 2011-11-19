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

"""Interface for adding and removing C{FocusEvent} listeners."""

from muntjac.terminal.gwt.client.event_id import EventId
from muntjac.event.component_event_listener import IComponentEventListener
from muntjac.ui.component import Event as ComponentEvent


class IFocusNotifier(object):
    """The interface for adding and removing C{FocusEvent} listeners.
    By implementing this interface a class explicitly announces that it will
    generate a C{FocusEvent} when it receives keyboard focus.

    @see: L{IFocusListener}
    @see: L{FocusEvent}
    """

    def addListener(self, listener, iface=None):
        """Adds a C{IFocusListener} to the Component which gets fired
        when a C{Field} receives keyboard focus.

        @see: L{IFocusListener}
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Removes a C{IFocusListener} from the Component.

        @see: L{IFocusListener}
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


class IBlurNotifier(object):
    """The interface for adding and removing C{BlurEvent} listeners.
    By implementing this interface a class explicitly announces that it will
    generate a C{BlurEvent} when it loses keyboard focus.

    @see: L{IBlurListener}
    @see: L{BlurEvent}
    """

    def addListener(self, listener, iface=None):
        """Adds a C{IBlurListener} to the Component which gets fired
        when a C{Field} loses keyboard focus.

        @see: L{IBlurListener}
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Removes a C{IBlurListener} from the Component.

        @see: L{IBlurListener}
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


class FocusEvent(ComponentEvent):
    """C{FocusEvent} class for holding additional event information.
    Fired when a C{Field} receives keyboard focus.
    """
    # Identifier for event that can be used in L{EventRouter}
    EVENT_ID = EventId.FOCUS

    def __init__(self, source):
        super(FocusEvent, self).__init__(source)


class IFocusListener(IComponentEventListener):
    """C{IFocusListener} interface for listening for C{FocusEvent} fired by
    a C{Field}.

    @see: FocusEvent
    """

    def focus(self, event):
        """Component has been focused

        @param event:
                   Component focus event.
        """
        raise NotImplementedError

    focusMethod = focus


class BlurEvent(ComponentEvent):
    """C{BlurEvent} class for holding additional event information.
    Fired when a C{Field} loses keyboard focus.
    """

    # Identifier for event that can be used in L{EventRouter}
    EVENT_ID = EventId.BLUR

    def __init__(self, source):
        super(BlurEvent, self).__init__(source)


class IBlurListener(IComponentEventListener):
    """C{IBlurListener} interface for listening for C{BlurEvent} fired by
    a C{Field}.

    @see: BlurEvent
    """

    def blur(self, event):
        """Component has been blurred

        @param event:
                   Component blur event.
        """
        raise NotImplementedError

    blurMethod = blur


class TextChangeEvent(ComponentEvent):
    """TextChangeEvents are fired when the user is editing the text content of
    a field. Most commonly text change events are triggered by typing text with
    keyboard, but e.g. pasting content from clip board to a text field also
    triggers an event.

    TextChangeEvents differ from L{ValueChangeEvent}s so that they are
    triggered repeatedly while the end user is filling the field.
    ValueChangeEvents are not fired until the user for example hits enter or
    focuses another field. Also note the difference that TextChangeEvents are
    only fired if the change is triggered from the user, while
    ValueChangeEvents are also fired if the field value is set by the
    application code.

    The L{ITextChangeNotifier}s implementation may decide when exactly
    TextChangeEvents are fired. TextChangeEvents are not necessary fire for
    example on each key press, but buffered with a small delay. The
    L{TextField} component supports different modes for triggering
    TextChangeEvents.

    @see: L{ITextChangeListener}
    @see: L{ITextChangeNotifier}
    @see: TextField.setTextChangeEventMode
    """

    def __init__(self, source):
        super(TextChangeEvent, self).__init__(source)


    def getText(self):
        """@return: the text content of the field after the
                L{TextChangeEvent}
        """
        pass


    def getCursorPosition(self):
        """@return: the cursor position during after the
        L{TextChangeEvent}"""
        pass


class ITextChangeListener(IComponentEventListener):
    """A listener for L{TextChangeEvent}s.
    """

    EVENT_ID = 'ie'

    def textChange(self, event):
        """This method is called repeatedly while the text is edited by a
        user.

        @param event:
                   the event providing details of the text change
        """
        raise NotImplementedError


EVENT_METHOD = ITextChangeListener.textChange


class ITextChangeNotifier(object):
    """An interface implemented by a L{Field} supporting
    L{TextChangeEvent}s. An example a L{TextField} supports
    L{ITextChangeListener}s.
    """

    def addListener(self, listener, iface=None):
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError
