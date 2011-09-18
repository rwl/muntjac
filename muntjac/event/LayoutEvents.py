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

from com.vaadin.tools.ReflectTools import (ReflectTools,)
from com.vaadin.event.ComponentEventListener import (ComponentEventListener,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)


class LayoutEvents(object):

    class LayoutClickListener(ComponentEventListener):
        clickMethod = ReflectTools.findMethod(LayoutClickListener, 'layoutClick', LayoutClickEvent)

        def layoutClick(self, event):
            """Layout has been clicked

            @param event
                       Component click event.
            """
            pass

    class LayoutClickNotifier(Serializable):
        """The interface for adding and removing <code>LayoutClickEvent</code>
        listeners. By implementing this interface a class explicitly announces
        that it will generate a <code>LayoutClickEvent</code> when a component
        inside it is clicked and a <code>LayoutClickListener</code> is
        registered.
        <p>
        Note: The general Java convention is not to explicitly declare that a
        class generates events, but to directly define the
        <code>addListener</code> and <code>removeListener</code> methods. That
        way the caller of these methods has no real way of finding out if the
        class really will send the events, or if it just defines the methods to
        be able to implement an interface.
        </p>

        @since 6.5.2
        @see LayoutClickListener
        @see LayoutClickEvent
        """

        def addListener(self, listener):
            """Add a click listener to the layout. The listener is called whenever
            the user clicks inside the layout. An event is also triggered when
            the click targets a component inside a nested layout or Panel,
            provided the targeted component does not prevent the click event from
            propagating. A caption is not considered part of a component.

            The child component that was clicked is included in the
            {@link LayoutClickEvent}.

            Use {@link #removeListener(LayoutClickListener)} to remove the
            listener.

            @param listener
                       The listener to add
            """
            pass

        def removeListener(self, listener):
            """Removes an LayoutClickListener.

            @param listener
                       LayoutClickListener to be removed
            """
            pass

    class LayoutClickEvent(ClickEvent):
        """An event fired when the layout has been clicked. The event contains
        information about the target layout (component) and the child component
        that was clicked. If no child component was found it is set to null.
        """
        _clickedComponent = None
        _childComponent = None

        def __init__(self, source, mouseEventDetails, clickedComponent, childComponent):
            super(LayoutClickEvent, self)(source, mouseEventDetails)
            self._clickedComponent = clickedComponent
            self._childComponent = childComponent

        def getClickedComponent(self):
            """Returns the component that was clicked, which is somewhere inside the
            parent layout on which the listener was registered.

            For the direct child component of the layout, see
            {@link #getChildComponent()}.

            @return clicked {@link Component}, null if none found
            """
            return self._clickedComponent

        def getChildComponent(self):
            """Returns the direct child component of the layout which contains the
            clicked component.

            For the clicked component inside that child component of the layout,
            see {@link #getClickedComponent()}.

            @return direct child {@link Component} of the layout which contains
                    the clicked Component, null if none found
            """
            return self._childComponent
