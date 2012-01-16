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

"""Defines an extension to the C{IComponent} interface which adds to it the
capacity to contain other components."""

from muntjac.ui.component import IComponent, Event


class IComponentContainer(IComponent):
    """Extension to the L{IComponent} interface which adds to it the
    capacity to contain other components. All UI elements that can have child
    elements implement this interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def addComponent(self, c):
        """Adds the component into this container.

        @param c: the component to be added.
        """
        raise NotImplementedError


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c: the component to be removed.
        """
        raise NotImplementedError


    def removeAllComponents(self):
        """Removes all components from this container."""
        raise NotImplementedError


    def replaceComponent(self, oldComponent, newComponent):
        """Replaces the component in the container with another one without
        changing position.

        This method replaces component with another one is such way that the
        new component overtakes the position of the old component. If the old
        component is not in the container, the new component is added to the
        container. If the both component are already in the container, their
        positions are swapped. IComponent attach and detach events should be
        taken care as with add and remove.

        @param oldComponent:
                   the old component that will be replaced.
        @param newComponent:
                   the new component to be replaced.
        """
        raise NotImplementedError


    def getComponentIterator(self):
        """Gets an iterator to the collection of contained components. Using
        this iterator it is possible to step through all components contained
        in this container.

        @return: the component iterator.
        """
        raise NotImplementedError


    def requestRepaintAll(self):
        """Causes a repaint of this component, and all components below it.

        This should only be used in special cases, e.g when the state of a
        descendant depends on the state of a ancestor.
        """
        raise NotImplementedError


    def moveComponentsFrom(self, source):
        """Moves all components from an another container into this container.
        The components are removed from C{source}.

        @param source:
                   the container which contains the components that are to be
                   moved to this container.
        """
        raise NotImplementedError


    def addListener(self, listener, iface=None):
        """Listens the component attach/detach events.

        @param listener:
                   the listener to add.
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Stops the listening component attach/detach events.

        @param listener:
                   the listener to removed.
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


class IComponentAttachListener(object):
    """IComponent attach listener interface."""

    def componentAttachedToContainer(self, event):
        """A new component is attached to container.

        @param event:
                   the component attach event.
        """
        raise NotImplementedError


class IComponentDetachListener(object):
    """IComponent detach listener interface."""

    def componentDetachedFromContainer(self, event):
        """A component has been detached from container.

        @param event:
                   the component detach event.
        """
        raise NotImplementedError


class ComponentAttachEvent(Event):
    """IComponent attach event sent when a component is attached to container.
    """

    def __init__(self, container, attachedComponent):
        """Creates a new attach event.

        @param container:
                   the component container the component has been
                   detached to.
        @param attachedComponent:
                   the component that has been attached.
        """
        super(ComponentAttachEvent, self).__init__(container)
        self._component = attachedComponent


    def getContainer(self):
        """Gets the component container.

        @return: the component container.
        """
        return self.getSource()


    def getAttachedComponent(self):
        """Gets the attached component.

        @return: the attach component.
        """
        return self._component


class ComponentDetachEvent(Event):
    """IComponent detach event sent when a component is detached from
    container."""

    def __init__(self, container, detachedComponent):
        """Creates a new detach event.

        @param container:
                   the component container the component has been
                   detached from.
        @param detachedComponent:
                   the component that has been detached.
        """
        super(ComponentDetachEvent, self).__init__(container)
        self._component = detachedComponent


    def getContainer(self):
        """Gets the component container.

        @return: the component container.
        """
        return self.getSource()


    def getDetachedComponent(self):
        """Gets the detached component.

        @return: the detached component.
        """
        return self._component
