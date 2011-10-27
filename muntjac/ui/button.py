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

from warnings import warn

from muntjac.ui.abstract_field import AbstractField
from muntjac.ui.component import Event as ComponentEvent
from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.data.property import IProperty

from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails

from muntjac.event.field_events import \
    (BlurEvent, IBlurListener, IBlurNotifier, FocusEvent,
    IFocusListener, IFocusNotifier)

from muntjac.ui.abstract_component import AbstractComponent


class IClickListener(object):
    """Interface for listening for a {@link ClickEvent} fired by a
    {@link Component}.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def buttonClick(self, event):
        """Called when a {@link Button} has been clicked. A reference to
        the button is given by {@link ClickEvent#getButton()}.

        @param event
                   An event containing information about the click.
        """
        raise NotImplementedError


_BUTTON_CLICK_METHOD = getattr(IClickListener, "buttonClick")


class Button(AbstractField, IBlurNotifier, IFocusNotifier):
    """A generic button component.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    CLIENT_WIDGET = None #ClientWidget(VButton, LoadStyle.EAGER)

    def __init__(self, *args):
        """Creates a new push button. The value of the push button is false
        and it is immediate by default.
        ---
        Creates a new push button.

        The value of the push button is false and it is immediate by default.

        @param caption
                   the Button caption.
        ---
        Creates a new push button with click listener.

        @param caption
                   the Button caption.
        @param listener
                   the Button click listener.
        ---
        Creates a new push button with a method listening button clicks. Using
        this method is discouraged because it cannot be checked during
        compilation. Use
        {@link #Button(String, com.vaadin.ui.Button.ClickListener)} instead.
        The method must have either no parameters, or only one parameter of
        Button.ClickEvent type.

        @param caption
                   the Button caption.
        @param target
                   the Object having the method for listening button clicks.
        @param methodName
                   the name of the method in target object, that receives
                   button click events.
        ---
        Creates a new switch button with initial value.

        @param state
                   the Initial state of the switch-button.
        @param initialState
        @deprecated use {@link CheckBox} instead of Button in "switchmode"
        ---
        Creates a new switch button that is connected to a boolean property.

        @param state
                   the Initial state of the switch-button.
        @param dataSource
        @deprecated use {@link CheckBox} instead of Button in "switchmode"
        """
        super(Button, self).__init__()

        self._switchMode = False
        self.clickShortcut = None

        nargs = len(args)
        if nargs == 0:
            self.setValue(False)
        elif nargs == 1:
            caption, = args
            Button.__init__(self)
            self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IClickListener):
                caption, listener = args
                Button.__init__(self, caption)
                self.addListener(listener, IClickListener)
            elif isinstance(args[1], IProperty):
                caption, dataSource = args
                self.setCaption(caption)
                self.setSwitchMode(True)
                self.setPropertyDataSource(dataSource)
            else:
                caption, initialState = args
                self.setCaption(caption)
                self.setValue(bool(initialState))
                self.setSwitchMode(True)
        elif nargs == 3:
            caption, target, methodName = args
            Button.__init__(self, caption)
            self.registerListener(ClickEvent, target, methodName)
        else:
            raise ValueError, 'too many arguments'


    def paintContent(self, target):
        """Paints the content of this component.

        @param event
                   the PaintEvent.
        @throws IOException
                    if the writing failed due to input/output error.
        @throws PaintException
                    if the paint operation failed.
        """
        super(Button, self).paintContent(target)

        if self.isSwitchMode():
            target.addAttribute('type', 'switch')

        target.addVariable(self, 'state', self.booleanValue())

        if self.clickShortcut is not None:
            target.addAttribute('keycode', self.clickShortcut.getKeyCode())


    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed. Button
        listeners are notified if the button is clicked.

        @param source
        @param variables
        """
        super(Button, self).changeVariables(source, variables)

        if not self.isReadOnly() and 'state' in variables:
            # Gets the new and old button states
            newValue = variables.get('state')
            oldValue = self.getValue()

            if self.isSwitchMode():
                # For switch button, the event is only sent if the
                # switch state is changed
                if (newValue is not None and newValue != oldValue
                        and not self.isReadOnly()):
                    self.setValue(newValue)
                    if 'mousedetails' in variables:
                        self.fireClick(MouseEventDetails.deSerialize(
                                variables.get('mousedetails')))
                    else:
                        # for compatibility with custom implementations
                        # which don't send mouse details
                        self.fireClick()
            else:
                # Only send click event if the button is pushed
                if bool(newValue):
                    if 'mousedetails' in variables:
                        self.fireClick(MouseEventDetails.deSerialize(
                                variables.get('mousedetails')))
                    else:
                        # for compatibility with custom implementations
                        # which don't send mouse details
                        self.fireClick()

                # If the button is true for some reason, release it
                if oldValue is None or bool(oldValue):
                    self.setValue(False)

        if FocusEvent.EVENT_ID in variables:
            self.fireEvent( FocusEvent(self) )

        if BlurEvent.EVENT_ID in variables:
            self.fireEvent( BlurEvent(self) )


    def isSwitchMode(self):
        """Checks if it is switchMode.

        @return <code>true</code> if it is in Switch Mode, otherwise
                <code>false</code>.
        @deprecated the {@link CheckBox} component should be used instead
                    of Button in switch mode
        """
        warn('use CheckBox instead', DeprecationWarning)
        return self._switchMode


    def setSwitchMode(self, switchMode):
        """Sets the switchMode.

        @param switchMode
                   The switchMode to set.
        @deprecated the {@link CheckBox} component should be used instead
                    of Button in switch mode
        """
        self._switchMode = switchMode
        if not switchMode:
            self.setImmediate(True)
            if self.booleanValue():
                self.setValue(False)


    def booleanValue(self):
        """Get the boolean value of the button state.

        @return True iff the button is pressed down or checked.
        """
        value = self.getValue()
        return False if value is None else bool(value)


    def setImmediate(self, immediate):
        """Sets immediate mode. Push buttons can not be set in
        non-immediate mode.

        @see AbstractComponent.setImmediate
        """
        # Push buttons are always immediate
        super(Button, self).setImmediate(
                (not self.isSwitchMode()) or immediate)


    def getType(self):
        """The type of the button as a property.

        @see com.vaadin.data.IProperty#getType()
        """
        return bool

    # Button style with no decorations. Looks like a link, acts like a button
    # @deprecated use {@link BaseTheme#BUTTON_LINK} instead.
    STYLE_LINK = 'link'


    def addListener(self, listener, iface):
        """Adds the button click listener.

        @param listener
                   the Listener to be added.
        """
        if iface == IBlurListener:
            self.registerListener(BlurEvent.EVENT_ID, BlurEvent,
                    listener, IBlurListener.blurMethod)

        elif iface == IClickListener:
            self.registerListener(ClickEvent, listener, _BUTTON_CLICK_METHOD)

        elif iface == IFocusListener:
            self.registerListener(FocusEvent.EVENT_ID, FocusEvent,
                    listener, IFocusListener.focusMethod)

        else:
            super(Button, self).addListener(listener, iface)


    def addBlurListener(self, listener):
        self.addListener(listener, IBlurListener)


    def addClickListener(self, listener):
        self.addListener(listener, IClickListener)


    def addFocusListener(self, listener):
        self.addListener(listener, IFocusListener)


    def removeListener(self, listener, iface):
        """Removes the button click listener.

        @param listener
                   the Listener to be removed.
        """
        if iface == IBlurListener:
            self.withdrawListener(BlurEvent.EVENT_ID, BlurEvent, listener)

        elif iface == IClickListener:
            self.withdrawListener(ClickEvent, listener, _BUTTON_CLICK_METHOD)

        elif iface == IFocusListener:
            self.withdrawListener(FocusEvent.EVENT_ID, FocusEvent, listener)

        else:
            super(Button, self).removeListener(listener, iface)


    def removeBlurListener(self, listener):
        self.removeListener(listener, IBlurListener)


    def removeClickListener(self, listener):
        self.removeListener(listener, IClickListener)


    def removeFocusListener(self, listener):
        self.removeListener(listener, IFocusListener)


    def fireClick(self, details=None):
        """Fires a click event to all listeners without any event details.

        In subclasses, override {@link #fireClick(MouseEventDetails)} instead
        of this method.
        ---
        Fires a click event to all listeners.

        @param details
                   MouseEventDetails from which keyboard modifiers and other
                   information about the mouse click can be obtained. If the
                   button was clicked by a keyboard event, some of the fields
                   may be empty/undefined.
        """
        if details is None:
            self.fireEvent( ClickEvent(self) )
        else:
            self.fireEvent( ClickEvent(self, details) )


    def setInternalValue(self, newValue):
        # Make sure only booleans get through
        if newValue is not None and not isinstance(newValue, bool):
            raise ValueError, (self.__class__.__name__ +
                    ' only accepts Boolean values')

        super(Button, self).setInternalValue(newValue)


    def setClickShortcut(self, keyCode, *modifiers):
        """Makes it possible to invoke a click on this button by pressing
        the given {@link KeyCode} and (optional) {@link ModifierKey}s.

        The shortcut is global (bound to the containing Window).

        @param keyCode
                   the keycode for invoking the shortcut
        @param modifiers
                   the (optional) modifiers for invoking the shortcut, null
                   for none
        """
        if self.clickShortcut is not None:
            self.removeShortcutListener(self.clickShortcut)

        self.clickShortcut = ClickShortcut(self, keyCode, modifiers)
        self.addShortcutListener(self.clickShortcut)


    def removeClickShortcut(self):
        """Removes the keyboard shortcut previously set with
        {@link #setClickShortcut(int, int...)}.
        """
        if self.clickShortcut is not None:
            self.removeShortcutListener(self.clickShortcut)
            self.clickShortcut = None


class ClickShortcut(ShortcutListener):
    """A {@link ShortcutListener} specifically made to define a keyboard
    shortcut that invokes a click on the given button.
    """

    def __init__(self, *args):
        """Creates a keyboard shortcut for clicking the given button using
        the shorthand notation defined in {@link ShortcutAction}.

        @param button
                   to be clicked when the shortcut is invoked
        @param shorthandCaption
                   the caption with shortcut keycode and modifiers indicated
        ---
        Creates a keyboard shortcut for clicking the given button using the
        given {@link KeyCode} and {@link ModifierKey}s.

        @param button
                   to be clicked when the shortcut is invoked
        @param keyCode
                   KeyCode to react to
        @param modifiers
                   optional modifiers for shortcut
        ---
        Creates a keyboard shortcut for clicking the given button using the
        given {@link KeyCode}.

        @param button
                   to be clicked when the shortcut is invoked
        @param keyCode
                   KeyCode to react to
        """
        args = args
        nargs = len(args)
        if nargs == 2:
            if isinstance(args[1], int):
                button, keyCode = args
                ClickShortcut.__init__(self, button, keyCode, None)
            else:
                button, shorthandCaption = args
                super(ClickShortcut, self).__init__(shorthandCaption)
                self.button = button
        elif nargs >= 3:
            button, keyCode = args[:2]
            modifiers = args[2:]
            super(ClickShortcut, self).__init__(None, keyCode, modifiers)
            self.button = button
        else:
            raise ValueError, 'too few arguments'


    def handleAction(self, sender, target):
        if self.button.isEnabled() and not self.button.isReadOnly():
            self.button.fireClick()


class ClickEvent(ComponentEvent):
    """Click event. This event is thrown, when the button is clicked.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """
    _details = None

    def __init__(self, source, details=None):
        """New instance of text change event.

        @param source
                   the Source of the event.
        ---
        Constructor with mouse details

        @param source
                   The source where the click took place
        @param details
                   Details about the mouse click
        """
        super(ClickEvent, self).__init__(source)
        self._details = details


    def getButton(self):
        """Gets the Button where the event occurred.

        @return the Source of the event.
        """
        return self.getSource()


    def getClientX(self):
        """Returns the mouse position (x coordinate) when the click took
        place. The position is relative to the browser client area.

        @return The mouse cursor x position or -1 if unknown
        """
        if None is not self._details:
            return self._details.getClientX()
        else:
            return -1


    def getClientY(self):
        """Returns the mouse position (y coordinate) when the click took
        place. The position is relative to the browser client area.

        @return The mouse cursor y position or -1 if unknown
        """
        if None is not self._details:
            return self._details.getClientY()
        else:
            return -1


    def getRelativeX(self):
        """Returns the relative mouse position (x coordinate) when the click
        took place. The position is relative to the clicked component.

        @return The mouse cursor x position relative to the clicked layout
                component or -1 if no x coordinate available
        """
        if None is not self._details:
            return self._details.getRelativeX()
        else:
            return -1


    def getRelativeY(self):
        """Returns the relative mouse position (y coordinate) when the click
        took place. The position is relative to the clicked component.

        @return The mouse cursor y position relative to the clicked layout
                component or -1 if no y coordinate available
        """
        if None is not self._details:
            return self._details.getRelativeY()
        else:
            return -1


    def isAltKey(self):
        """Checks if the Alt key was down when the mouse event took place.

        @return true if Alt was down when the event occured, false
                otherwise or if unknown
        """
        if None is not self._details:
            return self._details.isAltKey()
        else:
            return False


    def isCtrlKey(self):
        """Checks if the Ctrl key was down when the mouse event took place.

        @return true if Ctrl was pressed when the event occured, false
                otherwise or if unknown
        """
        if None is not self._details:
            return self._details.isCtrlKey()
        else:
            return False


    def isMetaKey(self):
        """Checks if the Meta key was down when the mouse event took place.

        @return true if Meta was pressed when the event occurred, false
                otherwise or if unknown
        """
        if None is not self._details:
            return self._details.isMetaKey()
        else:
            return False


    def isShiftKey(self):
        """Checks if the Shift key was down when the mouse event took place.

        @return true if Shift was pressed when the event occurred, false
                otherwise or if unknown
        """
        if None is not self._details:
            return self._details.isShiftKey()
        else:
            return False
