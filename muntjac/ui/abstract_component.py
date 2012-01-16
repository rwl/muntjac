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

"""Defines the default implementation for the IComponent interface."""

import re

from warnings import warn

from muntjac.event.method_event_source import IMethodEventSource
from muntjac.event.event_router import EventRouter
from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent
from muntjac.terminal.paintable import RepaintRequestEvent,\
    IRepaintRequestListener
from muntjac.util import fullname

from muntjac.ui.component import \
    IComponent, IListener, IFocusable, Event as ComponentEvent
from muntjac.ui import component


_COMPONENT_EVENT_METHOD = getattr(IListener, 'componentEvent')


class AbstractComponent(IComponent, IMethodEventSource):
    """An abstract class that defines default implementation for the
    L{IComponent} interface. Basic UI components that are not derived
    from an external component can inherit this class to easily qualify
    as Muntjac components. Most components in Muntjac do just that.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    SIZE_PATTERN = '^(-?\\d+(\\.\\d+)?)(%|px|em|ex|in|cm|mm|pt|pc)?$'

    def __init__(self):
        """Constructs a new IComponent."""
        super(AbstractComponent, self).__init__()

        #: Style names.
        self._styles = None

        #: Caption text.
        self._caption = None

        #: Application specific data object. The component does not use
        #  or modify this.
        self._applicationData = None

        #: Icon to be shown together with caption.
        self._icon = None

        #: Is the component enabled (its normal usage is allowed).
        self._enabled = True

        #: Is the component visible (it is rendered).
        self._visible = True

        #: Is the component read-only ?
        self._readOnly = False

        #: Description of the usage (XML).
        self._description = None

        #: The container this component resides in.
        self._parent = None

        #: The EventRouter used for the event model.
        self._eventRouter = None

        #: A set of event identifiers with registered listeners.
        self._eventIdentifiers = None

        #: The internal error message of the component.
        self._componentError = None

        #: Immediate mode: if true, all variable changes are required
        #  to be sent from the terminal immediately.
        self._immediate = False

        #: Locale of this component.
        self._locale = None

        #: The component should receive focus (if L{IFocusable})
        #  when attached.
        self._delayedFocus = None

        #: List of repaint request listeners or null if not listened at all.
        self._repaintRequestListeners = list()

        self._repaintRequestCallbacks = dict()

        #: Are all the repaint listeners notified about recent changes ?
        self._repaintRequestListenersNotified = False

        self._testingId = None

        # Sizeable fields
        self._width = self.SIZE_UNDEFINED
        self._height = self.SIZE_UNDEFINED
        self._widthUnit = self.UNITS_PIXELS
        self._heightUnit = self.UNITS_PIXELS

        self._sizePattern = re.compile(self.SIZE_PATTERN)

        self.errorHandler = None

        #ComponentSizeValidator.setCreationLocation(self)


    def __getstate__(self):
        result = self.__dict__.copy()
        del result['_sizePattern']
        return result


    def __setstate__(self, d):
        self.__dict__ = d
        self._sizePattern = re.compile(self.SIZE_PATTERN)


    def setDebugId(self, idd):
        self._testingId = idd


    def getDebugId(self):
        return self._testingId


    def getStyle(self):
        """Gets style for component. Multiple styles are joined with spaces.

        @return: the component's styleValue of property style.
        @deprecated: Use getStyleName() instead; renamed for consistency and
                     to indicate that "style" should not be used to switch
                     client side implementation, only to style the component.
        """
        warn('Use getStyleName() instead', DeprecationWarning)
        return self.getStyleName()


    def setStyle(self, style):
        """Sets and replaces all previous style names of the component. This
        method will trigger a L{RepaintRequestEvent}.

        @param style:
                   the new style of the component.
        @deprecated: Use setStyleName() instead; renamed for consistency and
                     to indicate that "style" should not be used to switch
                     client side implementation, only to style the component.
        """
        warn('Use setStyleName() instead', DeprecationWarning)
        self.setStyleName(style)


    def getStyleName(self):
        # Gets the component's style.
        s = ''
        if self._styles is not None:
            s = ' '.join(self._styles)
        return s


    def setStyleName(self, style):
        # Sets the component's style.
        if style is None or style == '':
            self._styles = None
            self.requestRepaint()
            return

        if self._styles is None:
            self._styles = list()

        del self._styles[:]

        styleParts = style.split()
        for part in styleParts:
            if len(part) > 0:
                self._styles.append(part)

        self.requestRepaint()


    def addStyleName(self, style):
        if style is None or style == '':
            return

        if self._styles is None:
            self._styles = list()

        for s in style.split():
            if s not in self._styles:
                self._styles.append(s)
                self.requestRepaint()


    def removeStyleName(self, style):
        if self._styles is not None:
            styleParts = style.split()
            for part in styleParts:
                if len(part) > 0 and part in self._styles:
                    self._styles.remove(part)
            self.requestRepaint()


    def getCaption(self):
        # Get's the component's caption.
        return self._caption


    def setCaption(self, caption):
        """Sets the component's caption string. Caption is the
        visible name of the component. This method will trigger a
        L{RepaintRequestEvent}.

        @param caption:
                   the new caption string for the component.
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
        """Sets the locale of this component::

          # IComponent for which the locale is meaningful
          date = InlineDateField(&quot;Datum&quot;)

          # German language specified with ISO 639-1 language
          # code and ISO 3166-1 alpha-2 country code.
          date.setLocale(Locale(&quot;de&quot;, &quot;DE&quot;))

          date.setResolution(DateField.RESOLUTION_DAY)
          layout.addComponent(date)

        @param locale:
                   the locale to become this component's locale.
        """
        self._locale = locale
        self.requestRepaint()


    def getIcon(self):
        # Gets the component's icon resource.
        return self._icon


    def setIcon(self, icon):
        """Sets the component's icon. This method will trigger a
        L{RepaintRequestEvent<IPaintable.RepaintRequestEvent>}.

        @param icon:
                   the icon to be shown with the component's caption.
        """
        self._icon = icon
        self.requestRepaint()


    def isEnabled(self):
        # Tests if the component is enabled or not.
        return (self._enabled and ((self._parent is None)
            or (self._parent.isEnabled())) and self.isVisible())


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
        This method will trigger a L{RepaintRequestEvent}.

        @param immediate:
                   the boolean value specifying if the component should
                   be in the immediate mode after the call.
        @see: L{IComponent.isImmediate}
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
        """Gets the component's description, used in tooltips and can be
        displayed directly in certain other components such as forms. The
        description can be used to briefly describe the state of the
        component to the user. The description string may contain certain
        XML tags::

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

        These tags may be nested.

        @return: component's description string
        """
        return self._description


    def setDescription(self, description):
        """Sets the component's description. See L{getDescription}
        for more information on what the description is. This method will
        trigger a L{RepaintRequestEvent}.

        The description is displayed as HTML/XHTML in tooltips or directly in
        certain components so care should be taken to avoid creating the
        possibility for HTML injection and possibly XSS vulnerabilities.

        @param description:
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

        @return: ErrorMessage containing the description of the error state
                of the component or null, if the component contains no errors.
                Extending classes should override this method if they support
                other error message types such as validation errors or
                buffering errors. The returned error message contains
                information about all the errors.
        """
        return self._componentError


    def getComponentError(self):
        """Gets the component's error message.

        @return: the component's error message.
        """
        return self._componentError


    def setComponentError(self, componentError):
        """Sets the component's error message. The message may contain
        certain XML tags.

        @param componentError:
                   the new C{ErrorMessage} of the component.
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
        L{IFocusable}.
        """
        if isinstance(self, IFocusable):
            app = self.getApplication()
            if app is not None:
                self.getWindow().setFocusedComponent(self)
                self._delayedFocus = False
            else:
                self._delayedFocus = True


    def getApplication(self):
        """Gets the application object to which the component is attached.

        The method will return C{None} if the component is not currently
        attached to an application. This is often a problem in constructors
        of regular components and in the initializers of custom composite
        components. A standard workaround is to move the problematic
        initialization to L{attach}, as described in the documentation
        of the method.

        B{This method is not meant to be overridden.}

        @return: the parent application of the component or C{None}.
        @see: L{attach}
        """
        if self._parent is None:
            return None
        else:
            return self._parent.getApplication()


    def requestRepaintRequests(self):
        self._repaintRequestListenersNotified = False


    def paint(self, target):
        """Paints the Paintable into a UIDL stream. This method creates the
        UIDL sequence describing it and outputs it to the given UIDL stream.

        It is called when the contents of the component should be painted in
        response to the component first being shown or having been altered so
        that its visual representation is changed.

        B{Do not override this to paint your component.} Override
        L{paintContent} instead.

        @param target:
                  the target UIDL stream where the component should paint
                  itself to.
        @raise PaintException:
                  if the paint operation failed.
        """
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

        @return: CSS height
        """
        if self.getHeightUnits() == self.UNITS_PIXELS:
            return (str( int(self.getHeight()) )
                    + self.UNIT_SYMBOLS[self.getHeightUnits()])
        else:
            return (str(self.getHeight())
                    + self.UNIT_SYMBOLS[self.getHeightUnits()])


    def getCSSWidth(self):
        """Build CSS compatible string representation of width.

        @return: CSS width
        """
        if self.getWidthUnits() == self.UNITS_PIXELS:
            return (str( int(self.getWidth()) )
                    + self.UNIT_SYMBOLS[self.getWidthUnits()])
        else:
            return (str(self.getWidth())
                    + self.UNIT_SYMBOLS[self.getWidthUnits()])


    def paintContent(self, target):
        """Paints any needed component-specific things to the given UIDL
        stream. The more general L{paint} method handles
        all general attributes common to all components, and it calls this
        method to paint any component-specific attributes to the UIDL stream.

        @param target:
                   the target UIDL stream where the component should paint
                   itself to
        @raise PaintException:
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
        """
        # Notify listeners only once
        if not self._repaintRequestListenersNotified:
            # Notify the listeners
            event = RepaintRequestEvent(self)

            for listener in self._repaintRequestListeners:
                if alreadyNotified is None:
                    alreadyNotified = list()

                if listener not in alreadyNotified:
                    listener.repaintRequested(event)
                    alreadyNotified.append(listener)
                    self._repaintRequestListenersNotified = True

            for callback, args in self._repaintRequestCallbacks.iteritems():
                if alreadyNotified is None:
                    alreadyNotified = list()

                if callback not in alreadyNotified:
                    callback(event, *args)
                    alreadyNotified.append(callback)
                    self._repaintRequestListenersNotified = True

            # Notify the parent
            parent = self.getParent()
            if parent is not None:
                parent.childRequestedRepaint(alreadyNotified)


    def addListener(self, listener, iface=None):
        if (isinstance(listener, IListener) and
                (iface is None or issubclass(iface, IListener))):
            self.registerListener(ComponentEvent, listener,
                    _COMPONENT_EVENT_METHOD)

        if (isinstance(listener, IRepaintRequestListener) and
                (iface is None or issubclass(iface, IRepaintRequestListener))):
            if listener not in self._repaintRequestListeners:
                self._repaintRequestListeners.append(listener)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ComponentEvent):
            self.registerCallback(ComponentEvent, callback, None, *args)

        elif issubclass(eventType, RepaintRequestEvent):
            self._repaintRequestCallbacks[callback] = args

        else:
            super(AbstractComponent, self).addCallback(callback,
                    eventType, *args)


    def registerListener(self, *args):
        """Registers a new listener with the specified activation method to
        listen events generated by this component. If the activation method
        does not have any arguments the event object will not be passed to
        it when it's called.

        This method additionally informs the event-api to route events with
        the given eventIdentifier to the components handleEvent function
        call.

        For more information on the inheritable event mechanism see the
        L{muntjac.event package documentation<muntjac.event>}.

        @param args: tuple of the form
            - (eventIdentifier, eventType, target, method)
              1. the identifier of the event to listen for
              2. the type of the listened event. Events of this type or
                 its subclasses activate the listener.
              3. the object instance who owns the activation method.
              4. the activation method.
            - (eventType, target, method)
              1. the type of the listened event. Events of this type or
                 its subclasses activate the listener.
              2. the object instance who owns the activation method.
              3. the activation method or the name of the activation method.
        """
        nargs = len(args)
        if nargs == 3:
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


    def registerCallback(self, eventType, callback, eventId, *args):

        if hasattr(callback, 'im_self'):
            target = callback.im_self
        elif hasattr(callback, 'func_name'):
            target = None
        else:
            raise ValueError('invalid callback: %s' % callback)


        if len(args) > 0:
            arguments = (None,) + args  # assume event always passed first
            eventArgIdx = 0
        else:
            arguments = None
            eventArgIdx = None


        if self._eventRouter is None:
            self._eventRouter = EventRouter()

        if self._eventIdentifiers is None:
            self._eventIdentifiers = set()

        if eventId is not None:
            needRepaint = not self._eventRouter.hasListeners(eventType)

        self._eventRouter.addListener(eventType, target, callback,
                arguments, eventArgIdx)

        if (eventId is not None) and needRepaint:
            self._eventIdentifiers.add(eventId)
            self.requestRepaint()


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, IListener) and
                (iface is None or issubclass(iface, IListener))):
            self.withdrawListener(ComponentEvent, listener,
                    _COMPONENT_EVENT_METHOD)

        if (isinstance(listener, IRepaintRequestListener) and
                (iface is None or issubclass(iface, IRepaintRequestListener))):
            if listener in self._repaintRequestListeners:
                self._repaintRequestListeners.remove(listener)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if eventType == ComponentEvent:
            self.withdrawCallback(ComponentEvent, callback)

        elif eventType == RepaintRequestEvent:
            if callback in self._repaintRequestCallbacks:
                del self._repaintRequestCallbacks[callback]
        else:
            super(AbstractComponent, self).removeCallback(callback, eventType)


    def withdrawListener(self, *args):
        """Removes all registered listeners matching the given parameters.
        Since this method receives the event type and the listener object
        as parameters, it will unregister all C{object}'s methods that are
        registered to listen to events of type C{eventType} generated by
        this component.

        This method additionally informs the event-api to stop routing
        events with the given eventIdentifier to the components handleEvent
        function call.

        For more information on the inheritable event mechanism see the
        L{muntjac.event package documentation<muntjac.event>}.

        @param args: tuple of the form
            - (eventIdentifier, eventType, target)
              1. the identifier of the event to stop listening for
              2. the exact event type the C{object} listens to.
              3. the target object that has registered to listen to events
                 of type C{eventType} with one or more methods.
            - (eventType, target)
              1. the exact event type the C{object} listens to.
              2. the target object that has registered to listen to events
                 of type C{eventType} with one or more methods.
            - (eventType, target, method)
              1. the exact event type the C{object} listens to.
              2. the target object that has registered to listen to events
                 of type C{eventType} with one or more methods.
              3. the method or the name of the method  owned by C{target}
                 that's registered to listen to events of type C{eventType}.
        """
        nargs = len(args)
        if nargs == 2:
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


    def withdrawCallback(self, eventType, callback, eventId=None):
        if self._eventRouter is not None:

            if hasattr(callback, 'im_self'):  # method
                target = callback.im_self
            elif hasattr(callback, 'func_name'):  # function
                target = None
            else:
                raise ValueError('invalid callback: %s' % callback)

            self._eventRouter.removeListener(eventType, target, callback)

            if (eventId is not None and
                    not self._eventRouter.hasListeners(eventType)):
                self._eventIdentifiers.remove(eventId)
                self.requestRepaint()


    def changeVariables(self, source, variables):
        # Invoked when the value of a variable has changed.
        pass


    def hasListeners(self, eventType):
        """Checks if the given L{Event} type is listened for this
        component.

        @param eventType:
                   the event type to be checked
        @return: true if a listener is registered for the given event type
        """
        return (self._eventRouter is not None
                and self._eventRouter.hasListeners(eventType))


    def getListeners(self, eventType):
        """Returns all listeners that are registered for the given event
        type or one of its subclasses.

        @param eventType:
                   The type of event to return listeners for.
        @return: A collection with all registered listeners. Empty if no
                 listeners are found.
        """
        if issubclass(eventType, RepaintRequestEvent):
            # RepaintRequestListeners are not stored in eventRouter
            return list(self._repaintRequestListeners)

        if self._eventRouter is None:
            return list()

        return self._eventRouter.getListeners(eventType)


    def fireEvent(self, event):
        """Sends the event to all listeners.

        @param event:
                   the Event to be sent to all listeners.
        """
        if self._eventRouter is not None:
            self._eventRouter.fireEvent(event)


    def fireComponentEvent(self):
        """Emits the component event. It is transmitted to all registered
        listeners interested in such events.
        """
        event = ComponentEvent(self)
        self.fireEvent(event)


    def fireComponentErrorEvent(self):
        """Emits the component error event. It is transmitted to all
        registered listeners interested in such events.
        """
        event = component.ErrorEvent(self.getComponentError(), self)
        self.fireEvent(event)


    def setData(self, data):
        """Sets the data object, that can be used for any application
        specific data. The component does not use or modify this data.

        @param data:
                   the Application specific data.
        """
        self._applicationData = data


    def getData(self):
        """Gets the application specific data. See L{setData}.

        @return: the Application specific data set with setData function.
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


    def setHeight(self, height, unit=None):
        if unit is None:
            if isinstance(height, float):
                self.setHeight(height, self.getHeightUnits())
            else:
                p = self.parseStringSize(height)
                self.setHeight(p[0], p[1])
        else:
            self._height = height
            self._heightUnit = unit
            self.requestRepaint()
            #ComponentSizeValidator.setHeightLocation(this);


    def setHeightUnits(self, unit):
        self.setHeight(self.getHeight(), unit)


    def setSizeFull(self):
        self.setWidth(100, self.UNITS_PERCENTAGE)
        self.setHeight(100, self.UNITS_PERCENTAGE)


    def setSizeUndefined(self):
        self.setWidth(-1, self.UNITS_PIXELS)
        self.setHeight(-1, self.UNITS_PIXELS)


    def setWidth(self, width, unit=None):
        if unit is None:
            if isinstance(width, float):
                self.setWidth(width, self.getWidthUnits())
            else:
                p = self.parseStringSize(width)
                self.setWidth(p[0], p[1])
        else:
            self._width = width
            self._widthUnit = unit
            self.requestRepaint()
            #ComponentSizeValidator.setWidthLocation(this);


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

        @param errorHandler:
                  AbstractField specific error handler
        """
        self.errorHandler = errorHandler


    def handleError(self, error):
        """Handle the component error event.

        @param error:
                  Error event to handle
        @return: True if the error has been handled False, otherwise. If
                the error haven't been handled by this component, it will
                be handled in the application error handler.
        """
        if self.errorHandler != None:
            return self.errorHandler.handleComponentError(error)

        return False


class IComponentErrorHandler(object):
    """Handle the component error
    """

    def handleComponentError(self, event):
        """@return: True if the error has been handled False, otherwise
        """
        pass


class IComponentErrorEvent(ITerminalErrorEvent):
    pass
