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

from muntjac.ui.abstract_layout \
    import AbstractLayout

from muntjac.ui.alignment \
    import Alignment

from muntjac.event.layout_events \
    import ILayoutClickNotifier, LayoutClickEvent, ILayoutClickListener

from muntjac.terminal.gwt.client.event_id \
    import EventId


class Direction(object):
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'


class WeeLayout(AbstractLayout, ILayoutClickNotifier):
    """Server side component for the VWeeLayout widget."""

    CLIENT_WIDGET = None #ClientWidget(VWeeLayout)

    TYPE_MAPPING = 'org.vaadin.weelayout.WeeLayout'

    _CLICK_EVENT = EventId.LAYOUT_CLICK

    def __init__(self, direction):
        """Create a new layout. The direction of the child components must be
        specified. The direction can only be set once.

        @param direction:
                   The direction in which the child components will flow, either
                   L{Direction}.VERTICAL or L{Direction} .HORIZONTAL
        """
        self._direction = direction

        # Custom layout slots containing the components.
        self.components = list()

        # Mapping from components to alignments (horizontal + vertical).
        self._componentToAlignment = dict()

        # Should the layout clip any overflowing components outside the layout
        # dimensions.
        self._clip = False

        self._smartRelatives = None

        super(WeeLayout, self).__init__()


    def addComponent(self, *args):
        """Add a component into this container. The component is added after the
        previous component or into indexed position in this container.

        @param args:
                tuple of the form:
                  - (c)
                    - the component to be added.
                  - (c, alignment)
                    - the component to be added.
                    - the alignment for the component.
                  - (c, width, height, alignment)
                    - the component to be added.
                    - set the width of the component. Use <code>null</code>
                      to leave untouched.
                    - set the height of the component. Use <code>null</code>
                      to leave untouched.
                    - the alignment for the component.
                  - (c, index)
                    - the component to be added.
                    - the Index of the component position. The components
                      currently in and after the position are shifted forwards.
                  - (c, index, alignment)
                    - the component to be added.
                    - the Index of the component position. The components
                      currently in and after the position are shifted forwards.
                    - the alignment for the component.
        """
        nargs = len(args)
        if nargs == 1:
            c, = args
            self.components.append(c)
            try:
                super(WeeLayout, self).addComponent(c)
                self.requestRepaint()
            except ValueError, e:
                self.components.remove(c)
                raise e
        elif nargs == 2:
            if isinstance(args[1], Alignment):
                c, alignment = args
                self.addComponent(c)
                if alignment is not None:
                    self.setComponentAlignment(c, alignment)
            else:
                c, index = args
                self.components.append(index, c)
                try:
                    super(WeeLayout, self).addComponent(c)
                    self.requestRepaint()
                except ValueError, e:
                    self.components.remove(c)
                    raise e
        elif nargs == 3:
            c, index, alignment = args
            self.components.append(index, c)
            try:
                super(WeeLayout, self).addComponent(c)
                self.setComponentAlignment(c, alignment)
                self.requestRepaint()
            except ValueError, e:
                self.components.remove(c)
                self._componentToAlignment.remove(c)
                raise e
        elif nargs == 4:
            c, width, height, alignment = args
            self.addComponent(c)
            if width is not None:
                c.setWidth(width)
            if height is not None:
                c.setHeight(height)
            if alignment is not None:
                self.setComponentAlignment(c, alignment)
        else:
            raise ValueError


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c:
                   the component to be removed.
        """
        self.components.remove(c)
        self._componentToAlignment.remove(c)
        super(WeeLayout, self).removeComponent(c)
        self.requestRepaint()


    def paintContent(self, target):
        super(WeeLayout, self).paintContent(target)

        # Specify direction
        if self._direction == Direction.VERTICAL:
            target.addAttribute('vertical', True)

        # Specify clipping
        if self._clip:
            target.addAttribute('clip', True)

        # Specify smart relative size handling
        if self._smartRelatives:
            target.addAttribute('smart', True)

        # Adds all items in all the locations
        for c in self.components:
            # Paint child component UIDL
            c.paint(target)

        # Add child component alignment info to layout tag
        target.addAttribute('alignments', self._componentToAlignment)


    def getComponentIterator(self):
        return self.components


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
                self.components.append(newLocation, oldComponent)
                self.components.remove(newComponent)
                self._componentToAlignment.remove(newComponent)
                self.components.append(oldLocation, newComponent)
            else:
                self.components.remove(newComponent)
                self.components.append(oldLocation, newComponent)
                self.components.remove(oldComponent)
                self._componentToAlignment.remove(oldComponent)
                self.components.append(newLocation, oldComponent)

            self.requestRepaint()


    def setComponentAlignment(self, childComponent, alignment):
        """Set the alignment of component in this layout. Only one direction
        is affected, depending on the layout direction, i.e. only vertical
        alignment is considered when the direction is horizontal.
        """
        if childComponent in self.components and alignment is not None:
            self._componentToAlignment[childComponent] = alignment
            self.requestRepaint()
        else:
            raise ValueError('Component must be added to layout before using setComponentAlignment()')


    def getComponentAlignment(self, childComponent):
        alignment = self._componentToAlignment.get(childComponent)
        if alignment is None:
            return Alignment.TOP_LEFT
        else:
            return alignment


    def getComponentIndex(self, component):
        """Returns the index of the given component.

        @param component:
                   The component to look up.
        @return: The index of the component or -1 if the component is not
                 a child.
        """
        return self.components.index(component)


    def getComponent(self, index):
        """Returns the component at the given position.

        @param index:
                   The position of the component.
        @return: The component at the given index.
        @raise IndexError:
                    If the index is out of range.
        """
        return self.components[index]


    def size(self):
        """Returns the number of components in the layout.

        @return: Component amount
        """
        return len(self.components)


    def setClipping(self, clip):
        """Set the clipping value for this layout. If clipping is C{True},
        components overflowing outside the layout boundaries will be clipped.
        Otherwise overflowing components are visible.

        @param clip:
                   the new clipping value.
        """
        self._clip = clip
        self.requestRepaint()


    def setSmartRelativeSizes(self, smartRelatives):
        """When the layout size is undefined, relative sizes are calculated as
        zeros. Set this flag to C{True} if you wish for the layout to
        calculate relative sizes inside undefined sized layouts as well (the
        largest component will determine the size).
        """
        self._smartRelatives = smartRelatives


    def addListener(self, listener, iface=None):
        if (isinstance(listener, ILayoutClickListener) and
                (iface is None or issubclass(iface, ILayoutClickListener))):
            self.registerListener(self._CLICK_EVENT, LayoutClickEvent,
                    listener, ILayoutClickListener.clickMethod)

        super(WeeLayout, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType  # set by decorator

        if issubclass(eventType, LayoutClickEvent):
            self.registerCallback(LayoutClickEvent, callback,
                    self._CLICK_EVENT, *args)
        else:
            super(WeeLayout, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        if (isinstance(listener, ILayoutClickListener) and
                (iface is None or issubclass(iface, ILayoutClickListener))):
            self.withdrawListener(self._CLICK_EVENT, LayoutClickEvent,
                    listener)

        super(WeeLayout, self).addListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, LayoutClickEvent):
            self.withdrawCallback(LayoutClickEvent, callback,
                    self._CLICK_EVENT)
        else:
            super(WeeLayout, self).removeCallback(callback, eventType)
