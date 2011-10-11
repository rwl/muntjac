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

import re

from warnings import warn

from muntjac.event.method_event_source import IMethodEventSource
from muntjac.event.event_router import EventRouter
from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent
from muntjac.terminal.paintable import RepaintRequestEvent
from muntjac.util import fullname

from muntjac.ui.component import \
    IComponent, IListener, IFocusable, Event as ComponentEvent


class AbstractComponent(IComponent, IMethodEventSource):
    """An abstract class that defines default implementation for the
    {@link IComponent} interface. Basic UI components that are not derived
    from an external component can inherit this class to easily qualify as
    Vaadin components. Most components in Vaadin do just that.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self):
        """Constructs a new IComponent."""

        # Style names.
        self._styles = None

        # Caption text.
        self._caption = None

        # Application specific data object. The component does not use
        # or modify this.
        self._applicationData = None

        # Icon to be shown together with caption.
        self._icon = None

        # Is the component enabled (its normal usage is allowed).
        self._enabled = True

        # Is the component visible (it is rendered).
        self._visible = True

        # Is the component read-only ?
        self._readOnly = False

        # Description of the usage (XML).
        self._description = None

        # The container this component resides in.
        self._parent = None

        # The EventRouter used for the event model.
        self._eventRouter = None

        # A set of event identifiers with registered listeners.
        self._eventIdentifiers = None

        # The internal error message of the component.
        self._componentError = None

        # Immediate mode: if true, all variable changes are required
        # to be sent from the terminal immediately.
        self._immediate = False

        # Locale of this component.
        self._locale = None

        # The component should receive focus (if {@link IFocusable})
        # when attached.
        self._delayedFocus = None

        # List of repaint request listeners or null if not listened at all.
        self._repaintRequestListeners = None

        # Are all the repaint listeners notified about recent changes ?
        self._repaintRequestListenersNotified = False

        self._testingId = None

        # Sizeable fields
        self._width = self.SIZE_UNDEFINED
        self._height = self.SIZE_UNDEFINED
        self._widthUnit = self.UNITS_PIXELS
        self._heightUnit = self.UNITS_PIXELS

        self._sizePattern = \
                re.compile('^(-?\\d+(\\.\\d+)?)(%|px|em|ex|in|cm|mm|pt|pc)?$')

        self._errorHandler = None

        #ComponentSizeValidator.setCreationLocation(this);


    def getTag(self):
        """Gets the UIDL tag corresponding to the component.

        Note! In version 6.2 the method for mapping server side components
        to their client side counterparts was enhanced. This method was made
        final to intentionally "break" code where it is needed. If your code
        does not compile due overriding this method, it is very likely that
        you need to:
        <ul>
        <li>remove the implementation of getTag
        <li>add {@link ClientWidget} annotation to your component
        </ul>

        @return the component's UIDL tag as <code>String</code>
        @deprecated tags are no more required for components. Instead of tags
                    we are now using {@link ClientWidget} annotations to map
                    server side components to client side counterparts.
                    Generating identifier for component type is delegated to
                    terminal.
        @see ClientWidget
        """
        warn('tags are no more required for components', DeprecationWarning)
        return ''


    def setDebugId(self, idd):
        self._testingId = idd


    def getDebugId(self):
        return self._testingId


    def getStyle(self):
        """Gets style for component. Multiple styles are joined with spaces.

        @return the component's styleValue of property style.
        @deprecated Use getStyleName() instead; renamed for consistency and
                    to indicate that "style" should not be used to switch
                    client side implementation, only to style the component.
        """
        warn('Use getStyleName() instead', DeprecationWarning)
        return self.getStyleName()


    def setStyle(self, style):
        """Sets and replaces all previous style names of the component. This
        method will trigger a {@link RepaintRequestEvent}.

        @param style
                   the new style of the component.
        @deprecated Use setStyleName() instead; renamed for consistency and
                    to indicate that "style" should not be used to switch
                    client side implementation, only to style the component.
        """
        warn('Use setStyleName() instead', DeprecationWarning)
        self.setStyleName(style)


    def getStyleName(self):
        # Gets the component's style.
        s = ''
        if self._styles is not None:
            for i, sty in enumerate(self._styles):
                s += sty
                if i < len(self._styles) - 1:
                    s += ' '
        return s


    def setStyleName(self, style):
        # Sets the component's style.
        if style is None or '' == style:
            self._styles = None
            self.requestRepaint()
            return

        if self._styles is None:
            self._styles = list()

        self._styles.clear()
        self._styles.append(style)
        self.requestRepaint()


    def addStyleName(self, style):
        if style is None or '' == style:
            return

        if self._styles is None:
            self._styles = list()

        if style not in self._styles:
            self._styles.append(style)
            self.requestRepaint()


    def removeStyleName(self, style):
        if self._styles is not None:
            self._styles.remove(style)
            self.requestRepaint()


    def getCaption(self):
        # Get's the component's caption.
        return self._caption


    def setCaption(self, caption):
        """Sets the component's caption <code>String</code>. Caption is the
        visible name of the component. This method will trigger a
        {@link RepaintRequestEvent}.

        @param caption
                   the new caption <code>String</code> for the component.
        """
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
        // IComponent for which the locale is meaningful
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
        self._locale = locale
        self.requestRepaint()


    def getIcon(self):
        # Gets the component's icon resource.
        return self._icon


    def setIcon(self, icon):
        """Sets the component's icon. This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param icon
                   the icon to be shown with the component's caption.
        """
        self._icon = icon
        self.requestRepaint()


    def isEnabled(self):
        # Tests if the component is enabled or not.
        return (self._enabled and (self._parent is None)
            or self._parent.isEnabled() and self.isVisible())


    def setEnabled(self, enabled):
        # Enables or disables the component. Don't add a JavaDoc comment
        # here, we use the default documentation from implemented interface.
        if self._enabled != enabled:
            wasEnabled = self._enabled
            wasEnabledInContext = self.isEnabled()

            self._enabled = enabled

            isEnabled = enabled
            isEnabledInContext = self.isEnabled()

            # If the actual enabled state (as rendered, in context) has not
            # changed we do not need to repaint except if the parent is
            # invisible.
            # If the parent is invisible we must request a repaint so the
            # component is repainted with the new enabled state when the
            # parent is set visible again. This workaround is needed as
            # isEnabled checks isVisible.
            needRepaint = ((wasEnabledInContext != isEnabledInContext)
                or (wasEnabled != isEnabled
                    and (self.getParent() is None)
                    or (not self.getParent().isVisible())))

            if needRepaint:
                self.requestRepaint()


    def isImmediate(self):
        # Tests if the component is in the immediate mode.
        return self._immediate


    def setImmediate(self, immediate):
        """Sets the component's immediate mode to the specified status.
        This method will trigger a {@link RepaintRequestEvent}.

        @param immediate
                   the boolean value specifying if the component should
                   be in the immediate mode after the call.
        @see IComponent#isImmediate()
        """
        self._immediate = immediate
        self.requestRepaint()


    def isVisible(self):
        return (self._visible
                and (self.getParent() is None
                     or self.getParent().isVisible()))


    def setVisible(self, visible):
        if self._visible != visible:
            self._visible = visible
            # Instead of requesting repaint normally we
            # fire the event directly to assure that the
            # event goes through event in the component might
            # now be invisible
            self.fireRequestRepaintEvent(None)


    def getDescription(self):
        """Gets the component's description. The description can be used
        to briefly describe the state of the component to the user. The
        description string may contain certain XML tags:

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

        These tags may be nested.

        @return component's description <code>String</code>
        """
        return self._description


    def setDescription(self, description):
        """Sets the component's description. See {@link #getDescription()}
        for more information on what the description is. This method will
        trigger a {@link RepaintRequestEvent}.

        @param description
                   the new description string for the component.
        """
        self._description = description
        self.requestRepaint()


    def getParent(self):
        # Gets the component's parent component.
        return self._parent


    def setParent(self, parent):
        # Sets the parent component.

        # If the parent is not changed, don't do anything
        if parent == self._parent:
            return

        if parent is not None and self._parent is not None:
            raise ValueError, fullname(self) + ' already has a parent.'

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

        @return ErrorMessage containing the description of the error state
                of the component or null, if the component contains no errors.
                Extending classes should override this method if they support
                other error message types such as validation errors or
                buffering errors. The returned error message contains
                information about all the errors.
        """
        return self._componentError


    def getComponentError(self):
        """Gets the component's error message.

        @return the component's error message.
        """
        return self._componentError


    def setComponentError(self, componentError):
        """Sets the component's error message. The message may contain
        certain XML tags, for more information see

        @link IComponent.ErrorMessage#ErrorMessage(String, int)

        @param componentError
                   the new <code>ErrorMessage</code> of the component.
        """
        self._componentError = componentError
        self.fireComponentErrorEvent()
        self.requestRepaint()


    def isReadOnly(self):
        # Tests if the component is in read-only mode.
        return self._readOnly


    def setReadOnly(self, readOnly):
        # Sets the component's read-only mode.
        self._readOnly = readOnly
        self.requestRepaint()


    def getWindow(self):
        # Gets the parent window of the component.
        if self._parent is None:
            return None
        else:
            return self._parent.getWindow()


    def attach(self):
        # Notify the component that it's attached to a window.
        self.requestRepaint()
        if not self._visible:
            # Bypass the repaint optimization in childRequestedRepaint
            # method when attaching. When reattaching (possibly moving)
            # must repaint
            self.fireRequestRepaintEvent(None)

        if self._delayedFocus:
            self.focus()


    def detach(self):
        # Detach the component from application.
        pass


    def focus(self):
        """Sets the focus for this component if the component is
        {@link IFocusable}.
        """
        if isinstance(self, IFocusable):
            app = self.getApplication()
            if app is not None:
                self.getWindow().setFocusedComponent(self)
                self._delayedFocus = False
            else:
                self._delayedFocus = True


    def getApplication(self):
        # Gets the parent application of the component.
        if self._parent is None:
            return None
        else:
            return self._parent.getApplication()


    def requestRepaintRequests(self):
        self._repaintRequestListenersNotified = False


    def paint(self, target):
        # Paints the component into a UIDL stream.
        tag = target.getTag(self)
        if ((not target.startTag(self, tag))
                or self._repaintRequestListenersNotified):

            # Paint the contents of the component

            # Only paint content of visible components.
            if self.isVisible():
                from muntjac.terminal.gwt.server.component_size_validator \
                    import ComponentSizeValidator  # FIXME: circular import

                if (self.getHeight() >= 0
                    and (self.getHeightUnits() != self.UNITS_PERCENTAGE
                    or ComponentSizeValidator.parentCanDefineHeight(self))):

                    target.addAttribute('height', '' + self.getCSSHeight())

                if (self.getWidth() >= 0
                    and (self.getWidthUnits() != self.UNITS_PERCENTAGE
                    or ComponentSizeValidator.parentCanDefineWidth(self))):

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

                if (self.getDescription() is not None
                        and len(self.getDescription()) > 0):
                    target.addAttribute('description', self.getDescription())

                if self._eventIdentifiers is not None:
                    target.addAttribute('eventListeners',
                            list(self._eventIdentifiers))

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
            return (str(self.getWidth())
                    + self.UNIT_SYMBOLS[self.getWidthUnits()])
        else:
            return (str(self.getWidth())
                    + self.UNIT_SYMBOLS[self.getWidthUnits()])


    def paintContent(self, target):
        """Paints any needed component-specific things to the given UIDL
        stream. The more general {@link #paint(PaintTarget)} method handles
        all general attributes common to all components, and it calls this
        method to paint any component-specific attributes to the UIDL stream.

        @param target
                   the target UIDL stream where the component should paint
                   itself to
        @throws PaintException
                    if the paint operation failed.
        """
        pass


    def requestRepaint(self):
        # The effect of the repaint request is identical to case where
        # a child requests repaint
        self.childRequestedRepaint(None)


    def childRequestedRepaint(self, alreadyNotified):
        # Invisible components (by flag in this particular component)
        # do not need repaints
        if not self._visible:
            return
        self.fireRequestRepaintEvent(alreadyNotified)


    def fireRequestRepaintEvent(self, alreadyNotified):
        """Fires the repaint request event.

        @param alreadyNotified
        """
        # Notify listeners only once
        if not self._repaintRequestListenersNotified:
            # Notify the listeners
            if (self._repaintRequestListeners is not None
                    and len(self._repaintRequestListeners) > 0):

                listeners = list(self._repaintRequestListeners)
                event = RepaintRequestEvent(self)

                for listener in listeners:
                    if alreadyNotified is None:
                        alreadyNotified = list()

                    if listener not in alreadyNotified:
                        listener.repaintRequested(event)
                        alreadyNotified.append(listener)
                        self._repaintRequestListenersNotified = True

            # Notify the parent
            parent = self.getParent()
            if parent is not None:
                parent.childRequestedRepaint(alreadyNotified)


    def addListener(self, *args):
        """Registers a new listener with the specified activation method to
        listen events generated by this component. If the activation method
        does not have any arguments the event object will not be passed to
        it when it's called.

        This method additionally informs the event-api to route events with
        the given eventIdentifier to the components handleEvent function
        call.

        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.

        @param eventIdentifier
                   the identifier of the event to listen for
        @param eventType
                   the type of the listened event. Events of this type or
                   its subclasses activate the listener.
        @param target
                   the object instance who owns the activation method.
        @param method
                   the activation method.

        @since 6.2
        ---
        Registers a new listener with the specified activation method to
        listen events generated by this component. If the activation method
        does not have any arguments the event object will not be passed to
        it when it's called.

        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.

        @param eventType
                   the type of the listened event. Events of this type or
                   its subclasses activate the listener.
        @param target
                   the object instance who owns the activation method.
        @param method
                   the activation method.
        ---
        Convenience method for registering a new listener with the specified
        activation method to listen events generated by this component. If
        the activation method does not have any arguments the event object
        will not be passed to it when it's called.

        This version of <code>addListener</code> gets the name of the
        activation method as a parameter. The actual method is reflected
        from <code>object</code>, and unless exactly one match is found,
        <code>java.lang.IllegalArgumentException</code> is thrown.

        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.

        Note: Using this method is discouraged because it cannot be checked
        during compilation. Use {@link #addListener(Class, Object, Method)}
        or {@link #addListener(com.vaadin.ui.IComponent.IListener)} instead.

        @param eventType
                   the type of the listened event. Events of this type or
                   its subclasses activate the listener.
        @param target
                   the object instance who owns the activation method.
        @param methodName
                   the name of the activation method.
        """
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], IListener):
                listener = args[0]
                self.addListener(ComponentEvent, listener,
                        self._COMPONENT_EVENT_METHOD)
            else:
                listener = args[0]  # RepaintRequestListener

                if self._repaintRequestListeners is None:
                    self._repaintRequestListeners = list()

                if listener not in self._repaintRequestListeners:
                    self._repaintRequestListeners.append(listener)
        elif nargs == 3:
            if isinstance(args[2], basestring):
                eventType, target, methodName = args

                if self._eventRouter is None:
                    self._eventRouter = EventRouter()

                self._eventRouter.addListener(eventType, target, methodName)
            else:
                eventType, target, method = args

                if self._eventRouter is None:
                    self._eventRouter = EventRouter()

                self._eventRouter.addListener(eventType, target, method)
        elif nargs == 4:
            eventIdentifier, eventType, target, method = args

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
            raise ValueError, 'invalid number of arguments'


    def removeListener(self, *args):
        """Removes all registered listeners matching the given parameters.
        Since this method receives the event type and the listener object
        as parameters, it will unregister all <code>object</code>'s methods
        that are registered to listen to events of type
        <code>eventType</code> generated by this component.

        This method additionally informs the event-api to stop routing
        events with the given eventIdentifier to the components handleEvent
        function call.

        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.

        @param eventIdentifier
                   the identifier of the event to stop listening for
        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   the target object that has registered to listen to events
                   of type <code>eventType</code> with one or more methods.

        @since 6.2
        ---
        Removes all registered listeners matching the given parameters. Since
        this method receives the event type and the listener object as
        parameters, it will unregister all <code>object</code>'s methods that
        are registered to listen to events of type <code>eventType</code>
        generated by this component.

        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.

        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   the target object that has registered to listen to events
                   of type <code>eventType</code> with one or more methods.
        ---
        Removes one registered listener method. The given method owned by the
        given object will no longer be called when the specified events are
        generated by this component.

        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.

        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   target object that has registered to listen to events of
                   type <code>eventType</code> with one or more methods.
        @param method
                   the method owned by <code>target</code> that's registered
                   to listen to events of type <code>eventType</code>.
        ---
        Removes one registered listener method. The given method owned by the
        given object will no longer be called when the specified events are
        generated by this component.

        This version of <code>removeListener</code> gets the name of the
        activation method as a parameter. The actual method is reflected from
        <code>target</code>, and unless exactly one match is found,
        <code>java.lang.IllegalArgumentException</code> is thrown.

        For more information on the inheritable event mechanism see the
        {@link com.vaadin.event com.vaadin.event package documentation}.

        @param eventType
                   the exact event type the <code>object</code> listens to.
        @param target
                   the target object that has registered to listen to events
                   of type <code>eventType</code> with one or more methods.
        @param methodName
                   the name of the method owned by <code>target</code>
                   that's registered to listen to events of type
                   <code>eventType</code>.
        """
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], IListener):
                listener = [0]
                self.removeListener(ComponentEvent, listener,
                        self._COMPONENT_EVENT_METHOD)
            else:
                listener = args[0]
                if self._repaintRequestListeners is not None:
                    self._repaintRequestListeners.remove(listener)
                    if len(self._repaintRequestListeners) == 0:
                        self._repaintRequestListeners = None
        elif nargs == 2:
            eventType, target = args

            if self._eventRouter is not None:
                self._eventRouter.removeListener(eventType, target)
        elif nargs == 3:
            if isinstance(args[0], basestring):
                eventIdentifier, eventType, target = args

                if self._eventRouter is not None:
                    self._eventRouter.removeListener(eventType, target)
                    if not self._eventRouter.hasListeners(eventType):
                        self._eventIdentifiers.remove(eventIdentifier)
                        self.requestRepaint()
            else:
                if isinstance(args[2], basestring):
                    eventType, target, methodName = args

                    if self._eventRouter is not None:
                        self._eventRouter.removeListener(eventType, target,
                                methodName)
                else:
                    eventType, target, method = args

                    if self._eventRouter is not None:
                        self._eventRouter.removeListener(eventType, target,
                                method)
        else:
            raise ValueError, 'invalid number of arguments'


    def changeVariables(self, source, variables):
        # Invoked when the value of a variable has changed.
        pass


    _COMPONENT_EVENT_METHOD = getattr(IListener, 'componentEvent')


    def hasListeners(self, eventType):
        """Checks if the given {@link Event} type is listened for this
        component.

        @param eventType
                   the event type to be checked
        @return true if a listener is registered for the given event type
        """
        return (self._eventRouter is not None
                and self._eventRouter.hasListeners(eventType))


    def getListeners(self, eventType):
        """Returns all listeners that are registered for the given event
        type or one of its subclasses.

        @param eventType
                   The type of event to return listeners for.
        @return A collection with all registered listeners. Empty if no
                listeners are found.
        """
        if issubclass(eventType, RepaintRequestEvent):
            # RepaintRequestListeners are not stored in eventRouter
            if self._repaintRequestListeners is None:
                return list()
            else:
                return self._repaintRequestListeners

        if self._eventRouter is None:
            return list()

        return self._eventRouter.getListeners(eventType)


    def fireEvent(self, event):
        """Sends the event to all listeners.

        @param event
                   the Event to be sent to all listeners.
        """
        if self._eventRouter is not None:
            self._eventRouter.fireEvent(event)


    def fireComponentEvent(self):
        """Emits the component event. It is transmitted to all registered
        listeners interested in such events.
        """
        self.fireEvent( ComponentEvent(self) )


    def fireComponentErrorEvent(self):
        """Emits the component error event. It is transmitted to all
        registered listeners interested in such events.
        """
        self.fireEvent( IComponentErrorEvent(self.getComponentError(), self) )


    def setData(self, data):
        """Sets the data object, that can be used for any application
        specific data. The component does not use or modify this data.

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
        return self._applicationData


    def getHeight(self):
        return self._height


    def getHeightUnits(self):
        return self._heightUnit


    def getWidth(self):
        return self._width


    def getWidthUnits(self):
        return self._widthUnit


    def setHeight(self, *args):
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], float):
                height = args[0]
                self.setHeight(height, self.getHeightUnits())
            else:
                height = args[0]
                p = self.parseStringSize(height)
                self.setHeight(p[0], p[1])
        elif nargs == 2:
            height, unit = args
            self._height = height
            self._heightUnit = unit
            self.requestRepaint()
            #ComponentSizeValidator.setHeightLocation(this);
        else:
            raise ValueError, 'too many arguments'


    def setHeightUnits(self, unit):
        self.setHeight(self.getHeight(), unit)


    def setSizeFull(self):
        self.setWidth(100, self.UNITS_PERCENTAGE)
        self.setHeight(100, self.UNITS_PERCENTAGE)


    def setSizeUndefined(self):
        self.setWidth(-1, self.UNITS_PIXELS)
        self.setHeight(-1, self.UNITS_PIXELS)


    def setWidth(self, *args):
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], float):
                width, = args
                self.setWidth(width, self.getWidthUnits())
            else:
                width, = args
                p = self.parseStringSize(width)
                self.setWidth(p[0], p[1])
        elif nargs == 2:
            width, unit = args
            self._width = width
            self._widthUnit = unit
            self.requestRepaint()
            #ComponentSizeValidator.setWidthLocation(this);
        else:
            raise ValueError, 'too many arguments'


    def setWidthUnits(self, unit):
        self.setWidth(self.getWidth(), unit)


    def parseStringSize(self, s):
        """Returns array with size in index 0 unit in index 1. Null or empty
        string will produce {-1,UNITS_PIXELS}.
        """
        values = [-1, self.UNITS_PIXELS]
        if s == None:
            return values

        s = s.strip()
        if s == '':
            return values

        match = self._sizePattern.match(s)
        if bool(match) == True:
            values[0] = float( match.group(1) )
            if values[0] < 0:
                values[0] = -1
            else:
                unit = match.group(3)
                if unit == None:
                    values[1] = self.UNITS_PIXELS
                elif unit == "px":
                    values[1] = self.UNITS_PIXELS
                elif unit == "%":
                    values[1] = self.UNITS_PERCENTAGE
                elif unit == "em":
                    values[1] = self.UNITS_EM
                elif unit == "ex":
                    values[1] = self.UNITS_EX
                elif unit == "in":
                    values[1] = self.UNITS_INCH
                elif unit == "cm":
                    values[1] = self.UNITS_CM
                elif unit == "mm":
                    values[1] = self.UNITS_MM
                elif unit == "pt":
                    values[1] = self.UNITS_POINTS
                elif unit == "pc":
                    values[1] = self.UNITS_PICAS
        else:
            raise ValueError, "Invalid size argument: " + s

        return values


    def getErrorHandler(self):
        """Gets the error handler for the component.

        The error handler is dispatched whenever there is an error
        processing the data coming from the client.
        """
        return self.errorHandler


    def setErrorHandler(self, errorHandler):
        """Sets the error handler for the component.

        The error handler is dispatched whenever there is an error
        processing the data coming from the client.

        If the error handler is not set, the application error handler
        is used to handle the exception.

        @param errorHandler
                  AbstractField specific error handler
        """
        self.errorHandler = errorHandler


    def handleError(self, error):
        """Handle the component error event.

        @param error
                  Error event to handle
        @return True if the error has been handled False, otherwise. If
                the error haven't been handled by this component, it will
                be handled in the application error handler.
        """
        if self.errorHandler != None:
            return self.errorHandler.handleComponentError(error)

        return False


class IComponentErrorHandler(object):
    """Handle the component error

    @param event
    @return True if the error has been handled False, otherwise
    """

    def handleComponentError(self, event):
        pass


class IComponentErrorEvent(ITerminalErrorEvent):
    pass
