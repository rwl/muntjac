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

from muntjac.ui.Component import Component
from muntjac.event.MethodEventSource import MethodEventSource
from muntjac.terminal.gwt.server.ComponentSizeValidator import ComponentSizeValidator
from muntjac.event.EventRouter import EventRouter
from muntjac.terminal.Terminal import ErrorEvent as TerminalErrorEvent


class AbstractComponent(Component, MethodEventSource):
    """An abstract class that defines default implementation for the
    {@link Component} interface. Basic UI components that are not derived from an
    external component can inherit this class to easily qualify as Vaadin
    components. Most components in Vaadin do just that.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Private members
    # Style names.
    _styles = None
    # Caption text.
    _caption = None
    # Application specific data object. The component does not use or modify
    # this.

    _applicationData = None
    # Icon to be shown together with caption.
    _icon = None
    # Is the component enabled (its normal usage is allowed).
    _enabled = True
    # Is the component visible (it is rendered).
    _visible = True
    # Is the component read-only ?
    _readOnly = False
    # Description of the usage (XML).
    _description = None
    # The container this component resides in.
    _parent = None
    # The EventRouter used for the event model.
    _eventRouter = None
    # A set of event identifiers with registered listeners.
    _eventIdentifiers = None
    # The internal error message of the component.
    _componentError = None
    # Immediate mode: if true, all variable changes are required to be sent
    # from the terminal immediately.

    _immediate = False
    # Locale of this component.
    _locale = None
    # The component should receive focus (if {@link Focusable}) when attached.
    _delayedFocus = None
    # List of repaint request listeners or null if not listened at all.
    _repaintRequestListeners = None
    # Are all the repaint listeners notified about recent changes ?
    _repaintRequestListenersNotified = False
    _testingId = None
    # Sizeable fields
    _width = SIZE_UNDEFINED
    _height = SIZE_UNDEFINED
    _widthUnit = UNITS_PIXELS
    _heightUnit = UNITS_PIXELS
    _sizePattern = Pattern.compile('^(-?\\d+(\\.\\d+)?)(%|px|em|ex|in|cm|mm|pt|pc)?$')
    _errorHandler = None
    # Constructor

    def __init__(self):
        """Constructs a new Component."""
        # ComponentSizeValidator.setCreationLocation(this);
        # Get/Set component properties
        pass

    def getTag(self):
        """Gets the UIDL tag corresponding to the component.

        <p>
        Note! In version 6.2 the method for mapping server side components to
        their client side counterparts was enhanced. This method was made final
        to intentionally "break" code where it is needed. If your code does not
        compile due overriding this method, it is very likely that you need to:
        <ul>
        <li>remove the implementation of getTag
        <li>add {@link ClientWidget} annotation to your component
        </ul>

        @return the component's UIDL tag as <code>String</code>
        @deprecated tags are no more required for components. Instead of tags we
                    are now using {@link ClientWidget} annotations to map server
                    side components to client side counterparts. Generating
                    identifier for component type is delegated to terminal.
        @see ClientWidget
        """
        return ''

    def setDebugId(self, id):
        self._testingId = id

    def getDebugId(self):
        return self._testingId

    def getStyle(self):
        """Gets style for component. Multiple styles are joined with spaces.

        @return the component's styleValue of property style.
        @deprecated Use getStyleName() instead; renamed for consistency and to
                    indicate that "style" should not be used to switch client
                    side implementation, only to style the component.
        """
        return self.getStyleName()

    def setStyle(self, style):
        """Sets and replaces all previous style names of the component. This method
        will trigger a {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param style
                   the new style of the component.
        @deprecated Use setStyleName() instead; renamed for consistency and to
                    indicate that "style" should not be used to switch client
                    side implementation, only to style the component.
        """
        # Gets the component's style. Don't add a JavaDoc comment here, we use the
        # default documentation from implemented interface.

        self.setStyleName(style)

    def getStyleName(self):
        # Sets the component's style. Don't add a JavaDoc comment here, we use the
        # default documentation from implemented interface.

        s = ''
        if self._styles is not None:
            _0 = True
            it = self._styles
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                s += it.next()
                if it.hasNext():
                    s += ' '
        return s

    def setStyleName(self, style):
        if (style is None) or ('' == style):
            self._styles = None
            self.requestRepaint()
            return
        if self._styles is None:
            self._styles = list()
        self._styles.clear()
        self._styles.add(style)
        self.requestRepaint()

    def addStyleName(self, style):
        if (style is None) or ('' == style):
            return
        if self._styles is None:
            self._styles = list()
        if not self._styles.contains(style):
            self._styles.add(style)
            self.requestRepaint()

    def removeStyleName(self, style):
        # Get's the component's caption. Don't add a JavaDoc comment here, we use
        # the default documentation from implemented interface.

        if self._styles is not None:
            self._styles.remove(style)
            self.requestRepaint()

    def getCaption(self):
        return self._caption

    def setCaption(self, caption):
        """Sets the component's caption <code>String</code>. Caption is the visible
        name of the component. This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param caption
                   the new caption <code>String</code> for the component.
        """
        # Don't add a JavaDoc comment here, we use the default documentation from
        # implemented interface.

        self._caption = caption
        self.requestRepaint()

    def getLocale(self):
        if self._locale is not None:
            return self._locale
        if self._parent is not None:
            return self._parent.getLocale()
        app = self.getApplication()
        if app is not None:
            return app.getLocale()
        return None

    def setLocale(self, locale):
        """Sets the locale of this component.

        <pre>
        // Component for which the locale is meaningful
        InlineDateField date = new InlineDateField(&quot;Datum&quot;);

        // German language specified with ISO 639-1 language
        // code and ISO 3166-1 alpha-2 country code.
        date.setLocale(new Locale(&quot;de&quot;, &quot;DE&quot;));

        date.setResolution(DateField.RESOLUTION_DAY);
        layout.addComponent(date);
        </pre>


        @param locale
                   the locale to become this component's locale.
        """
        # Gets the component's icon resource. Don't add a JavaDoc comment here, we
        # use the default documentation from implemented interface.

        self._locale = locale
        self.requestRepaint()

    def getIcon(self):
        return self._icon

    def setIcon(self, icon):
        """Sets the component's icon. This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param icon
                   the icon to be shown with the component's caption.
        """
        # Tests if the component is enabled or not. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        self._icon = icon
        self.requestRepaint()

    def isEnabled(self):
        # Enables or disables the component. Don't add a JavaDoc comment here, we
        # use the default documentation from implemented interface.

        return self._enabled and (self._parent is None) or self._parent.isEnabled() and self.isVisible()

    def setEnabled(self, enabled):
        # Tests if the component is in the immediate mode. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._enabled != enabled:
            wasEnabled = self._enabled
            wasEnabledInContext = self.isEnabled()
            self._enabled = enabled
            isEnabled = enabled
            isEnabledInContext = isEnabled()
            # If the actual enabled state (as rendered, in context) has not
            # changed we do not need to repaint except if the parent is
            # invisible.
            # If the parent is invisible we must request a repaint so the
            # component is repainted with the new enabled state when the parent
            # is set visible again. This workaround is needed as isEnabled
            # checks isVisible.
            needRepaint = (wasEnabledInContext != isEnabledInContext) or (wasEnabled != isEnabled and (self.getParent() is None) or (not self.getParent().isVisible()))
            if needRepaint:
                self.requestRepaint()

    def isImmediate(self):
        return self._immediate

    def setImmediate(self, immediate):
        """Sets the component's immediate mode to the specified status. This method
        will trigger a {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param immediate
                   the boolean value specifying if the component should be in the
                   immediate mode after the call.
        @see Component#isImmediate()
        """
        # (non-Javadoc)
        #
        # @see com.vaadin.ui.Component#isVisible()

        self._immediate = immediate
        self.requestRepaint()

    def isVisible(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.ui.Component#setVisible(boolean)

        return self._visible and (self.getParent() is None) or self.getParent().isVisible()

    def setVisible(self, visible):
        if self._visible != visible:
            self._visible = visible
            # Instead of requesting repaint normally we
            # fire the event directly to assure that the
            # event goes through event in the component might
            # now be invisible
            self.fireRequestRepaintEvent(None)

    def getDescription(self):
        """<p>
        Gets the component's description. The description can be used to briefly
        describe the state of the component to the user. The description string
        may contain certain XML tags:
        </p>

        <p>
        <table border=1>
        <tr>
        <td width=120><b>Tag</b></td>
        <td width=120><b>Description</b></td>
        <td width=120><b>Example</b></td>
        </tr>
        <tr>
        <td>&lt;b></td>
        <td>bold</td>
        <td><b>bold text</b></td>
        </tr>
        <tr>
        <td>&lt;i></td>
        <td>italic</td>
        <td><i>italic text</i></td>
        </tr>
        <tr>
        <td>&lt;u></td>
        <td>underlined</td>
        <td><u>underlined text</u></td>
        </tr>
        <tr>
        <td>&lt;br></td>
        <td>linebreak</td>
        <td>N/A</td>
        </tr>
        <tr>
        <td>&lt;ul><br>
        &lt;li>item1<br>
        &lt;li>item1<br>
        &lt;/ul></td>
        <td>item list</td>
        <td>
        <ul>
        <li>item1
        <li>item2
        </ul>
        </td>
        </tr>
        </table>
        </p>

        <p>
        These tags may be nested.
        </p>

        @return component's description <code>String</code>
        """
        return self._description

    def setDescription(self, description):
        """Sets the component's description. See {@link #getDescription()} for more
        information on what the description is. This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param description
                   the new description string for the component.
        """
        # Gets the component's parent component. Don't add a JavaDoc comment here,
        # we use the default documentation from implemented interface.

        self._description = description
        self.requestRepaint()

    def getParent(self):
        # Sets the parent component. Don't add a JavaDoc comment here, we use the
        # default documentation from implemented interface.

        return self._parent

    def setParent(self, parent):
        # If the parent is not changed, don't do anything
        if parent == self._parent:
            return
        if parent is not None and self._parent is not None:
            raise self.IllegalStateException(self.getClass().getName() + ' already has a parent.')
        # Send detach event if the component have been connected to a window
        if self.getApplication() is not None:
            self.detach()
        # Connect to new parent
        self._parent = parent
        # Send attach event if connected to a window
        if self.getApplication() is not None:
            self.attach()

    def getErrorMessage(self):
        """Gets the error message for this component.

        @return ErrorMessage containing the description of the error state of the
                component or null, if the component contains no errors. Extending
                classes should override this method if they support other error
                message types such as validation errors or buffering errors. The
                returned error message contains information about all the errors.
        """
        return self._componentError

    def getComponentError(self):
        """Gets the component's error message.

        @link Terminal.ErrorMessage#ErrorMessage(String, int)

        @return the component's error message.
        """
        return self._componentError

    def setComponentError(self, componentError):
        """Sets the component's error message. The message may contain certain XML
        tags, for more information see

        @link Component.ErrorMessage#ErrorMessage(String, int)

        @param componentError
                   the new <code>ErrorMessage</code> of the component.
        """
        # Tests if the component is in read-only mode. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        self._componentError = componentError
        self.fireComponentErrorEvent()
        self.requestRepaint()

    def isReadOnly(self):
        # Sets the component's read-only mode. Don't add a JavaDoc comment here, we
        # use the default documentation from implemented interface.

        return self._readOnly

    def setReadOnly(self, readOnly):
        # Gets the parent window of the component. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        self._readOnly = readOnly
        self.requestRepaint()

    def getWindow(self):
        # Notify the component that it's attached to a window. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._parent is None:
            return None
        else:
            return self._parent.getWindow()

    def attach(self):
        # Detach the component from application. Don't add a JavaDoc comment here,
        # we use the default documentation from implemented interface.

        self.requestRepaint()
        if not self._visible:
            # Bypass the repaint optimization in childRequestedRepaint method
            # when attaching. When reattaching (possibly moving) -> must
            # repaint

            self.fireRequestRepaintEvent(None)
        if self._delayedFocus:
            self.focus()

    def detach(self):
        pass

    def focus(self):
        """Sets the focus for this component if the component is {@link Focusable}."""
        # Gets the parent application of the component. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        if isinstance(self, Focusable):
            app = self.getApplication()
            if app is not None:
                self.getWindow().setFocusedComponent(self)
                self._delayedFocus = False
            else:
                self._delayedFocus = True

    def getApplication(self):
        # Component painting
        # Documented in super interface
        if self._parent is None:
            return None
        else:
            return self._parent.getApplication()

    def requestRepaintRequests(self):
        # Paints the component into a UIDL stream. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.

        self._repaintRequestListenersNotified = False

    def paint(self, target):
        tag = target.getTag(self)
        if (not target.startTag(self, tag)) or self._repaintRequestListenersNotified:
            # Paint the contents of the component
            # Only paint content of visible components.
            if self.isVisible():
                if (
                    self.getHeight() >= 0 and (self.getHeightUnits() != self.UNITS_PERCENTAGE) or ComponentSizeValidator.parentCanDefineHeight(self)
                ):
                    target.addAttribute('height', '' + self.getCSSHeight())
                if (
                    self.getWidth() >= 0 and (self.getWidthUnits() != self.UNITS_PERCENTAGE) or ComponentSizeValidator.parentCanDefineWidth(self)
                ):
                    target.addAttribute('width', '' + self.getCSSWidth())
                if self._styles is not None and len(self._styles) > 0:
                    target.addAttribute('style', self.getStyle())
                if self.isReadOnly():
                    target.addAttribute('readonly', True)
                if self.isImmediate():
                    target.addAttribute('immediate', True)
                if not self.isEnabled():
                    target.addAttribute('disabled', True)
                if self.getCaption() is not None:
                    target.addAttribute('caption', self.getCaption())
                if self.getIcon() is not None:
                    target.addAttribute('icon', self.getIcon())
                if self.getDescription() is not None and len(self.getDescription()) > 0:
                    target.addAttribute('description', self.getDescription())
                if self._eventIdentifiers is not None:
                    target.addAttribute('eventListeners', list(self._eventIdentifiers))
                self.paintContent(target)
                error = self.getErrorMessage()
                if error is not None:
                    error.paint(target)
            else:
                target.addAttribute('invisible', True)
        else:
            # Contents have not changed, only cached presentation can be used
            target.addAttribute('cached', True)
        target.endTag(tag)
        self._repaintRequestListenersNotified = False

    def getCSSHeight(self):
        """Build CSS compatible string representation of height.

        @return CSS height
        """
        if self.getHeightUnits() == self.UNITS_PIXELS:
            return self.getHeight() + self.UNIT_SYMBOLS[self.getHeightUnits()]
        else:
            return self.getHeight() + self.UNIT_SYMBOLS[self.getHeightUnits()]

    def getCSSWidth(self):
        """Build CSS compatible string representation of width.

        @return CSS width
        """
        if self.getWidthUnits() == self.UNITS_PIXELS:
            return self.getWidth() + self.UNIT_SYMBOLS[self.getWidthUnits()]
        else:
            return self.getWidth() + self.UNIT_SYMBOLS[self.getWidthUnits()]

    def paintContent(self, target):
        """Paints any needed component-specific things to the given UIDL stream. The
        more general {@link #paint(PaintTarget)} method handles all general
        attributes common to all components, and it calls this method to paint
        any component-specific attributes to the UIDL stream.

        @param target
                   the target UIDL stream where the component should paint itself
                   to
        @throws PaintException
                    if the paint operation failed.
        """
        # Documentation copied from interface
        pass

    def requestRepaint(self):
        # The effect of the repaint request is identical to case where a
        # child requests repaint
        # Documentation copied from interface
        self.childRequestedRepaint(None)

    def childRequestedRepaint(self, alreadyNotified):
        # Invisible components (by flag in this particular component) do not
        # need repaints
        if not self._visible:
            return
        self.fireRequestRepaintEvent(alreadyNotified)

    def fireRequestRepaintEvent(self, alreadyNotified):
        """Fires the repaint request event.

        @param alreadyNotified
        """
        # Notify listeners only once
        # Documentation copied from interface
        if not self._repaintRequestListenersNotified:
            # Notify the listeners
            if (
                self._repaintRequestListeners is not None and not self._repaintRequestListeners.isEmpty()
            ):
                listeners = list(self._repaintRequestListeners)
                event = self.RepaintRequestEvent(self)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(listeners)):
                        break
                    if alreadyNotified is None:
                        alreadyNotified = LinkedList()
                    if not alreadyNotified.contains(listeners[i]):
                        listeners[i].repaintRequested(event)
                        alreadyNotified.add(listeners[i])
                        self._repaintRequestListenersNotified = True
            # Notify the parent
            parent = self.getParent()
            if parent is not None:
                parent.childRequestedRepaint(alreadyNotified)

    def addListener(self, *args):
        """None
        ---
        <p>
        Registers a new listener with the specified activation method to listen
        events generated by this component. If the activation method does not
        have any arguments the event object will not be passed to it when it's
        called.
        </p>

        <p>
        This method additionally informs the event-api to route events with the
        given eventIdentifier to the components handleEvent function call.
        </p>

        <p>
        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.
        </p>

        @param eventIdentifier
                   the identifier of the event to listen for
        @param eventType
                   the type of the listened event. Events of this type or its
                   subclasses activate the listener.
        @param target
                   the object instance who owns the activation method.
        @param method
                   the activation method.

        @since 6.2
        ---
        <p>
        Registers a new listener with the specified activation method to listen
        events generated by this component. If the activation method does not
        have any arguments the event object will not be passed to it when it's
        called.
        </p>

        <p>
        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.
        </p>

        @param eventType
                   the type of the listened event. Events of this type or its
                   subclasses activate the listener.
        @param target
                   the object instance who owns the activation method.
        @param method
                   the activation method.
        ---
        <p>
        Convenience method for registering a new listener with the specified
        activation method to listen events generated by this component. If the
        activation method does not have any arguments the event object will not
        be passed to it when it's called.
        </p>

        <p>
        This version of <code>addListener</code> gets the name of the activation
        method as a parameter. The actual method is reflected from
        <code>object</code>, and unless exactly one match is found,
        <code>java.lang.IllegalArgumentException</code> is thrown.
        </p>

        <p>
        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.
        </p>

        <p>
        Note: Using this method is discouraged because it cannot be checked
        during compilation. Use {@link #addListener(Class, Object, Method)} or
        {@link #addListener(com.vaadin.ui.Component.Listener)} instead.
        </p>

        @param eventType
                   the type of the listened event. Events of this type or its
                   subclasses activate the listener.
        @param target
                   the object instance who owns the activation method.
        @param methodName
                   the name of the activation method.
        """
        # Documentation copied from interface
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Component.Listener):
                listener, = _0
                self.addListener(Component.Event, listener, self._COMPONENT_EVENT_METHOD)
            else:
                listener, = _0
                if self._repaintRequestListeners is None:
                    self._repaintRequestListeners = LinkedList()
                if not self._repaintRequestListeners.contains(listener):
                    self._repaintRequestListeners.add(listener)
        elif _1 == 3:
            if isinstance(_0[2], Method):
                eventType, target, method = _0
                if self._eventRouter is None:
                    self._eventRouter = EventRouter()
                self._eventRouter.addListener(eventType, target, method)
            else:
                eventType, target, methodName = _0
                if self._eventRouter is None:
                    self._eventRouter = EventRouter()
                self._eventRouter.addListener(eventType, target, methodName)
        elif _1 == 4:
            eventIdentifier, eventType, target, method = _0
            if self._eventRouter is None:
                self._eventRouter = EventRouter()
            if self._eventIdentifiers is None:
                self._eventIdentifiers = set()
            needRepaint = not self._eventRouter.hasListeners(eventType)
            self._eventRouter.addListener(eventType, target, method)
            if needRepaint:
                self._eventIdentifiers.add(eventIdentifier)
                self.requestRepaint()
        else:
            raise ARGERROR(1, 4)

    def removeListener(self, *args):
        """None
        ---
        Removes all registered listeners matching the given parameters. Since
        this method receives the event type and the listener object as
        parameters, it will unregister all <code>object</code>'s methods that are
        registered to listen to events of type <code>eventType</code> generated
        by this component.

        <p>
        This method additionally informs the event-api to stop routing events
        with the given eventIdentifier to the components handleEvent function
        call.
        </p>

        <p>
        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.
        </p>

        @param eventIdentifier
                   the identifier of the event to stop listening for
        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   the target object that has registered to listen to events of
                   type <code>eventType</code> with one or more methods.

        @since 6.2
        ---
        Removes all registered listeners matching the given parameters. Since
        this method receives the event type and the listener object as
        parameters, it will unregister all <code>object</code>'s methods that are
        registered to listen to events of type <code>eventType</code> generated
        by this component.

        <p>
        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.
        </p>

        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   the target object that has registered to listen to events of
                   type <code>eventType</code> with one or more methods.
        ---
        Removes one registered listener method. The given method owned by the
        given object will no longer be called when the specified events are
        generated by this component.

        <p>
        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.
        </p>

        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   target object that has registered to listen to events of type
                   <code>eventType</code> with one or more methods.
        @param method
                   the method owned by <code>target</code> that's registered to
                   listen to events of type <code>eventType</code>.
        ---
        <p>
        Removes one registered listener method. The given method owned by the
        given object will no longer be called when the specified events are
        generated by this component.
        </p>

        <p>
        This version of <code>removeListener</code> gets the name of the
        activation method as a parameter. The actual method is reflected from
        <code>target</code>, and unless exactly one match is found,
        <code>java.lang.IllegalArgumentException</code> is thrown.
        </p>

        <p>
        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.
        </p>

        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   the target object that has registered to listen to events of
                   type <code>eventType</code> with one or more methods.
        @param methodName
                   the name of the method owned by <code>target</code> that's
                   registered to listen to events of type <code>eventType</code>.
        """
        # Component variable changes
        # Invoked when the value of a variable has changed. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Component.Listener):
                listener, = _0
                self.removeListener(Component.Event, listener, self._COMPONENT_EVENT_METHOD)
            else:
                listener, = _0
                if self._repaintRequestListeners is not None:
                    self._repaintRequestListeners.remove(listener)
                    if self._repaintRequestListeners.isEmpty():
                        self._repaintRequestListeners = None
        elif _1 == 2:
            eventType, target = _0
            if self._eventRouter is not None:
                self._eventRouter.removeListener(eventType, target)
        elif _1 == 3:
            if isinstance(_0[0], Class):
                if isinstance(_0[2], Method):
                    eventType, target, method = _0
                    if self._eventRouter is not None:
                        self._eventRouter.removeListener(eventType, target, method)
                else:
                    eventType, target, methodName = _0
                    if self._eventRouter is not None:
                        self._eventRouter.removeListener(eventType, target, methodName)
            else:
                eventIdentifier, eventType, target = _0
                if self._eventRouter is not None:
                    self._eventRouter.removeListener(eventType, target)
                    if not self._eventRouter.hasListeners(eventType):
                        self._eventIdentifiers.remove(eventIdentifier)
                        self.requestRepaint()
        else:
            raise ARGERROR(1, 3)

    def changeVariables(self, source, variables):
        # General event framework
        pass

    _COMPONENT_EVENT_METHOD = ReflectTools.findMethod(Component.Listener, 'componentEvent', Component.Event)

    def hasListeners(self, eventType):
        """Checks if the given {@link Event} type is listened for this component.

        @param eventType
                   the event type to be checked
        @return true if a listener is registered for the given event type
        """
        return self._eventRouter is not None and self._eventRouter.hasListeners(eventType)

    def getListeners(self, eventType):
        """Returns all listeners that are registered for the given event type or one
        of its subclasses.

        @param eventType
                   The type of event to return listeners for.
        @return A collection with all registered listeners. Empty if no listeners
                are found.
        """
        if eventType.isAssignableFrom(self.RepaintRequestEvent):
            # RepaintRequestListeners are not stored in eventRouter
            if self._repaintRequestListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._repaintRequestListeners)
        if self._eventRouter is None:
            return Collections.EMPTY_LIST
        return self._eventRouter.getListeners(eventType)

    def fireEvent(self, event):
        """Sends the event to all listeners.

        @param event
                   the Event to be sent to all listeners.
        """
        # Component event framework
        # Registers a new listener to listen events generated by this component.
        # Don't add a JavaDoc comment here, we use the default documentation from
        # implemented interface.

        if self._eventRouter is not None:
            self._eventRouter.fireEvent(event)

    # Removes a previously registered listener from this component. Don't add a
    # JavaDoc comment here, we use the default documentation from implemented
    # interface.

    def fireComponentEvent(self):
        """Emits the component event. It is transmitted to all registered listeners
        interested in such events.
        """
        self.fireEvent(Component.Event(self))

    def fireComponentErrorEvent(self):
        """Emits the component error event. It is transmitted to all registered
        listeners interested in such events.
        """
        self.fireEvent(Component.ErrorEvent(self.getComponentError(), self))

    def setData(self, data):
        """Sets the data object, that can be used for any application specific data.
        The component does not use or modify this data.

        @param data
                   the Application specific data.
        @since 3.1
        """
        self._applicationData = data

    def getData(self):
        """Gets the application specific data. See {@link #setData(Object)}.

        @return the Application specific data set with setData function.
        @since 3.1
        """
        # Sizeable and other size related methods
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#getHeight()

        return self._applicationData

    def getHeight(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#getHeightUnits()

        return self._height

    def getHeightUnits(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#getWidth()

        return self._heightUnit

    def getWidth(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#getWidthUnits()

        return self._width

    def getWidthUnits(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#setHeight(float)

        return self._widthUnit

    def setHeight(self, *args):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#setHeightUnits(int)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], float):
                height, = _0
                self.setHeight(height, self.getHeightUnits())
            else:
                height, = _0
                p = self.parseStringSize(height)
                self.setHeight(p[0], p[1])
        elif _1 == 2:
            height, unit = _0
            self._height = height
            self._heightUnit = unit
            self.requestRepaint()
            # ComponentSizeValidator.setHeightLocation(this);
        else:
            raise ARGERROR(1, 2)

    def setHeightUnits(self, unit):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#setHeight(float, int)

        self.setHeight(self.getHeight(), unit)

    # (non-Javadoc)
    #
    # @see com.vaadin.terminal.Sizeable#setSizeFull()

    def setSizeFull(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#setSizeUndefined()

        self.setWidth(100, self.UNITS_PERCENTAGE)
        self.setHeight(100, self.UNITS_PERCENTAGE)

    def setSizeUndefined(self):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#setWidth(float)

        self.setWidth(-1, self.UNITS_PIXELS)
        self.setHeight(-1, self.UNITS_PIXELS)

    def setWidth(self, *args):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#setWidthUnits(int)

        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], float):
                width, = _0
                self.setWidth(width, self.getWidthUnits())
            else:
                width, = _0
                p = self.parseStringSize(width)
                self.setWidth(p[0], p[1])
        elif _1 == 2:
            width, unit = _0
            self._width = width
            self._widthUnit = unit
            self.requestRepaint()
            # ComponentSizeValidator.setWidthLocation(this);
        else:
            raise ARGERROR(1, 2)

    def setWidthUnits(self, unit):
        # (non-Javadoc)
        #
        # @see com.vaadin.terminal.Sizeable#setWidth(float, int)

        self.setWidth(self.getWidth(), unit)

    # (non-Javadoc)
    #
    # @see com.vaadin.terminal.Sizeable#setWidth(java.lang.String)

    # (non-Javadoc)
    #
    # @see com.vaadin.terminal.Sizeable#setHeight(java.lang.String)



class ComponentErrorEvent(TerminalErrorEvent):
    pass

#    /*
#     * Returns array with size in index 0 unit in index 1. Null or empty string
#     * will produce {-1,UNITS_PIXELS}
#     */
#    private static float[] parseStringSize(String s) {
#        float[] values = { -1, UNITS_PIXELS };
#        if (s == null) {
#            return values;
#        }
#        s = s.trim();
#        if ("".equals(s)) {
#            return values;
#        }
#
#        Matcher matcher = sizePattern.matcher(s);
#        if (matcher.find()) {
#            values[0] = Float.parseFloat(matcher.group(1));
#            if (values[0] < 0) {
#                values[0] = -1;
#            } else {
#                String unit = matcher.group(3);
#                if (unit == null) {
#                    values[1] = UNITS_PIXELS;
#                } else if (unit.equals("px")) {
#                    values[1] = UNITS_PIXELS;
#                } else if (unit.equals("%")) {
#                    values[1] = UNITS_PERCENTAGE;
#                } else if (unit.equals("em")) {
#                    values[1] = UNITS_EM;
#                } else if (unit.equals("ex")) {
#                    values[1] = UNITS_EX;
#                } else if (unit.equals("in")) {
#                    values[1] = UNITS_INCH;
#                } else if (unit.equals("cm")) {
#                    values[1] = UNITS_CM;
#                } else if (unit.equals("mm")) {
#                    values[1] = UNITS_MM;
#                } else if (unit.equals("pt")) {
#                    values[1] = UNITS_POINTS;
#                } else if (unit.equals("pc")) {
#                    values[1] = UNITS_PICAS;
#                }
#            }
#        } else {
#            throw new IllegalArgumentException("Invalid size argument: \"" + s
#                    + "\" (should match " + sizePattern.pattern() + ")");
#        }
#        return values;
#    }
#
#    public interface ComponentErrorHandler extends Serializable {
#        /**
#         * Handle the component error
#         *
#         * @param event
#         * @return True if the error has been handled False, otherwise
#         */
#        public boolean handleComponentError(ComponentErrorEvent event);
#    }
#
#    /**
#     * Gets the error handler for the component.
#     *
#     * The error handler is dispatched whenever there is an error processing the
#     * data coming from the client.
#     *
#     * @return
#     */
#    public ComponentErrorHandler getErrorHandler() {
#        return errorHandler;
#    }
#
#    /**
#     * Sets the error handler for the component.
#     *
#     * The error handler is dispatched whenever there is an error processing the
#     * data coming from the client.
#     *
#     * If the error handler is not set, the application error handler is used to
#     * handle the exception.
#     *
#     * @param errorHandler
#     *            AbstractField specific error handler
#     */
#    public void setErrorHandler(ComponentErrorHandler errorHandler) {
#        this.errorHandler = errorHandler;
#    }
#
#    /**
#     * Handle the component error event.
#     *
#     * @param error
#     *            Error event to handle
#     * @return True if the error has been handled False, otherwise. If the error
#     *         haven't been handled by this component, it will be handled in the
#     *         application error handler.
#     */
#    public boolean handleError(ComponentErrorEvent error) {
#        if (errorHandler != null) {
#            return errorHandler.handleComponentError(error);
#        }
#        return false;
#
#    }
