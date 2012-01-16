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

"""Defines the top-level interface that is and must be implemented by
all Muntjac components."""

from muntjac.terminal.variable_owner import IVariableOwner
from muntjac.terminal.sizeable import ISizeable
from muntjac.terminal.paintable import IPaintable
from muntjac.util import EventObject, IEventListener


class IComponent(IPaintable, IVariableOwner, ISizeable):
    """C{IComponent} is the top-level interface that is and must be
    implemented by all Muntjac components. C{IComponent} is paired with
    L{AbstractComponent}, which provides a default implementation for
    all the methods defined in this interface.

    Components are laid out in the user interface hierarchically. The layout
    is managed by layout components, or more generally by components that
    implement the L{ComponentContainer} interface. Such a container is
    the I{parent} of the contained components.

    The L{getParent} method allows retrieving the parent component
    of a component. While there is a L{setParent}, you rarely need
    it as you normally add components with the
    L{addComponent()<ComponentContainer.addComponent>} method
    of the layout or other C{ComponentContainer}, which automatically
    sets the parent.

    A component becomes I{attached} to an application (and the
    L{attach} is called) when it or one of its parents is attached to
    the main window of the application through its containment hierarchy.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def getStyleName(self):
        """Gets all user-defined CSS style names of a component. If the
        component has multiple style names defined, the return string is a
        space-separated list of style names. Built-in style names defined in
        Muntjac or GWT are not returned.

        The style names are returned only in the basic form in which they
        were added; each user-defined style name shows as two CSS style class
        names in the rendered HTML: one as it was given and one prefixed with
        the component-specific style name. Only the former is returned.

        @return: the style name or a space-separated list of user-defined
                 style names of the component
        @see: L{setStyleName}
        @see: L{addStyleName}
        @see: L{removeStyleName}
        """
        raise NotImplementedError


    def setStyleName(self, style):
        """Sets one or more user-defined style names of the component,
        replacing any previous user-defined styles. Multiple styles can be
        specified as a space-separated list of style names. The style names
        must be valid CSS class names and should not conflict with any
        built-in style names in Muntjac or GWT::

          label = new Label("This text has a lot of style")
          label.setStyleName("myonestyle myotherstyle")

        Each style name will occur in two versions: one as specified and one
        that is prefixed with the style name of the component. For example,
        if you have a C{Button} component and give it "C{mystyle}"
        style, the component will have both "C{mystyle}" and
        "C{v-button-mystyle}" styles. You could then style the component
        either with::

          .myonestyle {background: blue;}

        or::

          .v-button-myonestyle {background: blue;}

        It is normally a good practice to use L{addStyleName} rather than this
        setter, as different software abstraction layers can then add their own
        styles without accidentally removing those defined in other layers.

        This method will trigger a L{RepaintRequestEvent}.

        @param style:
                   the new style or styles of the component as a
                   space-separated list
        @see: L{getStyleName}
        @see: L{addStyleName}
        @see: L{removeStyleName}
        """
        raise NotImplementedError


    def addStyleName(self, style):
        """Adds a style name to component. The style name will be rendered as
        a HTML class name, which can be used in a CSS definition::

          label = new Label("This text has style")
          label.addStyleName("mystyle")

        Each style name will occur in two versions: one as specified and one
        that is prefixed wil the style name of the component. For example, if
        you have a C{Button} component and give it "C{mystyle}"
        style, the component will have both "C{mystyle}" and
        "C{v-button-mystyle}" styles. You could then style the component
        either with::

          .mystyle {font-style: italic;}

        or::

          .v-button-mystyle {font-style: italic;}

        This method will trigger a L{RepaintRequestEvent}.

        @param style:
                   the new style to be added to the component
        @see: L{getStyleName}
        @see: L{setStyleName}
        @see: L{removeStyleName}
        """
        raise NotImplementedError


    def removeStyleName(self, style):
        """Removes one or more style names from component. Multiple styles
        can be specified as a space-separated list of style names.

        The parameter must be a valid CSS style name. Only user-defined style
        names added with L{addStyleName} or L{setStyleName} can be removed;
        built-in style names defined in Muntjac or GWT can not be removed.

        This method will trigger a L{RepaintRequestEvent}.

        @param style:
                   the style name or style names to be removed
        @see: L{getStyleName}
        @see: L{setStyleName}
        @see: L{addStyleName}
        """
        raise NotImplementedError


    def isEnabled(self):
        """Tests whether the component is enabled or not. A user can not
        interact with disabled components. Disabled components are rendered
        in a style that indicates the status, usually in gray color. Children
        of a disabled component are also disabled. Components are enabled by
        default.

        As a security feature, all variable change events for disabled
        components are blocked on the server-side.

        @return: C{True} if the component and its parent are enabled,
                 C{False} otherwise.
        @see: L{IVariableOwner.isEnabled}
        """
        raise NotImplementedError


    def setEnabled(self, enabled):
        """Enables or disables the component. The user can not interact
        disabled components, which are shown with a style that indicates the
        status, usually shaded in light gray color. Components are enabled
        by default. Children of a disabled component are automatically
        disabled; if a child component is explicitly set as disabled, changes
        in the disabled status of its parents do not change its status::

          enabled = new Button("Enabled")
          enabled.setEnabled(True)  # the default
          layout.addComponent(enabled)

          disabled = Button("Disabled")
          disabled.setEnabled(False)
          layout.addComponent(disabled)

        This method will trigger a L{RepaintRequestEvent} for the
        component and, if it is a L{ComponentContainer}, for all its
        children recursively.

        @param enabled:
                   a boolean value specifying if the component should be
                   enabled or not
        """
        raise NotImplementedError


    def isVisible(self):
        """Tests the I{visibility} property of the component.

        Visible components are drawn in the user interface, while invisible
        ones are not. The effect is not merely a cosmetic CSS change, but the
        entire HTML element will be empty. Making a component invisible
        through this property can alter the positioning of other components.

        A component is visible only if all its parents are also visible.
        Notice that if a child component is explicitly set as invisible,
        changes in the visibility status of its parents do not change its
        status.

        This method does not check whether the component is attached (see
        L{attach}). The component and all its parents may be
        considered "visible", but not necessarily attached to application.
        To test if component will actually be drawn, check both its visibility
        and that L{getApplication} does not return C{None}.

        @return: C{True} if the component is visible in the user
                interface, C{False} if not
        @see: L{setVisible}
        @see: L{attach}
        """
        raise NotImplementedError


    def setVisible(self, visible):
        """Sets the visibility of the component.

        Visible components are drawn in the user interface, while invisible
        ones are not. The effect is not merely a cosmetic CSS change, but the
        entire HTML element will be empty::

          readonly = TextField("Read-Only")
          readonly.setValue("You can't see this!")
          readonly.setVisible(False)
          layout.addComponent(readonly)

        A component is visible only if all of its parents are also visible.
        If a component is explicitly set to be invisible, changes in the
        visibility of its parents will not change the visibility of the
        component.

        @param visible:
                   the boolean value specifying if the component should be
                   visible after the call or not.
        @see: L{isVisible}
        """
        raise NotImplementedError


    def getParent(self):
        """Gets the parent component of the component.

        Components can be nested but a component can have only one parent. A
        component that contains other components, that is, can be a parent,
        should usually inherit the L{ComponentContainer} interface.

        @return: the parent component
        @see: L{setParent}
        """
        raise NotImplementedError


    def setParent(self, parent):
        """Sets the parent component of the component.

        This method automatically calls L{attach} if the parent
        becomes attached to the application, regardless of whether it was
        attached previously. Conversely, if the parent is C{None} and
        the component is attached to the application, L{detach} is
        called for the component.

        This method is rarely called directly. The
        L{ComponentContainer.addComponent} method is normally used for adding
        components to a container and it will call this method implicitly.

        It is not possible to change the parent without first setting the
        parent to C{None}.

        @param parent:
                   the parent component
        @raise ValueError:
                    if a parent is given even though the component already has
                    a parent
        """
        raise NotImplementedError


    def isReadOnly(self):
        """Tests whether the component is in the read-only mode. The user can
        not change the value of a read-only component. As only L{IField}
        components normally have a value that can be input or changed by the
        user, this is mostly relevant only to field components, though not
        restricted to them.

        Notice that the read-only mode only affects whether the user can
        change the I{value} of the component; it is possible to, for
        example, scroll a read-only table.

        The read-only status affects only the user; the value can still be
        changed programmatically, for example, with L{IProperty.setValue}.

        The method will return C{True} if the component or any of its
        parents is in the read-only mode.

        @return: C{True} if the component or any of its parents is in
                 read-only mode, C{False} if not.
        @see: L{setReadOnly}
        """
        raise NotImplementedError


    def setReadOnly(self, readOnly):
        """Sets the read-only mode of the component to the specified mode.
        The user can not change the value of a read-only component.

        As only L{IField} components normally have a value that can be
        input or changed by the user, this is mostly relevant only to field
        components, though not restricted to them.

        Notice that the read-only mode only affects whether the user can
        change the I{value} of the component; it is possible to, for
        example, scroll a read-only table.

        The read-only status affects only the user; the value can still be
        changed programmatically, for example, with L{IProperty.setValue}.

        This method will trigger a L{RepaintRequestEvent}.

        @param readOnly:
                   a boolean value specifying whether the component is put
                   read-only mode or not
        """
        raise NotImplementedError


    def getCaption(self):
        """Gets the caption of the component.

        See L{setCaption} for a detailed description of the caption.

        @return: the caption of the component or C{null} if the caption
                 is not set.
        @see: L{setCaption}
        """
        raise NotImplementedError


    def setCaption(self, caption):
        """Sets the caption of the component.

        A I{caption} is an explanatory textual label accompanying a user
        interface component, usually shown above, left of, or inside the
        component. I{Icon} (see L{setIcon} is
        closely related to caption and is usually displayed horizontally before
        or after it, depending on the component and the containing layout.

        The caption can usually also be given as the first parameter to a
        constructor, though some components do not support it::

          area = new RichTextArea()
          area.setCaption("You can edit stuff here")
          area.setValue("<h1>Helpful Heading</h1>"
                + "<p>All this is for you to edit.</p>")

        The contents of a caption are automatically quoted, so no raw XHTML can
        be rendered in a caption. The validity of the used character encoding,
        usually UTF-8, is not checked.

        The caption of a component is, by default, managed and displayed by the
        layout component or component container in which the component is
        placed. For example, the L{VerticalLayout} component shows the captions
        left-aligned above the contained components, while the L{FormLayout}
        component shows the captions on the left side of the vertically laid
        components, with the captions and their associated components
        left-aligned in their own columns. The L{CustomComponent} does not
        manage the caption of its composition root, so if the root component
        has a caption, it will not be rendered. Some components, such as
        L{Button} and L{Panel}, manage the caption themselves and display it
        inside the component.

        This method will trigger a L{RepaintRequestEvent}. A reimplementation
        should call the superclass implementation.

        @param caption:
                   the new caption for the component. If the caption is
                   C{None}, no caption is shown and it does not normally
                   take any space
        """
        raise NotImplementedError


    def getIcon(self):
        """Gets the icon resource of the component.

        See L{setIcon} for a detailed description of the icon.

        @return: the icon resource of the component or C{None} if the
                 component has no icon
        @see: L{setIcon}
        """
        raise NotImplementedError


    def setIcon(self, icon):
        """Sets the icon of the component.

        An icon is an explanatory graphical label accompanying a user interface
        component, usually shown above, left of, or inside the component. Icon
        is closely related to caption (see L{setCaption})
        and is usually displayed horizontally before or after it, depending on
        the component and the containing layout.

        The image is loaded by the browser from a resource, typically a
        L{ThemeResource}::

          # IComponent with an icon from a custom theme
          name = TextField("Name")
          name.setIcon(ThemeResource("icons/user.png"))
          layout.addComponent(name)

          # IComponent with an icon from another theme ('runo')
          ok = Button("OK")
          ok.setIcon(ThemeResource("../runo/icons/16/ok.png"))
          layout.addComponent(ok)

        The icon of a component is, by default, managed and displayed by the
        layout component or component container in which the component is
        placed. For example, the L{VerticalLayout} component shows the icons
        left-aligned above the contained components, while the L{FormLayout}
        component shows the icons on the left side of the vertically laid
        components, with the icons and their associated components left-aligned
        in their own columns. The L{CustomComponent} does not manage the
        icon of its composition root, so if the root component has an icon, it
        will not be rendered.

        An icon will be rendered inside an HTML element that has the
        C{v-icon} CSS style class. The containing layout may enclose an icon
        and a caption inside elements related to the caption, such as
        C{v-caption} .

        This method will trigger a L{RepaintRequestEvent}.

        @param icon:
                   the icon of the component. If null, no icon is shown and it
                   does not normally take any space.
        @see: L{getIcon}
        @see: L{setCaption}
        """
        raise NotImplementedError


    def getWindow(self):
        """Gets the parent window of the component.

        If the component is not attached to a window through a component
        containment hierarchy, C{None} is returned.

        The window can be either an application-level window or a sub-window.
        If the component is itself a window, it returns a reference to itself,
        not to its containing window (of a sub-window).

        @return: the parent window of the component or C{None} if it is
                not attached to a window or is itself a window
        """
        raise NotImplementedError


    def getApplication(self):
        """Gets the application object to which the component is attached.

        The method will return C{None} if the component is not currently
        attached to an application. This is often a problem in constructors of
        regular components and in the initializers of custom composite
        components. A standard workaround is to move the problematic
        initialization to L{attach}, as described in the documentation of
        the method.

        @return: the parent application of the component or C{None}.
        @see: L{attach}
        """
        raise NotImplementedError


    def attach(self):
        """Notifies the component that it is connected to an application.

        The caller of this method is L{setParent} if the parent
        is itself already attached to the application. If not, the parent will
        call the L{attach} for all its children when it is attached to
        the application. This method is always called before the component is
        painted for the first time.

        Reimplementing the C{attach()} method is useful for tasks that need
        to get a reference to the parent, window, or application object with
        the L{getParent}, L{getWindow}, and L{getApplication} methods. A
        component does not yet know these objects in the constructor,
        so in such case, the methods will return C{None}. For example, the
        following is invalid::

          class AttachExample(CustomComponent):
              def __init__(self):
                  # ERROR: We can't access the application object yet.
                  r = ClassResource("smiley.jpg", getApplication())
                  image = Embedded("Image:", r)
                  setCompositionRoot(image)

        Adding a component to an application triggers calling the
        L{attach} method for the component. Correspondingly, removing a
        component from a container triggers calling the L{detach} method.
        If the parent of an added component is already connected to the
        application, the C{attach()} is called immediately from
        L{setParent}::

          class AttachExample(CustomComponent):
              def __init__(self):
                  pass

              def attach(self):
                  super(AttachExample, self).attach()  # must call

                  # Now we know who ultimately owns us.
                  r = ClassResource("smiley.jpg", self.getApplication())
                  image = Embedded("Image", r)
                  self.setCompositionRoot(image)

        The attachment logic is implemented in L{AbstractComponent}.

        @see: L{getApplication}
        """
        raise NotImplementedError


    def detach(self):
        """Notifies the component that it is detached from the application.

        The L{getApplication} and L{getWindow} methods might
        return C{None} after this method is called.

        The caller of this method is L{setParent} if the parent is in the
        application. When the parent is detached from the application
        it is its response to call L{detach} for all the children and to
        detach itself from the terminal.
        """
        raise NotImplementedError


    def getLocale(self):
        """Gets the locale of the component.

        If a component does not have a locale set, the locale of its parent is
        returned, and so on. Eventually, if no parent has locale set, the
        locale of the application is returned. If the application does not have
        a locale set, it is determined by C{getDefaultLocale()}.

        As the component must be attached before its locale can be acquired,
        using this method in the internationalization of component captions,
        etc. is generally not feasible. For such use case, we recommend using
        an otherwise acquired reference to the application locale.

        @return: Locale of this component or C{null} if the component and
                 none of its parents has a locale set and the component is not
                 yet attached to an application.
        """
        raise NotImplementedError


    def childRequestedRepaint(self, alreadyNotified):
        """The child components of the component must call this method when
        they need repainting. The call must be made even in the case in which
        the children sent the repaint request themselves.

        A repaint request is ignored if the component is invisible.

        This method is called automatically by L{AbstractComponent}, which
        also provides a default implementation of it. As this is a somewhat
        internal feature, it is rarely necessary to reimplement this or call it
        explicitly.

        @param alreadyNotified:
                   the collection of repaint request listeners that have been
                   already notified by the child. This component should not
                   re-notify the listed listeners again. The container given as
                   parameter must be modifiable as the component might modify
                   it and pass it forward. A C{None} parameter is interpreted
                   as an empty collection.
        """
        raise NotImplementedError


    def addListener(self, listener, iface=None):
        """Registers a new (generic) component event listener for the
        component::

          class Listening(CustomComponent, IListener):

              # Stored for determining the source of an event
              ok = None

              status = None  # For displaying info about the event

              def __init__(self):
                  layout = VerticalLayout()

                  # Some miscellaneous component
                  name = TextField("Say it all here")
                  name.addListener(self)
                  name.setImmediate(true)
                  layout.addComponent(name)

                  # Handle button clicks as generic events instead
                  # of Button.ClickEvent events
                  ok = new Button("OK")
                  ok.addListener(self)
                  layout.addComponent(ok)

                  # For displaying information about an event
                  status = new Label("")
                  layout.addComponent(status)

                  setCompositionRoot(layout)


              def componentEvent(event):
                  # Act according to the source of the event
                  if (event.getSource() == ok):
                      getWindow().showNotification("Click!")

                  status.setValue("Event from " +
                          event.getSource().__class__.__name__
                          + ": " + event.__class__.__name__)


          listening = Listening()
          layout.addComponent(listening)

        @param listener:
                   the new IListener to be registered.
        @see: L{component.Event}
        @see: L{removeListener}
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Removes a previously registered component event listener from this
        component.

        @param listener:
                   the listener to be removed.
        @see: L{addListener}
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


class Event(EventObject):
    """Superclass of all component originated events.

    Events are the basis of all user interaction handling in Muntjac. To
    handle events, you provide a listener object that receives the events of
    the particular event type::

    Notice that while each of the event types have their corresponding
    listener types; the listener interfaces are not required to inherit the
    C{IComponent.IListener} interface.

    @see: L{component.IListener}
    """

    def __init__(self, source):
        """Constructs a new event with the specified source component.

        @param source:
                   the source component of the event
        """
        super(Event, self).__init__(source)


    def getComponent(self):
        """Gets the component where the event occurred.

        @return: the source component of the event
        """
        return self.getSource()


class IListener(IEventListener):
    """IListener interface for receiving C{component.Event}s.

    IListener interfaces are the basis of all user interaction handling in
    Muntjac. You have or create a listener object that receives the events.
    All event types have their corresponding listener types; they are not,
    however, required to inherit the C{component.IListener} interface,
    and they rarely do so.

    This generic listener interface is useful typically when you wish to
    handle events from different component types in a single listener method
    (C{componentEvent()}. If you handle component events in an anonymous
    listener class, you normally use the component specific listener class,
    such as L{button.ClickEvent}::


      class Listening(CustomComponent, IListener):
          ok = None  # Stored for determining the source of an event

          status = None  # For displaying info about the event

          def __init__(self):
              layout = VerticalLayout()

              # Some miscellaneous component
              name = TextField("Say it all here")
              name.addListener(self)
              name.setImmediate(True)
              layout.addComponent(name)

              # Handle button clicks as generic events instead
              # of Button.ClickEvent events
              ok = new Button("OK")
              ok.addListener(self)
              layout.addComponent(ok)

              # For displaying information about an event
              status = Label("")
              layout.addComponent(status)

              setCompositionRoot(layout)


          def componentEvent(event):
              # Act according to the source of the event
              if (event.getSource() == ok
                      and event__class__ == Button.ClickEvent):
                  getWindow().showNotification("Click!")

              # Display source component and event class names
              status.setValue("Event from " +
                      event.getSource().__class__.__name__
                      + ": " + event.__class__.__name__)

      listening = Listening()
      layout.addComponent(listening)

    @see: L{IComponent.addListener}
    """

    def componentEvent(self, event):
        """Notifies the listener of a component event.

        As the event can typically come from one of many source components,
        you may need to differentiate between the event source by component
        reference, class, etc::

          def componentEvent(event):
              # Act according to the source of the event
              if (event.getSource() == ok and
                      event.__class__ == button.ClickEvent):
                  getWindow().showNotification("Click!")

              # Display source component and event class names
              status.setValue("Event from " +
                      event.getSource().__class__.__name__
                      + ": " + event.__class__.__name__)

        @param event:
                   the event that has occured.
        """
        raise NotImplementedError


class ErrorEvent(Event):
    """Class of all component originated error events.

    The component error event is normally fired by
    L{AbstractComponent.setComponentError}. The component errors are set
    by the framework in some situations and can be set by user code. They
    are indicated in a component with an error indicator.
    """

    def __init__(self, message, component):
        """Constructs a new event with a specified source component.

        @param message:
                   the error message.
        @param component:
                   the source component.
        """
        super(ErrorEvent, self).__init__(component)
        self._message = message


    def getErrorMessage(self):
        """Gets the error message.

        @return: the error message.
        """
        return self._message


class IErrorListener(IEventListener):
    """IListener interface for receiving C{IComponent.Errors}s."""

    def componentError(self, event):
        """Notifies the listener of a component error.

        @param event:
                   the event that has occured.
        """
        raise NotImplementedError


class IFocusable(IComponent):
    """A sub-interface implemented by components that can obtain input focus.
    This includes all L{Field} components as well as some other
    components, such as L{Upload}.

    Focus can be set with L{focus}. This interface does not provide
    an accessor that would allow finding out the currently focused component;
    focus information can be acquired for some (but not all) L{Field}
    components through the L{IFocusListener} and L{IBlurListener} interfaces.

    @see: L{FieldEvents}
    """

    def focus(self):
        """Sets the focus to this component::

          loginBox = Form()
          loginBox.setCaption("Login")
          layout.addComponent(loginBox)

          # Create the first field which will be focused
          username = TextField("User name")
          loginBox.addField("username", username)

          # Set focus to the user name
          username.focus()

          password = TextField("Password")
          loginBox.addField("password", password)

          login = Button("Login")
          loginBox.getFooter().addComponent(login)

        Notice that this interface does not provide an accessor that would
        allow finding out the currently focused component. Focus information
        can be acquired for some (but not all) L{IField} components
        through the L{IFocusListener} and L{IBlurListener} interfaces.

        @see: L{FieldEvents}
        @see: L{FocusEvent}
        @see: L{IFocusListener}
        @see: L{BlurEvent}
        @see: L{IBlurListener}
        """
        raise NotImplementedError


    def getTabIndex(self):
        """Gets the I{tabulator index} of the C{IFocusable} component.

        @return: tab index set for the C{IFocusable} component
        @see: L{setTabIndex}
        """
        raise NotImplementedError


    def setTabIndex(self, tabIndex):
        """Sets the I{tabulator index} of the C{IFocusable} component.
        The tab index property is used to specify the order in which the
        fields are focused when the user presses the Tab key. Components with
        a defined tab index are focused sequentially first, and then the
        components with no tab index::

          loginBox = Form()
          loginBox.setCaption("Login")
          layout.addComponent(loginBox)

          # Create the first field which will be focused
          username = TextField("User name")
          loginBox.addField("username", username)

          # Set focus to the user name
          username.focus()

          password = TextField("Password")
          loginBox.addField("password", password)

          login = Button("Login")
          loginBox.getFooter().addComponent(login)

          # An additional component which natural focus order would
          # be after the button.
          remember = CheckBox("Remember me")
          loginBox.getFooter().addComponent(remember)

          username.setTabIndex(1)
          password.setTabIndex(2)
          remember.setTabIndex(3)  # Different than natural place
          login.setTabIndex(4)

        After all focusable user interface components are done, the browser
        can begin again from the component with the smallest tab index, or it
        can take the focus out of the page, for example, to the location bar.

        If the tab index is not set (is set to zero), the default tab order
        is used. The order is somewhat browser-dependent, but generally
        follows the HTML structure of the page.

        A negative value means that the component is completely removed from
        the tabulation order and can not be reached by pressing the Tab key
        at all.

        @param tabIndex:
                   the tab order of this component. Indexes usually start
                   from 1. Zero means that default tab order should be used.
                   A negative value means that the field should not be
                   included in the tabbing sequence.
        @see: L{getTabIndex}
        """
        raise NotImplementedError
