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

from muntjac.ui.Component import Component, Event


class ComponentContainer(Component):
    """Extension to the {@link Component} interface which adds to it the capacity to
    contain other components. All UI elements that can have child elements
    implement this interface.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def addComponent(self, c):
        """Adds the component into this container.

        @param c
                   the component to be added.
        """
        pass


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c
                   the component to be removed.
        """
        pass


    def removeAllComponents(self):
        """Removes all components from this container."""
        pass


    def replaceComponent(self, oldComponent, newComponent):
        """Replaces the component in the container with another one without changing
        position.

        <p>
        This method replaces component with another one is such way that the new
        component overtakes the position of the old component. If the old
        component is not in the container, the new component is added to the
        container. If the both component are already in the container, their
        positions are swapped. Component attach and detach events should be taken
        care as with add and remove.
        </p>

        @param oldComponent
                   the old component that will be replaced.
        @param newComponent
                   the new component to be replaced.
        """
        pass


    def getComponentIterator(self):
        """Gets an iterator to the collection of contained components. Using this
        iterator it is possible to step through all components contained in this
        container.

        @return the component iterator.
        """
        pass


    def requestRepaintAll(self):
        """Causes a repaint of this component, and all components below it.

        This should only be used in special cases, e.g when the state of a
        descendant depends on the state of a ancestor.
        """
        pass


    def moveComponentsFrom(self, source):
        """Moves all components from an another container into this container. The
        components are removed from <code>source</code>.

        @param source
                   the container which contains the components that are to be
                   moved to this container.
        """
        pass


    def addListener(self, listener):
        """Listens the component attach events.

        @param listener
                   the listener to add.
        ---
        Listens the component detach events.
        """


    def removeListener(self, listener):
        """Stops the listening component attach events.

        @param listener
                   the listener to removed.
        ---
        Stops the listening component detach events.
        """


class ComponentAttachListener(object):
    """Component attach listener interface."""

    def componentAttachedToContainer(self, event):
        """A new component is attached to container.

        @param event
                   the component attach event.
        """
        pass


class ComponentDetachListener(object):
    """Component detach listener interface."""

    def componentDetachedFromContainer(self, event):
        """A component has been detached from container.

        @param event
                   the component detach event.
        """
        pass


class ComponentAttachEvent(Event):
    """Component attach event sent when a component is attached to container."""

    def __init__(self, container, attachedComponent):
        """Creates a new attach event.

        @param container
                   the component container the component has been detached
                   to.
        @param attachedComponent
                   the component that has been attached.
        """
        super(ComponentAttachEvent, self)(container)
        self._component = attachedComponent


    def getContainer(self):
        """Gets the component container.

        @param the
                   component container.
        """
        return self.getSource()


    def getAttachedComponent(self):
        """Gets the attached component.

        @param the
                   attach component.
        """
        return self._component


class ComponentDetachEvent(Event):
    """Component detach event sent when a component is detached from container."""

    def __init__(self, container, detachedComponent):
        """Creates a new detach event.

        @param container
                   the component container the component has been detached
                   from.
        @param detachedComponent
                   the component that has been detached.
        """
        super(ComponentDetachEvent, self)(container)
        self._component = detachedComponent


    def getContainer(self):
        """Gets the component container.

        @param the
                   component container.
        """
        return self.getSource()


    def getDetachedComponent(self):
        """Gets the detached component.

        @return the detached component.
        """
        return self._component
