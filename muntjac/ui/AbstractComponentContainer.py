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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.AbstractComponent import (AbstractComponent,)
from com.vaadin.terminal.gwt.server.ComponentSizeValidator import (ComponentSizeValidator,)
from com.vaadin.ui.ComponentContainer import (ComponentAttachEvent, ComponentAttachListener, ComponentContainer, ComponentDetachEvent, ComponentDetachListener,)
# from java.lang.reflect.Method import (Method,)
# from java.util.Collection import (Collection,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)


class AbstractComponentContainer(AbstractComponent, ComponentContainer):
    """Extension to {@link AbstractComponent} that defines the default
    implementation for the methods in {@link ComponentContainer}. Basic UI
    components that need to contain other components inherit this class to easily
    qualify as a component container.

    @author IT Mill Ltd
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self):
        """Constructs a new component container."""
        super(AbstractComponentContainer, self)()

    def removeAllComponents(self):
        """Removes all components from the container. This should probably be
        re-implemented in extending classes for a more powerful implementation.
        """
        # Moves all components from an another container into this container. Don't
        # add a JavaDoc comment here, we use the default documentation from
        # implemented interface.

        l = LinkedList()
        # Adds all components
        _0 = True
        i = self.getComponentIterator()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            l.add(i.next())
        # Removes all component
        _1 = True
        i = l
        while True:
            if _1 is True:
                _1 = False
            if not i.hasNext():
                break
            self.removeComponent(i.next())

    def moveComponentsFrom(self, source):
        components = LinkedList()
        _0 = True
        i = source.getComponentIterator()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            components.add(i.next())
        _1 = True
        i = components
        while True:
            if _1 is True:
                _1 = False
            if not i.hasNext():
                break
            c = i.next()
            source.removeComponent(c)
            self.addComponent(c)

    def attach(self):
        """Notifies all contained components that the container is attached to a
        window.

        @see com.vaadin.ui.Component#attach()
        """
        super(AbstractComponentContainer, self).attach()
        _0 = True
        i = self.getComponentIterator()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            i.next().attach()

    def detach(self):
        """Notifies all contained components that the container is detached from a
        window.

        @see com.vaadin.ui.Component#detach()
        """
        # Events
        super(AbstractComponentContainer, self).detach()
        _0 = True
        i = self.getComponentIterator()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            i.next().detach()

    _COMPONENT_ATTACHED_METHOD = None
    _COMPONENT_DETACHED_METHOD = None
    # This should never happen
    try:
        _COMPONENT_ATTACHED_METHOD = ComponentAttachListener.getDeclaredMethod('componentAttachedToContainer', [ComponentAttachEvent])
        _COMPONENT_DETACHED_METHOD = ComponentDetachListener.getDeclaredMethod('componentDetachedFromContainer', [ComponentDetachEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in AbstractComponentContainer')
    # documented in interface

    def addListener(self, *args):
        # documented in interface
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], ComponentAttachListener):
                listener, = _0
                self.addListener(ComponentContainer.ComponentAttachEvent, listener, self._COMPONENT_ATTACHED_METHOD)
            else:
                listener, = _0
                self.addListener(ComponentContainer.ComponentDetachEvent, listener, self._COMPONENT_DETACHED_METHOD)
        else:
            raise ARGERROR(1, 1)

    # documented in interface

    def removeListener(self, *args):
        # documented in interface
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], ComponentAttachListener):
                listener, = _0
                self.removeListener(ComponentContainer.ComponentAttachEvent, listener, self._COMPONENT_ATTACHED_METHOD)
            else:
                listener, = _0
                self.removeListener(ComponentContainer.ComponentDetachEvent, listener, self._COMPONENT_DETACHED_METHOD)
        else:
            raise ARGERROR(1, 1)

    def fireComponentAttachEvent(self, component):
        """Fires the component attached event. This should be called by the
        addComponent methods after the component have been added to this
        container.

        @param component
                   the component that has been added to this container.
        """
        self.fireEvent(ComponentAttachEvent(self, component))

    def fireComponentDetachEvent(self, component):
        """Fires the component detached event. This should be called by the
        removeComponent methods after the component have been removed from this
        container.

        @param component
                   the component that has been removed from this container.
        """
        self.fireEvent(ComponentDetachEvent(self, component))

    def addComponent(self, c):
        """This only implements the events and component parent calls. The extending
        classes must implement component list maintenance and call this method
        after component list maintenance.

        @see com.vaadin.ui.ComponentContainer#addComponent(Component)
        """
        if isinstance(c, ComponentContainer):
            # Make sure we're not adding the component inside it's own content
            _0 = True
            parent = self
            while True:
                if _0 is True:
                    _0 = False
                else:
                    parent = parent.getParent()
                if not (parent is not None):
                    break
                if parent == c:
                    raise self.IllegalArgumentException('Component cannot be added inside it\'s own content')
        if c.getParent() is not None:
            # If the component already has a parent, try to remove it
            oldParent = c.getParent()
            oldParent.removeComponent(c)
        c.setParent(self)
        self.fireComponentAttachEvent(c)

    def removeComponent(self, c):
        """This only implements the events and component parent calls. The extending
        classes must implement component list maintenance and call this method
        before component list maintenance.

        @see com.vaadin.ui.ComponentContainer#removeComponent(Component)
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

    def setWidth(self, width, unit):
        # child tree repaints may be needed, due to our fall back support for
        # invalid relative sizes

        dirtyChildren = None
        childrenMayBecomeUndefined = False
        if self.getWidth() == self.SIZE_UNDEFINED and width != self.SIZE_UNDEFINED:
            # children currently in invalid state may need repaint
            dirtyChildren = self.getInvalidSizedChildren(False)
        elif (
            (width == self.SIZE_UNDEFINED and self.getWidth() != self.SIZE_UNDEFINED) or (unit == self.UNITS_PERCENTAGE and self.getWidthUnits() != self.UNITS_PERCENTAGE and not ComponentSizeValidator.parentCanDefineWidth(self))
        ):
            # relative width children may get to invalid state if width becomes
            # invalid. Width may also become invalid if units become percentage
            # due to the fallback support

            childrenMayBecomeUndefined = True
            dirtyChildren = self.getInvalidSizedChildren(False)
        super(AbstractComponentContainer, self).setWidth(width, unit)
        self.repaintChangedChildTrees(dirtyChildren, childrenMayBecomeUndefined, False)

    def repaintChangedChildTrees(self, invalidChildren, childrenMayBecomeUndefined, vertical):
        if childrenMayBecomeUndefined:
            previouslyInvalidComponents = invalidChildren
            invalidChildren = self.getInvalidSizedChildren(vertical)
            if previouslyInvalidComponents is not None and invalidChildren is not None:
                _0 = True
                iterator = invalidChildren
                while True:
                    if _0 is True:
                        _0 = False
                    if not iterator.hasNext():
                        break
                    component = iterator.next()
                    if previouslyInvalidComponents.contains(component):
                        # still invalid don't repaint
                        iterator.remove()
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
        if isinstance(self, Panel):
            p = self
            content = p.getContent()
            valid = ComponentSizeValidator.checkHeights(content) if vertical else ComponentSizeValidator.checkWidths(content)
            if not valid:
                components = set(1)
                components.add(content)
        else:
            _0 = True
            componentIterator = self.getComponentIterator()
            while True:
                if _0 is True:
                    _0 = False
                if not componentIterator.hasNext():
                    break
                component = componentIterator.next()
                valid = ComponentSizeValidator.checkHeights(component) if vertical else ComponentSizeValidator.checkWidths(component)
                if not valid:
                    if components is None:
                        components = set()
                    components.add(component)
        return components

    def repaintChildTrees(self, dirtyChildren):
        for c in dirtyChildren:
            if isinstance(c, ComponentContainer):
                cc = c
                cc.requestRepaintAll()
            else:
                c.requestRepaint()

    def setHeight(self, height, unit):
        # child tree repaints may be needed, due to our fall back support for
        # invalid relative sizes

        dirtyChildren = None
        childrenMayBecomeUndefined = False
        if self.getHeight() == self.SIZE_UNDEFINED and height != self.SIZE_UNDEFINED:
            # children currently in invalid state may need repaint
            dirtyChildren = self.getInvalidSizedChildren(True)
        elif (
            (height == self.SIZE_UNDEFINED and self.getHeight() != self.SIZE_UNDEFINED) or (unit == self.UNITS_PERCENTAGE and self.getHeightUnits() != self.UNITS_PERCENTAGE and not ComponentSizeValidator.parentCanDefineHeight(self))
        ):
            # relative height children may get to invalid state if height
            # becomes invalid. Height may also become invalid if units become
            # percentage due to the fallback support.

            childrenMayBecomeUndefined = True
            dirtyChildren = self.getInvalidSizedChildren(True)
        super(AbstractComponentContainer, self).setHeight(height, unit)
        self.repaintChangedChildTrees(dirtyChildren, childrenMayBecomeUndefined, True)

    def requestRepaintAll(self):
        self.requestRepaint()
        _0 = True
        childIterator = self.getComponentIterator()
        while True:
            if _0 is True:
                _0 = False
            if not childIterator.hasNext():
                break
            c = childIterator.next()
            if isinstance(c, Form):
                # Form has children in layout, but is not ComponentContainer
                c.requestRepaint()
                c.getLayout().requestRepaintAll()
            elif isinstance(c, Table):
                c.requestRepaintAll()
            elif isinstance(c, ComponentContainer):
                c.requestRepaintAll()
            else:
                c.requestRepaint()
