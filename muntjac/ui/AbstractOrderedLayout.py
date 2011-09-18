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
from com.vaadin.ui.Alignment import (Alignment,)
from com.vaadin.ui.AbstractLayout import (AbstractLayout,)
from com.vaadin.ui.Layout import (AlignmentHandler, Layout, SpacingHandler,)
from com.vaadin.ui.AlignmentUtils import (AlignmentUtils,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.Map import (Map,)


class AbstractOrderedLayout(AbstractLayout, Layout, AlignmentHandler, Layout, SpacingHandler, LayoutClickNotifier):
    _CLICK_EVENT = EventId.LAYOUT_CLICK
    ALIGNMENT_DEFAULT = Alignment.TOP_LEFT
    # Custom layout slots containing the components.
    components = LinkedList()
    # Child component alignments
    # Mapping from components to alignments (horizontal + vertical).
    _componentToAlignment = dict()
    _componentToExpandRatio = dict()
    # Is spacing between contained components enabled. Defaults to false.
    _spacing = False

    def addComponent(self, *args):
        """Add a component into this container. The component is added to the right
        or under the previous component.

        @param c
                   the component to be added.
        ---
        Adds a component into indexed position in this container.

        @param c
                   the component to be added.
        @param index
                   the Index of the component position. The components currently
                   in and after the position are shifted forwards.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            c, = _0
            self.components.add(c)
            try:
                super(AbstractOrderedLayout, self).addComponent(c)
                self.requestRepaint()
            except IllegalArgumentException, e:
                self.components.remove(c)
                raise e
        elif _1 == 2:
            c, index = _0
            self.components.add(index, c)
            try:
                super(AbstractOrderedLayout, self).addComponent(c)
                self.requestRepaint()
            except IllegalArgumentException, e:
                self.components.remove(c)
                raise e
        else:
            raise ARGERROR(1, 2)

    def addComponentAsFirst(self, c):
        """Adds a component into this container. The component is added to the left
        or on top of the other components.

        @param c
                   the component to be added.
        """
        self.components.addFirst(c)
        try:
            super(AbstractOrderedLayout, self).addComponent(c)
            self.requestRepaint()
        except IllegalArgumentException, e:
            self.components.remove(c)
            raise e

    def removeComponent(self, c):
        """Removes the component from this container.

        @param c
                   the component to be removed.
        """
        self.components.remove(c)
        self._componentToAlignment.remove(c)
        self._componentToExpandRatio.remove(c)
        super(AbstractOrderedLayout, self).removeComponent(c)
        self.requestRepaint()

    def getComponentIterator(self):
        """Gets the component container iterator for going trough all the components
        in the container.

        @return the Iterator of the components inside the container.
        """
        return self.components

    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the iterator
        returned by {@link #getComponentIterator()}.

        @return the number of contained components
        """
        return len(self.components)

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the paint operation failed.
        """
        # Documented in superclass
        super(AbstractOrderedLayout, self).paintContent(target)
        # Add spacing attribute (omitted if false)
        if self._spacing:
            target.addAttribute('spacing', self._spacing)
        # Adds all items in all the locations
        for c in self.components:
            # Paint child component UIDL
            c.paint(target)
        # Add child component alignment info to layout tag
        target.addAttribute('alignments', self._componentToAlignment)
        target.addAttribute('expandRatios', self._componentToExpandRatio)

    def replaceComponent(self, oldComponent, newComponent):
        # Gets the locations
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.AlignmentHandler#setComponentAlignment(com
        # .vaadin.ui.Component, int, int)

        oldLocation = -1
        newLocation = -1
        location = 0
        _0 = True
        i = self.components
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            component = i.next()
            if component == oldComponent:
                oldLocation = location
            if component == newComponent:
                newLocation = location
            location += 1
        if oldLocation == -1:
            self.addComponent(newComponent)
        elif newLocation == -1:
            self.removeComponent(oldComponent)
            self.addComponent(newComponent, oldLocation)
        else:
            if oldLocation > newLocation:
                self.components.remove(oldComponent)
                self.components.add(newLocation, oldComponent)
                self.components.remove(newComponent)
                self._componentToAlignment.remove(newComponent)
                self.components.add(oldLocation, newComponent)
            else:
                self.components.remove(newComponent)
                self.components.add(oldLocation, newComponent)
                self.components.remove(oldComponent)
                self._componentToAlignment.remove(oldComponent)
                self.components.add(newLocation, oldComponent)
            self.requestRepaint()

    def setComponentAlignment(self, *args):
        """None
        ---
        Sets the component alignment using a short hand string notation.

        @deprecated Replaced by
                    {@link #setComponentAlignment(Component, Alignment)}

        @param component
                   A child component in this layout
        @param alignment
                   A short hand notation described in {@link AlignmentUtils}
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            if isinstance(_0[1], Alignment):
                childComponent, alignment = _0
                if self.components.contains(childComponent):
                    self._componentToAlignment.put(childComponent, alignment)
                    self.requestRepaint()
                else:
                    raise self.IllegalArgumentException('Component must be added to layout before using setComponentAlignment()')
            else:
                component, alignment = _0
                AlignmentUtils.setComponentAlignment(self, component, alignment)
        elif _1 == 3:
            childComponent, horizontalAlignment, verticalAlignment = _0
            if self.components.contains(childComponent):
                # Alignments are bit masks
                self._componentToAlignment.put(childComponent, Alignment(horizontalAlignment + verticalAlignment))
                self.requestRepaint()
            else:
                raise self.IllegalArgumentException('Component must be added to layout before using setComponentAlignment()')
        else:
            raise ARGERROR(2, 3)

    # (non-Javadoc)
    # 
    # @see com.vaadin.ui.Layout.AlignmentHandler#getComponentAlignment(com
    # .vaadin.ui.Component)

    def getComponentAlignment(self, childComponent):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.SpacingHandler#setSpacing(boolean)

        alignment = self._componentToAlignment[childComponent]
        if alignment is None:
            return self.ALIGNMENT_DEFAULT
        else:
            return alignment

    def setSpacing(self, enabled):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.SpacingHandler#isSpacing()

        self._spacing = enabled
        self.requestRepaint()

    def isSpacingEnabled(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Layout.SpacingHandler#isSpacing()

        return self._spacing

    def isSpacing(self):
        return self._spacing

    def setExpandRatio(self, component, ratio):
        """<p>
        This method is used to control how excess space in layout is distributed
        among components. Excess space may exist if layout is sized and contained
        non relatively sized components don't consume all available space.

        <p>
        Example how to distribute 1:3 (33%) for component1 and 2:3 (67%) for
        component2 :

        <code>
        layout.setExpandRatio(component1, 1);<br>
        layout.setExpandRatio(component2, 2);
        </code>

        <p>
        If no ratios have been set, the excess space is distributed evenly among
        all components.

        <p>
        Note, that width or height (depending on orientation) needs to be defined
        for this method to have any effect.

        @see Sizeable

        @param component
                   the component in this layout which expand ratio is to be set
        @param ratio
        """
        if self.components.contains(component):
            self._componentToExpandRatio.put(component, ratio)
            self.requestRepaint()
        else:
            raise self.IllegalArgumentException('Component must be added to layout before using setExpandRatio()')

    def getExpandRatio(self, component):
        """Returns the expand ratio of given component.

        @param component
                   which expand ratios is requested
        @return expand ratio of given component, 0.0f by default
        """
        ratio = self._componentToExpandRatio[component]
        return 0 if ratio is None else ratio.floatValue()

    def addListener(self, listener):
        self.addListener(self._CLICK_EVENT, self.LayoutClickEvent, listener, self.LayoutClickListener.clickMethod)

    def removeListener(self, listener):
        self.removeListener(self._CLICK_EVENT, self.LayoutClickEvent, listener)

    def getComponentIndex(self, component):
        """Returns the index of the given component.

        @param component
                   The component to look up.
        @return The index of the component or -1 if the component is not a child.
        """
        return self.components.index(component)

    def getComponent(self, index):
        """Returns the component at the given position.

        @param index
                   The position of the component.
        @return The component at the given index.
        @throws IndexOutOfBoundsException
                    If the index is out of range.
        """
        return self.components.get(index)
