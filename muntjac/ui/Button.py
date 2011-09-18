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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.event.FieldEvents import (BlurEvent, BlurListener, BlurNotifier, FieldEvents, FocusEvent, FocusListener, FocusNotifier,)
from com.vaadin.ui.AbstractField import (AbstractField,)
from com.vaadin.event.ShortcutListener import (ShortcutListener,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
# from com.vaadin.event.ShortcutAction.KeyCode import (KeyCode,)
# from com.vaadin.event.ShortcutAction.ModifierKey import (ModifierKey,)
# from java.io.IOException import (IOException,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.util.Map import (Map,)


class Button(AbstractField, FieldEvents, BlurNotifier, FieldEvents, FocusNotifier):
    """A generic button component.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Private members
    _switchMode = False

    def __init__(self, *args):
        """Creates a new push button. The value of the push button is false and it
        is immediate by default.
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
        {@link #Button(String, com.vaadin.ui.Button.ClickListener)} instead. The
        method must have either no parameters, or only one parameter of
        Button.ClickEvent type.

        @param caption
                   the Button caption.
        @param target
                   the Object having the method for listening button clicks.
        @param methodName
                   the name of the method in target object, that receives button
                   click events.
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
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setValue(Boolean.FALSE.FALSE)
        elif _1 == 1:
            caption, = _0
            self.__init__()
            self.setCaption(caption)
        elif _1 == 2:
            if isinstance(_0[1], ClickListener):
                caption, listener = _0
                self.__init__(caption)
                self.addListener(listener)
            elif isinstance(_0[1], Property):
                caption, dataSource = _0
                self.setCaption(caption)
                self.setSwitchMode(True)
                self.setPropertyDataSource(dataSource)
            else:
                caption, initialState = _0
                self.setCaption(caption)
                self.setValue(Boolean.valueOf.valueOf(initialState))
                self.setSwitchMode(True)
        elif _1 == 3:
            caption, target, methodName = _0
            self.__init__(caption)
            self.addListener(self.ClickEvent, target, methodName)
        else:
            raise ARGERROR(0, 3)

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
        """Invoked when the value of a variable has changed. Button listeners are
        notified if the button is clicked.

        @param source
        @param variables
        """
        super(Button, self).changeVariables(source, variables)
        if not self.isReadOnly() and 'state' in variables:
            # Gets the new and old button states
            newValue = variables['state']
            oldValue = self.getValue()
            if self.isSwitchMode():
                # For switch button, the event is only sent if the
                # switch state is changed
                if (
                    newValue is not None and not (newValue == oldValue) and not self.isReadOnly()
                ):
                    self.setValue(newValue)
                    if 'mousedetails' in variables:
                        self.fireClick(MouseEventDetails.deSerialize(variables['mousedetails']))
                    else:
                        # for compatibility with custom implementations which
                        # don't send mouse details
                        self.fireClick()
            else:
                # Only send click event if the button is pushed
                if newValue.booleanValue():
                    if 'mousedetails' in variables:
                        self.fireClick(MouseEventDetails.deSerialize(variables['mousedetails']))
                    else:
                        # for compatibility with custom implementations which
                        # don't send mouse details
                        self.fireClick()
                # If the button is true for some reason, release it
                if (None is oldValue) or oldValue.booleanValue():
                    self.setValue(Boolean.FALSE.FALSE)
        if FocusEvent.EVENT_ID in variables:
            self.fireEvent(FocusEvent(self))
        if BlurEvent.EVENT_ID in variables:
            self.fireEvent(BlurEvent(self))

    def isSwitchMode(self):
        """Checks if it is switchMode.

        @return <code>true</code> if it is in Switch Mode, otherwise
                <code>false</code>.
        @deprecated the {@link CheckBox} component should be used instead of
                    Button in switch mode
        """
        return self._switchMode

    def setSwitchMode(self, switchMode):
        """Sets the switchMode.

        @param switchMode
                   The switchMode to set.
        @deprecated the {@link CheckBox} component should be used instead of
                    Button in switch mode
        """
        self._switchMode = switchMode
        if not switchMode:
            self.setImmediate(True)
            if self.booleanValue():
                self.setValue(Boolean.FALSE.FALSE)

    def booleanValue(self):
        """Get the boolean value of the button state.

        @return True iff the button is pressed down or checked.
        """
        value = self.getValue()
        return False if None is value else value.booleanValue()

    def setImmediate(self, immediate):
        """Sets immediate mode. Push buttons can not be set in non-immediate mode.

        @see com.vaadin.ui.AbstractComponent#setImmediate(boolean)
        """
        # Push buttons are always immediate
        super(Button, self).setImmediate((not self.isSwitchMode()) or immediate)

    def getType(self):
        """The type of the button as a property.

        @see com.vaadin.data.Property#getType()
        """
        # Click event
        return bool

    _BUTTON_CLICK_METHOD = None
    # Button style with no decorations. Looks like a link, acts like a button
    # 
    # @deprecated use {@link BaseTheme#BUTTON_LINK} instead.

    STYLE_LINK = 'link'
    # This should never happen
    try:
        _BUTTON_CLICK_METHOD = self.ClickListener.getDeclaredMethod('buttonClick', [self.ClickEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in Button')

    class ClickEvent(Component.Event):
        """Click event. This event is thrown, when the button is clicked.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _details = None

        def __init__(self, *args):
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
            _0 = args
            _1 = len(args)
            if _1 == 1:
                source, = _0
                super(ClickEvent, self)(source)
                self._details = None
            elif _1 == 2:
                source, details = _0
                super(ClickEvent, self)(source)
                self._details = details
            else:
                raise ARGERROR(1, 2)

        def getButton(self):
            """Gets the Button where the event occurred.

            @return the Source of the event.
            """
            return self.getSource()

        def getClientX(self):
            """Returns the mouse position (x coordinate) when the click took place.
            The position is relative to the browser client area.

            @return The mouse cursor x position or -1 if unknown
            """
            if None is not self._details:
                return self._details.getClientX()
            else:
                return -1

        def getClientY(self):
            """Returns the mouse position (y coordinate) when the click took place.
            The position is relative to the browser client area.

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

            @return true if Alt was down when the event occured, false otherwise
                    or if unknown
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

            @return true if Meta was pressed when the event occured, false
                    otherwise or if unknown
            """
            if None is not self._details:
                return self._details.isMetaKey()
            else:
                return False

        def isShiftKey(self):
            """Checks if the Shift key was down when the mouse event took place.

            @return true if Shift was pressed when the event occured, false
                    otherwise or if unknown
            """
            if None is not self._details:
                return self._details.isShiftKey()
            else:
                return False

    class ClickListener(Serializable):
        """Interface for listening for a {@link ClickEvent} fired by a
        {@link Component}.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """

        def buttonClick(self, event):
            """Called when a {@link Button} has been clicked. A reference to the
            button is given by {@link ClickEvent#getButton()}.

            @param event
                       An event containing information about the click.
            """
            pass

    def addListener(self, *args):
        """Adds the button click listener.

        @param listener
                   the Listener to be added.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.addListener(BlurEvent.EVENT_ID, BlurEvent, listener, BlurListener.blurMethod)
            elif isinstance(_0[0], ClickListener):
                listener, = _0
                self.addListener(self.ClickEvent, listener, self._BUTTON_CLICK_METHOD)
            else:
                listener, = _0
                self.addListener(FocusEvent.EVENT_ID, FocusEvent, listener, FocusListener.focusMethod)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Removes the button click listener.

        @param listener
                   the Listener to be removed.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.removeListener(BlurEvent.EVENT_ID, BlurEvent, listener)
            elif isinstance(_0[0], ClickListener):
                listener, = _0
                self.removeListener(self.ClickEvent, listener, self._BUTTON_CLICK_METHOD)
            else:
                listener, = _0
                self.removeListener(FocusEvent.EVENT_ID, FocusEvent, listener)
        else:
            raise ARGERROR(1, 1)

    def fireClick(self, *args):
        """Fires a click event to all listeners without any event details.

        In subclasses, override {@link #fireClick(MouseEventDetails)} instead of
        this method.
        ---
        Fires a click event to all listeners.

        @param details
                   MouseEventDetails from which keyboard modifiers and other
                   information about the mouse click can be obtained. If the
                   button was clicked by a keyboard event, some of the fields may
                   be empty/undefined.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.fireEvent(Button.ClickEvent(self))
        elif _1 == 1:
            details, = _0
            self.fireEvent(Button.ClickEvent(self, details))
        else:
            raise ARGERROR(0, 1)

    def setInternalValue(self, newValue):
        # Make sure only booleans get through
        if None is not newValue and not isinstance(newValue, bool):
            raise self.IllegalArgumentException(self.getClass().getSimpleName() + ' only accepts Boolean values')
        super(Button, self).setInternalValue(newValue)

    # Actions
    clickShortcut = None

    def setClickShortcut(self, keyCode, *modifiers):
        """Makes it possible to invoke a click on this button by pressing the given
        {@link KeyCode} and (optional) {@link ModifierKey}s.<br/>
        The shortcut is global (bound to the containing Window).

        @param keyCode
                   the keycode for invoking the shortcut
        @param modifiers
                   the (optional) modifiers for invoking the shortcut, null for
                   none
        """
        if self.clickShortcut is not None:
            self.removeShortcutListener(self.clickShortcut)
        self.clickShortcut = self.ClickShortcut(self, keyCode, modifiers)
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
        button = None

        def __init__(self, *args):
            """Creates a keyboard shortcut for clicking the given button using the
            shorthand notation defined in {@link ShortcutAction}.

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
            _0 = args
            _1 = len(args)
            if _1 == 2:
                if isinstance(_0[1], int):
                    button, keyCode = _0
                    self.__init__(button, keyCode, None)
                else:
                    button, shorthandCaption = _0
                    super(ClickShortcut, self)(shorthandCaption)
                    self.button = button
            elif _1 == 3:
                button, keyCode, modifiers = _0
                super(ClickShortcut, self)(None, keyCode, modifiers)
                self.button = button
            else:
                raise ARGERROR(2, 3)

        def handleAction(self, sender, target):
            if self.button.isEnabled() and not self.button.isReadOnly():
                self.button.fireClick()
