# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
