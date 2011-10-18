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

from muntjac.ui.alignment import Alignment
from muntjac.ui.abstract_layout import AbstractLayout
from muntjac.ui.layout import IAlignmentHandler, ISpacingHandler
from muntjac.terminal.gwt.client.event_id import EventId

from muntjac.event.layout_events import \
    ILayoutClickNotifier, ILayoutClickListener, LayoutClickEvent
from muntjac.ui.abstract_component_container import AbstractComponentContainer
from muntjac.ui.abstract_component import AbstractComponent


class AbstractOrderedLayout(AbstractLayout, IAlignmentHandler,
            ISpacingHandler, ILayoutClickNotifier):

    _CLICK_EVENT = EventId.LAYOUT_CLICK

    ALIGNMENT_DEFAULT = Alignment.TOP_LEFT

    def __init__(self):
        super(AbstractOrderedLayout, self).__init__()

        # Custom layout slots containing the components.
        self.components = list()

        # Child component alignments
        # Mapping from components to alignments (horizontal + vertical).
        self._componentToAlignment = dict()
        self._componentToExpandRatio = dict()

        # Is spacing between contained components enabled. Defaults to false.
        self._spacing = False


    def addComponent(self, c, index=None):
        """Add a component into this container. The component is added
        to the right or under the previous component.

        @param c
                   the component to be added.
        ---
        Adds a component into indexed position in this container.

        @param c
                   the component to be added.
        @param index
                   the Index of the component position. The components
                   currently in and after the position are shifted
                   forwards.
        """
        if index is None:
            self.components.append(c)
        else:
            self.components.insert(index, c)

        try:
            super(AbstractOrderedLayout, self).addComponent(c)
            self.requestRepaint()
        except ValueError, e:
            if c in self.components:
                self.components.remove(c)
            raise e


    def addComponentAsFirst(self, c):
        """Adds a component into this container. The component is
        added to the left or on top of the other components.

        @param c the component to be added.
        """
        self.components.addFirst(c)
        try:
            super(AbstractOrderedLayout, self).addComponent(c)
            self.requestRepaint()
        except ValueError, e:
            self.components.remove(c)
            raise e


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c the component to be removed.
        """
        self.components.remove(c)
        del self._componentToAlignment[c]
        del self._componentToExpandRatio[c]
        super(AbstractOrderedLayout, self).removeComponent(c)
        self.requestRepaint()


    def getComponentIterator(self):
        """Gets the component container iterator for going through
        all the components in the container.

        @return the Iterator of the components inside the container.
        """
        return iter(self.components)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with
        the iterator returned by {@link #getComponentIterator()}.

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
        oldLocation = -1
        newLocation = -1
        location = 0
        for component in self.components:
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
                self.components.insert(newLocation, oldComponent)
                self.components.remove(newComponent)
                del self._componentToAlignment[newComponent]
                self.components.insert(oldLocation, newComponent)
            else:
                self.components.remove(newComponent)
                self.components.insert(oldLocation, newComponent)
                self.components.remove(oldComponent)
                del self._componentToAlignment[oldComponent]
                self.components.insert(newLocation, oldComponent)

            self.requestRepaint()


    def setComponentAlignment(self, childComponent, alignment,
                verticalAlignment=None):
        """Sets the component alignment using a short hand string notation.

        @deprecated Replaced by
                    {@link #setComponentAlignment(Component, Alignment)}

        @param component
                   A child component in this layout
        @param alignment
                   A short hand notation described in {@link AlignmentUtils}
        """
        if verticalAlignment is not None:
            alignment = Alignment(alignment + verticalAlignment)

        if childComponent in self.components:
            self._componentToAlignment[childComponent] = alignment
            self.requestRepaint()
        else:
            raise ValueError, ('Component must be added to layout '
                    'before using setComponentAlignment()')


    def getComponentAlignment(self, childComponent):
        alignment = self._componentToAlignment.get(childComponent)
        if alignment is None:
            return self.ALIGNMENT_DEFAULT
        else:
            return alignment


    def setSpacing(self, enabled):
        self._spacing = enabled
        self.requestRepaint()


    def isSpacingEnabled(self):
        return self._spacing


    def isSpacing(self):
        return self._spacing


    def setExpandRatio(self, component, ratio):
        """This method is used to control how excess space in layout
        is distributed among components. Excess space may exist if
        layout is sized and contained non relatively sized components
        don't consume all available space.

        Example how to distribute 1:3 (33%) for component1 and
        2:3 (67%) for component2 :

        <code>
        layout.setExpandRatio(component1, 1);<br>
        layout.setExpandRatio(component2, 2);
        </code>

        If no ratios have been set, the excess space is distributed
        evenly among all components.

        Note, that width or height (depending on orientation) needs
        to be defined for this method to have any effect.

        @see Sizeable

        @param component
                   the component in this layout which expand ratio
                   is to be set
        @param ratio
        """
        if component in self.components:
            self._componentToExpandRatio[component] = ratio
            self.requestRepaint()
        else:
            raise ValueError, ('Component must be added to layout '
                    'before using setExpandRatio()')


    def getExpandRatio(self, component):
        """Returns the expand ratio of given component.

        @param component
                   which expand ratios is requested
        @return expand ratio of given component, 0.0f by default
        """
        ratio = self._componentToExpandRatio.get(component)
        return 0 if ratio is None else float(ratio)


    def addListener(self, listener):
        AbstractComponent.addListener(self, self._CLICK_EVENT,
                LayoutClickEvent, listener, ILayoutClickListener.clickMethod)


    def removeListener(self, listener):
        AbstractComponent.removeListener(self, self._CLICK_EVENT,
                LayoutClickEvent, listener)


    def getComponentIndex(self, component):
        """Returns the index of the given component.

        @param component
                   The component to look up.
        @return The index of the component or -1 if the component
                is not a child.
        """
        return self.components.index(component)


    def getComponent(self, index):
        """Returns the component at the given position.

        @param index
                   The position of the component.
        @return The component at the given index.
        @raise IndexError:
                    If the index is out of range.
        """
        return self.components[index]
