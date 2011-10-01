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

from muntjac.terminal.IScrollable import IScrollable
from muntjac.event.ActionManager import ActionManager
from muntjac.event import Action
from muntjac.ui.VerticalLayout import VerticalLayout
from muntjac.ui.AbstractComponentContainer import AbstractComponentContainer

from muntjac.ui import IComponentContainer

from muntjac.ui.IComponent import IFocusable
from muntjac.ui.ILayout import ILayout
from muntjac.event.MouseEvents import ClickEvent, IClickListener

from muntjac.terminal.gwt.client.MouseEventDetails import MouseEventDetails
from muntjac.terminal.gwt.client.ui.VPanel import VPanel
from muntjac.ui.AbstractComponent import AbstractComponent


class Panel(AbstractComponentContainer, IScrollable,
            IComponentContainer.IComponentAttachListener,
            IComponentContainer.IComponentDetachListener,
            Action.INotifier, IFocusable):
    """Panel - a simple single component container.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    #CLIENT_WIDGET = ClientWidget(VPanel, LoadStyle.EAGER)

    _CLICK_EVENT = VPanel.CLICK_EVENT_IDENTIFIER

    # Removes extra decorations from the Panel.
    #
    # @deprecated this style is no longer part of the core framework and this
    #             component, even though most built-in themes implement this
    #             style. Use the constant specified in the theme class file
    #             that you're using, if it provides one, e.g.
    #             {@link Reindeer#PANEL_LIGHT} or {@link Runo#PANEL_LIGHT} .
    STYLE_LIGHT = 'light'


    def __init__(self, *args):
        """Creates a new empty panel. A VerticalLayout is used as content.
        ---
        Creates a new empty panel which contains the given content. The
        content cannot be null.

        @param content
                   the content for the panel.
        ---
        Creates a new empty panel with caption. Default layout is used.

        @param caption
                   the caption used in the panel.
        ---
        Creates a new empty panel with the given caption and content.

        @param caption
                   the caption of the panel.
        @param content
                   the content used in the panel.
        """
        # Content of the panel.
        self._content = None

        # Scroll X position.
        self._scrollOffsetX = 0

        # Scroll Y position.
        self._scrollOffsetY = 0

        # Scrolling mode.
        self._scrollable = False

        # Keeps track of the Actions added to this component, and manages
        # the painting and handling as well.
        self.actionManager = None

        # By default the Panel is not in the normal document focus flow and
        # can only be focused by using the focus()-method. Change this to 0
        # if you want to have the Panel in the normal focus flow.
        self._tabIndex = -1

        nargs = len(args)
        if nargs == 0:
            self.__init__(None)
        elif nargs == 1:
            if isinstance(args[0], IComponentContainer):
                content, = args
                self.setContent(content)
                self.setWidth(100, self.UNITS_PERCENTAGE)
            else:
                caption, = args
                self.__init__(caption, None)
        elif nargs == 2:
            caption, content = args
            self.__init__(content)
            self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'


    def getLayout(self):
        """Gets the current layout of the panel.

        @return the Current layout of the panel.
        @deprecated A Panel can now contain a IComponentContainer which is not
                    necessarily a ILayout. Use {@link #getContent()} instead.
        """
        raise DeprecationWarning, 'Use getContent() instead'

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

        Components from old layout are not moved to new layout by default
        (changed in 5.2.2). Use function in ILayout interface manually.

        @param newLayout
                   the New layout of the panel.
        @deprecated A Panel can now contain a IComponentContainer which is not
                    necessarily a ILayout. Use
                    {@link #setContent(IComponentContainer)} instead.
        """
        self.setContent(newLayout)


    def getContent(self):
        """Returns the content of the Panel.

        @return
        """
        return self._content


    def setContent(self, newContent):
        """Set the content of the Panel. If null is given as the new content
        then a layout is automatically created and set as the content.

        @param content: The new content
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
            self._content.removeListener(self)
            self._content.removeListener(self)

        # Sets the panel to be parent for the content
        newContent.setParent(self)

        # Sets the new content
        self._content = newContent

        # Adds the event listeners for new content
        newContent.addListener(self)
        newContent.addListener(self)

        self._content = newContent


    def createDefaultContent(self):
        """Create a IComponentContainer which is added by default to
        the Panel if user does not specify any content.

        @return
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
        @see AbstractComponentContainer#addComponent()
        """
        self._content.addComponent(c)
        # No repaint request is made as we except the underlying
        # container to request repaints


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c: The component to be removed.
        @see AbstractComponentContainer.removeComponent()
        """
        self._content.removeComponent(c)
        # No repaint request is made as we except the underlying
        # container to request repaints


    def getComponentIterator(self):
        """Gets the component container iterator for going through
        all the components in the container.

        @return the Iterator of the components inside the container.
        @see com.vaadin.ui.IComponentContainer#getComponentIterator()
        """
        return self._content.getComponentIterator()


    def changeVariables(self, source, variables):
        """Called when one or more variables handled by the implementing
        class are changed.

        @see com.vaadin.terminal.VariableOwner#changeVariables(Object, Map)
        """
        super(Panel, self).changeVariables(source, variables)

        if self._CLICK_EVENT in variables:
            self.fireClick(variables[self._CLICK_EVENT])

        # Get new size
        newWidth = variables.get('width')
        newHeight = variables.get('height')

        if newWidth is not None and int(newWidth) != self.getWidth():
            self.setWidth(int(newWidth), self.UNITS_PIXELS)

        if newHeight is not None and int(newHeight) != self.getHeight():
            self.setHeight(int(newHeight), self.UNITS_PIXELS)

        # Scrolling
        newScrollX = variables.get('scrollLeft')
        newScrollY = variables.get('scrollTop')
        if newScrollX is not None and int(newScrollX) != self.getScrollLeft():
            # set internally, not to fire request repaint
            self._scrollOffsetX = int(newScrollX)

        if newScrollY is not None and int(newScrollY) != self.getScrollTop():
            # set internally, not to fire request repaint
            self._scrollOffsetY = int(newScrollY)

        # Actions
        if self.actionManager is not None:
            self.actionManager.handleActions(variables, self)


    def getScrollLeft(self):
        return self._scrollOffsetX


    def getScrollOffsetX(self):
        """@deprecated use {@link #getScrollLeft()} instead"""
        raise DeprecationWarning, 'use getScrollLeft() instead'
        return self.getScrollLeft()


    def getScrollTop(self):
        return self._scrollOffsetY


    def getScrollOffsetY(self):
        """@deprecated use {@link #getScrollTop()} instead"""
        raise DeprecationWarning, 'use getScrollTop() instead'
        return self.getScrollTop()


    def isScrollable(self):
        return self._scrollable


    def setScrollable(self, isScrollingEnabled):
        if self._scrollable != isScrollingEnabled:
            self._scrollable = isScrollingEnabled
            self.requestRepaint()


    def setScrollLeft(self, pixelsScrolled):
        if pixelsScrolled < 0:
            raise ValueError, 'Scroll offset must be at least 0'

        if self._scrollOffsetX != pixelsScrolled:
            self._scrollOffsetX = pixelsScrolled
            self.requestRepaint()


    def setScrollOffsetX(self, pixels):
        """@deprecated use setScrollLeft() method instead"""
        raise DeprecationWarning, 'use setScrollLeft() method instead'
        self.setScrollLeft(pixels)


    def setScrollTop(self, pixelsScrolledDown):
        if pixelsScrolledDown < 0:
            raise ValueError, 'Scroll offset must be at least 0'
        if self._scrollOffsetY != pixelsScrolledDown:
            self._scrollOffsetY = pixelsScrolledDown
            self.requestRepaint()


    def setScrollOffsetY(self, pixels):
        """@deprecated use setScrollTop() method instead"""
        raise DeprecationWarning, 'use setScrollTop() method instead'
        self.setScrollTop(pixels)


    def replaceComponent(self, oldComponent, newComponent):
        self._content.replaceComponent(oldComponent, newComponent)


    def componentAttachedToContainer(self, event):
        """A new component is attached to container.

        @see IComponentAttachListener.componentAttachedToContainer()
        """
        if event.getContainer() == self._content:
            self.fireComponentAttachEvent(event.getAttachedComponent())


    def componentDetachedFromContainer(self, event):
        """A component has been detached from container.

        @see IComponentDetachListener.componentDetachedFromContainer()
        """
        if event.getContainer() == self._content:
            self.fireComponentDetachEvent(event.getDetachedComponent())


    def attach(self):
        """Notifies the component that it is connected to an application.

        @see com.vaadin.ui.Component#attach()
        """
        # can't call parent here as this is Panels hierarchy is a hack
        self.requestRepaint()
        if self._content is not None:
            self._content.attach()


    def detach(self):
        """Notifies the component that it is detached from the application.

        @see com.vaadin.ui.Component#detach()
        """
        # can't call parent here as this is Panels hierarchy is a hack
        if self._content is not None:
            self._content.detach()


    def removeAllComponents(self):
        """Removes all components from this container.

        @see com.vaadin.ui.IComponentContainer#removeAllComponents()
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


    def addListener(self, listener):
        """Add a click listener to the Panel. The listener is called whenever
        the user clicks inside the Panel. Also when the click targets a
        component inside the Panel, provided the targeted component does not
        prevent the click event from propagating.

        Use {@link #removeListener(ClickListener)} to remove the listener.

        @param listener
                   The listener to add
        """
        AbstractComponent.addListener(self, self._CLICK_EVENT, ClickEvent,
                listener, IClickListener.clickMethod)


    def removeListener(self, listener):
        """Remove a click listener from the Panel. The listener should earlier
        have been added using {@link #addListener(ClickListener)}.

        @param listener
                   The listener to remove
        """
        AbstractComponent.removeListener(self, self._CLICK_EVENT, ClickEvent,
                listener)


    def fireClick(self, parameters):
        """Fire a click event to all click listeners.

        @param object
                   The raw "value" of the variable change from the client side
        """
        mouseDetails = MouseEventDetails.deSerialize(
                parameters.get('mouseDetails'))
        self.fireEvent( ClickEvent(self, mouseDetails) )


    def getTabIndex(self):
        """{@inheritDoc}"""
        return self._tabIndex


    def setTabIndex(self, tabIndex):
        """{@inheritDoc}"""
        self._tabIndex = tabIndex
        self.requestRepaint()


    def focus(self):
        """Moves keyboard focus to the component. {@see IFocusable#focus()}"""
        super(Panel, self).focus()
