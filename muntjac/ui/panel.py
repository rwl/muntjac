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

"""Defines a simple single component container."""

from warnings import warn

from muntjac.terminal.scrollable import IScrollable
from muntjac.event.action_manager import ActionManager
from muntjac.event import action
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.ui.abstract_component_container import AbstractComponentContainer

from muntjac.ui import component_container

from muntjac.ui.component import IFocusable
from muntjac.ui.layout import ILayout
from muntjac.event.mouse_events import ClickEvent, IClickListener

from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.ui.v_panel import VPanel


class Panel(AbstractComponentContainer, IScrollable,
            component_container.IComponentAttachListener,
            component_container.IComponentDetachListener,
            action.INotifier, IFocusable):
    """Panel - a simple single component container.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VPanel, LoadStyle.EAGER)

    _CLICK_EVENT = VPanel.CLICK_EVENT_IDENTIFIER

    # Removes extra decorations from the Panel.
    #
    # @deprecated: this style is no longer part of the core framework and this
    #             component, even though most built-in themes implement this
    #             style. Use the constant specified in the theme class file
    #             that you're using, if it provides one, e.g.
    #             L{Reindeer#PANEL_LIGHT} or L{Runo#PANEL_LIGHT} .
    STYLE_LIGHT = 'light'


    def __init__(self, *args):
        """Creates a new panel with caption and or content. A VerticalLayout
        is used as content by default.

        @param args: tuple of the form
            - (content)
              1. the content for the panel (HTML/XHTML).
            - (caption)
              1. the caption used in the panel (HTML/XHTML).
            - (caption, content)
              1. the caption of the panel.
              2. the content used in the panel (HTML/XHTML).
        """
        super(Panel, self).__init__()

        #: Content of the panel.
        self._content = None

        #: Scroll X position.
        self._scrollOffsetX = 0

        #: Scroll Y position.
        self._scrollOffsetY = 0

        #: Scrolling mode.
        self._scrollable = False

        #: Keeps track of the Actions added to this component, and manages
        #  the painting and handling as well.
        self.actionManager = None

        #: By default the Panel is not in the normal document focus flow and
        #  can only be focused by using the focus()-method. Change this to 0
        #  if you want to have the Panel in the normal focus flow.
        self._tabIndex = -1

        nargs = len(args)
        if nargs == 0:
            Panel.__init__(self, None)
        elif nargs == 1:
            if isinstance(args[0], basestring):
                caption, = args
                Panel.__init__(self, caption, None)
                self.setCaption(caption)
            else:
                content, = args
                self.setContent(content)
                self.setWidth(100, self.UNITS_PERCENTAGE)
        elif nargs == 2:
            caption, content = args
            Panel.__init__(self, content)
            self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    def setCaption(self, caption):
        """Sets the caption of the panel.

        Note that the caption is interpreted as HTML/XHTML and therefore care
        should be taken not to enable HTML injection and XSS attacks using
        panel captions. This behavior may change in future versions.

        @see L{AbstractComponent.setCaption}
        """
        super(Panel, self).setCaption(caption)


    def getLayout(self):
        """Gets the current layout of the panel.

        @return: the Current layout of the panel.
        @deprecated: A Panel can now contain a IComponentContainer which is not
                     necessarily a ILayout. Use L{getContent} instead.
        """
        warn('Use getContent() instead', DeprecationWarning)

        if isinstance(self._content, ILayout):
            return self._content
        elif self._content is None:
            return None
        raise ValueError, ('Panel does not contain a ILayout. '
                'Use getContent() instead of getLayout().')


    def setLayout(self, newLayout):
        """Sets the layout of the panel.

        If given layout is null, a VerticalLayout with margins set is used
        as a default.

        Components from old layout are not moved to new layout by default.
        Use function in ILayout interface manually.

        @param newLayout:
                   the New layout of the panel.
        @deprecated: A Panel can now contain a IComponentContainer which is
                     not necessarily a ILayout. Use L{setContent} instead.
        """
        self.setContent(newLayout)


    def getContent(self):
        """Returns the content of the Panel.
        """
        return self._content


    def setContent(self, newContent):
        """Set the content of the Panel. If null is given as the new content
        then a layout is automatically created and set as the content.

        @param newContent: The new content
        """
        # If the content is null we create the default content
        if newContent is None:
            newContent = self.createDefaultContent()

        # if newContent is None:
        #     raise ValueError, "Content cannot be null"

        if newContent == self._content:
            return  # don't set the same content twice

        # detach old content if present
        if self._content is not None:
            self._content.setParent(None)
            self._content.removeListener(self,
                    component_container.IComponentAttachListener)
            self._content.removeListener(self,
                    component_container.IComponentDetachListener)

        # Sets the panel to be parent for the content
        newContent.setParent(self)

        # Sets the new content
        self._content = newContent

        # Adds the event listeners for new content
        newContent.addListener(self,
                component_container.IComponentAttachListener)
        newContent.addListener(self,
                component_container.IComponentDetachListener)

        self._content = newContent


    def createDefaultContent(self):
        """Create a IComponentContainer which is added by default to
        the Panel if user does not specify any content.
        """
        layout = VerticalLayout()
        # Force margins by default
        layout.setMargin(True)
        return layout


    def paintContent(self, target):
        self._content.paint(target)

        target.addVariable(self, 'tabindex', self.getTabIndex())

        if self.isScrollable():
            target.addVariable(self, 'scrollLeft', self.getScrollLeft())
            target.addVariable(self, 'scrollTop', self.getScrollTop())

        if self.actionManager is not None:
            self.actionManager.paintActions(None, target)


    def requestRepaintAll(self):
        # Panel has odd structure, delegate to layout
        self.requestRepaint()
        if self.getContent() is not None:
            self.getContent().requestRepaintAll()


    def addComponent(self, c):
        """Adds the component into this container.

        @param c: the component to be added.
        @see: L{AbstractComponentContainer.addComponent}
        """
        self._content.addComponent(c)
        # No repaint request is made as we except the underlying
        # container to request repaints


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c: The component to be removed.
        @see: L{AbstractComponentContainer.removeComponent}
        """
        self._content.removeComponent(c)
        # No repaint request is made as we except the underlying
        # container to request repaints


    def getComponentIterator(self):
        """Gets the component container iterator for going through
        all the components in the container.

        @return: the iterator of the components inside the container.
        @see: L{IComponentContainer.getComponentIterator}
        """
        return self._content.getComponentIterator()


    def changeVariables(self, source, variables):
        """Called when one or more variables handled by the implementing
        class are changed.

        @see: L{muntjac.terminal.VariableOwner.changeVariables}
        """
        super(Panel, self).changeVariables(source, variables)

        if self._CLICK_EVENT in variables:
            self.fireClick(variables[self._CLICK_EVENT])

        # Get new size
        newWidth = variables.get('width')
        newHeight = variables.get('height')

        if newWidth is not None and newWidth != self.getWidth():
            self.setWidth(newWidth, self.UNITS_PIXELS)

        if newHeight is not None and newHeight != self.getHeight():
            self.setHeight(newHeight, self.UNITS_PIXELS)

        # Scrolling
        newScrollX = variables.get('scrollLeft')
        newScrollY = variables.get('scrollTop')
        if newScrollX is not None and newScrollX != self.getScrollLeft():
            # set internally, not to fire request repaint
            self._scrollOffsetX = newScrollX

        if newScrollY is not None and newScrollY != self.getScrollTop():
            # set internally, not to fire request repaint
            self._scrollOffsetY = newScrollY

        # Actions
        if self.actionManager is not None:
            self.actionManager.handleActions(variables, self)


    def getScrollLeft(self):
        return self._scrollOffsetX


    def getScrollOffsetX(self):
        """@deprecated: use L{getScrollLeft} instead"""
        warn('use getScrollLeft() instead', DeprecationWarning)
        return self.getScrollLeft()


    def getScrollTop(self):
        return self._scrollOffsetY


    def getScrollOffsetY(self):
        """@deprecated: use L{getScrollTop} instead"""
        warn('use getScrollTop() instead', DeprecationWarning)
        return self.getScrollTop()


    def isScrollable(self):
        return self._scrollable


    def setScrollable(self, isScrollingEnabled):
        """Sets the panel as programmatically scrollable.

        Panel is by default not scrollable programmatically with
        L{setScrollLeft} and L{setScrollTop}, so if you use those methods,
        you need to enable scrolling with this method. Components that
        extend Panel may have a different default for the programmatic
        scrollability.

        @see: L{IScrollable.setScrollable}
        """
        if self._scrollable != isScrollingEnabled:
            self._scrollable = isScrollingEnabled
            self.requestRepaint()


    def setScrollLeft(self, pixelsScrolled):
        """Sets the horizontal scroll position.

        Setting the horizontal scroll position with this method requires that
        programmatic scrolling of the component has been enabled. For Panel it
        is disabled by default, so you have to call L{setScrollable}.
        Components extending Panel may have a different default for
        programmatic scrollability.

        @see: L{IScrollable.setScrollable}
        @see: L{setScrollable}
        """
        if pixelsScrolled < 0:
            raise ValueError, 'Scroll offset must be at least 0'

        if self._scrollOffsetX != pixelsScrolled:
            self._scrollOffsetX = pixelsScrolled
            self.requestRepaint()


    def setScrollOffsetX(self, pixels):
        """@deprecated: use setScrollLeft() method instead"""
        warn('use setScrollLeft() method instead', DeprecationWarning)
        self.setScrollLeft(pixels)


    def setScrollTop(self, pixelsScrolledDown):
        """Sets the vertical scroll position.

        Setting the vertical scroll position with this method requires that
        programmatic scrolling of the component has been enabled. For Panel
        it is disabled by default, so you have to call L{setScrollable}.
        Components extending Panel may have a different default for
        programmatic scrollability.

        @see: L{IScrollable.setScrollTop}
        @see: L{setScrollable}
        """
        if pixelsScrolledDown < 0:
            raise ValueError, 'Scroll offset must be at least 0'
        if self._scrollOffsetY != pixelsScrolledDown:
            self._scrollOffsetY = pixelsScrolledDown
            self.requestRepaint()


    def setScrollOffsetY(self, pixels):
        """@deprecated: use setScrollTop() method instead"""
        warn('use setScrollTop() method instead', DeprecationWarning)
        self.setScrollTop(pixels)


    def replaceComponent(self, oldComponent, newComponent):
        self._content.replaceComponent(oldComponent, newComponent)


    def componentAttachedToContainer(self, event):
        """A new component is attached to container.

        @see: L{IComponentAttachListener.componentAttachedToContainer}
        """
        if event.getContainer() == self._content:
            self.fireComponentAttachEvent(event.getAttachedComponent())


    def componentDetachedFromContainer(self, event):
        """A component has been detached from container.

        @see: L{IComponentDetachListener.componentDetachedFromContainer}
        """
        if event.getContainer() == self._content:
            self.fireComponentDetachEvent(event.getDetachedComponent())


    def attach(self):
        """Notifies the component that it is connected to an application.

        @see: L{IComponent.attach}
        """
        # can't call parent here as this is Panels hierarchy is a hack
        self.requestRepaint()
        if self._content is not None:
            self._content.attach()


    def detach(self):
        """Notifies the component that it is detached from the application.

        @see: L{IComponent.detach}
        """
        # can't call parent here as this is Panels hierarchy is a hack
        if self._content is not None:
            self._content.detach()


    def removeAllComponents(self):
        """Removes all components from this container.

        @see: L{IComponentContainer.removeAllComponents}
        """
        self._content.removeAllComponents()


    def getActionManager(self):
        if self.actionManager is None:
            self.actionManager = ActionManager(self)
        return self.actionManager


    def addAction(self, action):
        self.getActionManager().addAction(action)


    def removeAction(self, action):
        if self.actionManager is not None:
            self.actionManager.removeAction(action)


    def addActionHandler(self, actionHandler):
        self.getActionManager().addActionHandler(actionHandler)


    def removeActionHandler(self, actionHandler):
        if self.actionManager is not None:
            self.actionManager.removeActionHandler(actionHandler)


    def removeAllActionHandlers(self):
        """Removes all action handlers"""
        if self.actionManager is not None:
            self.actionManager.removeAllActionHandlers()


    def addListener(self, listener, iface=None):
        """Add a click listener to the Panel. The listener is called whenever
        the user clicks inside the Panel. Also when the click targets a
        component inside the Panel, provided the targeted component does not
        prevent the click event from propagating.

        Use L{removeListener} to remove the listener.

        @param listener:
                   The listener to add
        """
        if (isinstance(listener, IClickListener) and
                (iface is None or issubclass(iface, IClickListener))):
            self.registerListener(self._CLICK_EVENT, ClickEvent,
                    listener, IClickListener.clickMethod)

        super(Panel, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ClickEvent):
            self.registerCallback(ClickEvent, callback,
                    self._CLICK_EVENT, *args)
        else:
            super(Panel, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Remove a click listener from the Panel. The listener should earlier
        have been added using L{addListener}.

        @param listener:
                   The listener to remove
        """
        if (isinstance(listener, IClickListener) and
                (iface is None or issubclass(iface, IClickListener))):
            self.withdrawListener(self._CLICK_EVENT, ClickEvent, listener)

        super(Panel, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ClickEvent):
            self.withdrawCallback(ClickEvent, callback, self._CLICK_EVENT)
        else:
            super(Panel, self).removeCallback(callback, eventType)


    def fireClick(self, parameters):
        """Fire a click event to all click listeners.

        @param parameters:
                   The raw "value" of the variable change from the client side
        """
        params = parameters.get('mouseDetails')
        mouseDetails = MouseEventDetails.deSerialize(params)
        self.fireEvent( ClickEvent(self, mouseDetails) )


    def getTabIndex(self):
        return self._tabIndex


    def setTabIndex(self, tabIndex):
        self._tabIndex = tabIndex
        self.requestRepaint()


    def focus(self):
        """Moves keyboard focus to the component.

        @see: L{IFocusable.focus}
        """
        super(Panel, self).focus()
