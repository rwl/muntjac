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

"""Defines a layout that will give one of it's components as much space as
possible, while still showing the other components in the layout."""

from warnings import warn

from muntjac.ui.ordered_layout import OrderedLayout


class ExpandLayout(OrderedLayout):
    """A layout that will give one of it's components as much space as
    possible, while still showing the other components in the layout. The
    other components will in effect be given a fixed sized space, while the
    space given to the expanded component will grow/shrink to fill the rest
    of the space available - for instance when re-sizing the window.

    Note that this layout is 100% in both directions by default
    (L{setSizeFull}). Remember to set the units if you want to
    specify a fixed size. If the layout fails to show up, check that the
    parent layout is actually giving some space.

    @deprecated: Deprecated in favor of the new OrderedLayout
    """

    def __init__(self, orientation=None):
        warn('use OrderedLayout', DeprecationWarning)

        self._expanded = None

        if orientation is None:
            self.ORIENTATION_VERTICAL

        super(ExpandLayout, self).__init__(orientation)
        self.setSizeFull()


    def expand(self, c):
        """@param c: Component which container will be maximized
        """
        if self._expanded is not None:
            try:
                self.setExpandRatio(self._expanded, 0.0)
            except ValueError:
                pass  # Ignore error if component has been removed

        self._expanded = c
        if self._expanded is not None:
            self.setExpandRatio(self._expanded, 1.0)

        self.requestRepaint()


    def addComponent(self, c, index=None):
        if index is None:
            super(ExpandLayout, self).addComponent(c)
        else:
            super(ExpandLayout, self).addComponent(c, index)
        if self._expanded is None:
            self.expand(c)


    def addComponentAsFirst(self, c):
        super(ExpandLayout, self).addComponentAsFirst(c)
        if self._expanded is None:
            self.expand(c)


    def removeComponent(self, c):
        super(ExpandLayout, self).removeComponent(c)
        if c == self._expanded:
            try:
                self.expand(self.getComponentIterator().next())
            except StopIteration:
                self.expand(None)


    def replaceComponent(self, oldComponent, newComponent):
        super(ExpandLayout, self).replaceComponent(oldComponent, newComponent)
        if oldComponent == self._expanded:
            self.expand(newComponent)
