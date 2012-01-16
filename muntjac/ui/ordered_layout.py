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

"""Defines a component container, which shows the subcomponents in the order
of their addition in specified orientation."""

from warnings import warn

from muntjac.ui.abstract_ordered_layout import AbstractOrderedLayout


class OrderedLayout(AbstractOrderedLayout):
    """Ordered layout.

    C{OrderedLayout} is a component container, which shows the
    subcomponents in the order of their addition in specified orientation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    @deprecated: Replaced by VerticalLayout/HorizontalLayout. For type checking
                 please not that VerticalLayout/HorizontalLayout do not extend
                 OrderedLayout but AbstractOrderedLayout (which also
                 OrderedLayout extends).
    """

    CLIENT_WIDGET = None #ClientWidget(VOrderedLayout, LoadStyle.EAGER)

    # Components are to be laid out vertically.
    ORIENTATION_VERTICAL = 0

    # Components are to be laid out horizontally.
    ORIENTATION_HORIZONTAL = 1


    def __init__(self, orientation=None):
        """Creates a new ordered layout. The order of the layout defaults to
        C{ORIENTATION_VERTICAL}.

        @param orientation: the Orientation of the layout.
        @deprecated: Use VerticalLayout/HorizontalLayout instead.
        """
        warn('use VerticalLayout/HorizontalLayout instead', DeprecationWarning)

        super(OrderedLayout, self).__init__()

        # Orientation of the layout.
        self._orientation = None

        if orientation is None:
            orientation = self.ORIENTATION_VERTICAL

        self._orientation = orientation
        if orientation == self.ORIENTATION_VERTICAL:
            self.setWidth(100, self.UNITS_PERCENTAGE)


    def getOrientation(self):
        """Gets the orientation of the container.

        @return: the Value of property orientation.
        """
        return self._orientation


    def setOrientation(self, orientation, needsRepaint=True):
        """Sets the orientation of this OrderedLayout. This method should only
        be used before initial paint.

        @param orientation:
                   the New value of property orientation.
        @deprecated: Use VerticalLayout/HorizontalLayout or define orientation
                     in constructor instead
        """
        # Checks the validity of the argument
        if (orientation < self.ORIENTATION_VERTICAL
                or orientation > self.ORIENTATION_HORIZONTAL):
            raise ValueError()

        self._orientation = orientation
        if needsRepaint:
            self.requestRepaint()


    def paintContent(self, target):
        super(OrderedLayout, self).paintContent(target)

        # Adds the orientation attributes (the default is vertical)
        if self._orientation == self.ORIENTATION_HORIZONTAL:
            target.addAttribute('orientation', 'horizontal')
