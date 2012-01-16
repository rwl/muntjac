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

"""Defines the default implementation for the methods in IComponentContainer.
"""

from muntjac.ui.abstract_component import AbstractComponent

from muntjac.ui.component_container import \
    ComponentAttachEvent, IComponentAttachListener, IComponentContainer, \
    ComponentDetachEvent, IComponentDetachListener


_COMPONENT_ATTACHED_METHOD = getattr(IComponentAttachListener,
        'componentAttachedToContainer')

_COMPONENT_DETACHED_METHOD = getattr(IComponentDetachListener,
        'componentDetachedFromContainer')


class AbstractComponentContainer(AbstractComponent, IComponentContainer):
    """Extension to L{AbstractComponent} that defines the default
    implementation for the methods in L{IComponentContainer}. Basic
    UI components that need to contain other components inherit this class
    to easily qualify as a component container.

    @author: Vaadin Ltd.
    @version: 1.1.0
    """

    def __init__(self):
        """Constructs a new component container."""
        super(AbstractComponentContainer, self).__init__()


    def removeAllComponents(self):
        """Removes all components from the container. This should probably
        be re-implemented in extending classes for a more powerful
        implementation.
        """
        l = list()

        # Adds all components
        for c in self.getComponentIterator():
            l.append(c)

        # Removes all components
        for c in l:
            self.removeComponent(c)


    def moveComponentsFrom(self, source):
        # Moves all components from an another container into this container.
        components = list()

        for c in self.getComponentIterator():
            components.append(c)

        for c in components:
            source.removeComponent(c)
            self.addComponent(c)


    def attach(self):
        """Notifies all contained components that the container is attached
        to a window.

        @see: L{IComponent.attach}
        """
        super(AbstractComponentContainer, self).attach()

        for c in self.getComponentIterator():
            c.attach()


    def detach(self):
        """Notifies all contained components that the container is detached
        from a window.

        @see: L{IComponent.detach}
        """
        # Events
        super(AbstractComponentContainer, self).detach()

        for c in self.getComponentIterator():
            c.detach()


    def addListener(self, listener, iface=None):
        if (isinstance(listener, IComponentAttachListener) and
                (iface is None or issubclass(iface, IComponentAttachListener))):
            self.registerListener(ComponentAttachEvent, listener,
                    _COMPONENT_ATTACHED_METHOD)

        if (isinstance(listener, IComponentDetachListener) and
                (iface is None or issubclass(iface, IComponentDetachListener))):
            self.registerListener(ComponentDetachEvent, listener,
                    _COMPONENT_DETACHED_METHOD)

        super(AbstractComponentContainer, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ComponentAttachEvent):
            self.registerCallback(ComponentAttachEvent, callback, None, *args)

        elif issubclass(eventType, ComponentDetachEvent):
            self.registerCallback(ComponentDetachEvent, callback, None, *args)

        else:
            super(AbstractComponentContainer, self).addCallback(callback,
                    eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, IComponentAttachListener) and
                (iface is None or issubclass(iface, IComponentAttachListener))):
            self.withdrawListener(ComponentAttachEvent, listener,
                    _COMPONENT_ATTACHED_METHOD)

        if (isinstance(listener, IComponentDetachListener) and
                (iface is None or issubclass(iface, IComponentDetachListener))):
            self.withdrawListener(ComponentDetachEvent, listener,
                    _COMPONENT_DETACHED_METHOD)

        super(AbstractComponentContainer, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, ComponentAttachEvent):
            self.withdrawCallback(ComponentAttachEvent, callback)

        elif issubclass(eventType, ComponentDetachEvent):
            self.withdrawCallback(ComponentDetachEvent, callback)

        else:
            super(AbstractComponentContainer, self).removeCallback(callback,
                    eventType)


    def fireComponentAttachEvent(self, component):
        """Fires the component attached event. This should be called by
        the addComponent methods after the component have been added to
        this container.

        @param component:
                   the component that has been added to this container.
        """
        event = ComponentAttachEvent(self, component)
        self.fireEvent(event)


    def fireComponentDetachEvent(self, component):
        """Fires the component detached event. This should be called by
        the removeComponent methods after the component have been removed
        from this container.

        @param component:
                   the component that has been removed from this container.
        """
        event = ComponentDetachEvent(self, component)
        self.fireEvent(event)


    def addComponent(self, c):
        """This only implements the events and component parent calls. The
        extending classes must implement component list maintenance and call
        this method after component list maintenance.

        @see: L{IComponentContainer.addComponent}
        """
        if isinstance(c, IComponentContainer):
            # Make sure we're not adding the component
            # inside it's own content
            parent = self
            while parent is not None:
                parent = parent.getParent()
                if parent == c:
                    msg = 'Component cannot be added inside it\'s own content'
                    raise ValueError, msg

        if c.getParent() is not None:
            # If the component already has a parent, try to remove it
            oldParent = c.getParent()
            oldParent.removeComponent(c)

        c.setParent(self)
        self.fireComponentAttachEvent(c)


    def removeComponent(self, c):
        """This only implements the events and component parent calls. The
        extending classes must implement component list maintenance and call
        this method before component list maintenance.

        @see: L{IComponentContainer.removeComponent}
        """
        if c.getParent() == self:
            c.setParent(None)
            self.fireComponentDetachEvent(c)


    def setEnabled(self, enabled):
        super(AbstractComponentContainer, self).setEnabled(enabled)

        if self.getParent() is not None and not self.getParent().isEnabled():
            # some ancestor still disabled, don't update children
            return
        else:
            self.requestRepaintAll()


    def setWidth(self, width, unit=None):
        if unit is not None:
            from muntjac.terminal.gwt.server.component_size_validator import \
                ComponentSizeValidator  # FIXME: circular import

            # child tree repaints may be needed, due to our fall back support
            # for invalid relative sizes
            dirtyChildren = None
            childrenMayBecomeUndefined = False
            if (self.getWidth() == self.SIZE_UNDEFINED
                    and width != self.SIZE_UNDEFINED):
                # children currently in invalid state may need repaint
                dirtyChildren = self.getInvalidSizedChildren(False)

            elif ((width == self.SIZE_UNDEFINED
                    and self.getWidth() != self.SIZE_UNDEFINED)
                  or (unit == self.UNITS_PERCENTAGE
                    and self.getWidthUnits() != self.UNITS_PERCENTAGE
                    and not ComponentSizeValidator.parentCanDefineWidth(self))):

                # relative width children may get to invalid state if width
                # becomes invalid. Width may also become invalid if units become
                # percentage due to the fallback support
                childrenMayBecomeUndefined = True
                dirtyChildren = self.getInvalidSizedChildren(False)

            super(AbstractComponentContainer, self).setWidth(width, unit)
            self.repaintChangedChildTrees(dirtyChildren,
                    childrenMayBecomeUndefined, False)
        else:
            super(AbstractComponentContainer, self).setWidth(width)


    def repaintChangedChildTrees(self, invalidChildren,
                                 childrenMayBecomeUndefined, vertical):
        if childrenMayBecomeUndefined:
            previouslyInvalidComponents = invalidChildren

            invalidChildren = self.getInvalidSizedChildren(vertical)

            if (previouslyInvalidComponents is not None
                    and invalidChildren is not None):
                for component in invalidChildren:
                    if component in previouslyInvalidComponents:
                        # still invalid don't repaint
                        previouslyInvalidComponents.remove(component)

        elif invalidChildren is not None:
            stillInvalidChildren = self.getInvalidSizedChildren(vertical)

            if stillInvalidChildren is not None:
                for component in stillInvalidChildren:
                    # didn't become valid
                    invalidChildren.remove(component)

        if invalidChildren is not None:
            self.repaintChildTrees(invalidChildren)


    def getInvalidSizedChildren(self, vertical):
        components = None

        from muntjac.ui.panel import Panel  # FIXME: circular import
        from muntjac.terminal.gwt.server.component_size_validator import \
            ComponentSizeValidator  # FIXME: circular import

        if isinstance(self, Panel):
            p = self
            content = p.getContent()
            if vertical:
                valid = ComponentSizeValidator.checkHeights(content)
            else:
                valid = ComponentSizeValidator.checkWidths(content)
            if not valid:
                components = set()
                components.add(content)
        else:
            for component in self.getComponentIterator():
                if vertical:
                    valid = ComponentSizeValidator.checkHeights(component)
                else:
                    valid = ComponentSizeValidator.checkWidths(component)
                if not valid:
                    if components is None:
                        components = set()
                    components.add(component)

        return components


    def repaintChildTrees(self, dirtyChildren):
        for c in dirtyChildren:
            if isinstance(c, IComponentContainer):
                c.requestRepaintAll()
            else:
                c.requestRepaint()


    def setHeight(self, height, unit=None):
        if unit is not None:
            from muntjac.terminal.gwt.server.component_size_validator import \
                ComponentSizeValidator  # FIXME: circular import

            # child tree repaints may be needed, due to our fall back support
            # for invalid relative sizes
            dirtyChildren = None
            childrenMayBecomeUndefined = False
            if (self.getHeight() == self.SIZE_UNDEFINED
                    and height != self.SIZE_UNDEFINED):
                # children currently in invalid state may need repaint
                dirtyChildren = self.getInvalidSizedChildren(True)

            elif ((height == self.SIZE_UNDEFINED
                    and self.getHeight() != self.SIZE_UNDEFINED)
                  or (unit == self.UNITS_PERCENTAGE
                    and self.getHeightUnits() != self.UNITS_PERCENTAGE
                    and not ComponentSizeValidator.parentCanDefineHeight(self))):

                # relative height children may get to invalid state if height
                # becomes invalid. Height may also become invalid if units
                # become percentage due to the fallback support.
                childrenMayBecomeUndefined = True
                dirtyChildren = self.getInvalidSizedChildren(True)

            super(AbstractComponentContainer, self).setHeight(height, unit)

            self.repaintChangedChildTrees(dirtyChildren,
                    childrenMayBecomeUndefined, True)
        else:
            super(AbstractComponentContainer, self).setHeight(height)


    def requestRepaintAll(self):
        self.requestRepaint()

        from muntjac.ui.form import Form  # FIXME: circular import
        from muntjac.ui.table import Table

        for c in self.getComponentIterator():
            if isinstance(c, Form):
                # Form has children in layout, but
                # is not IComponentContainer
                c.requestRepaint()
                c.getLayout().requestRepaintAll()
            elif isinstance(c, Table):
                c.requestRepaintAll()
            elif isinstance(c, IComponentContainer):
                c.requestRepaintAll()
            else:
                c.requestRepaint()
