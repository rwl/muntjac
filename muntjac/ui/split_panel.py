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

"""Defines a component container, that can contain two components which are
split by divider element."""

from muntjac.ui.abstract_split_panel import AbstractSplitPanel


class SplitPanel(AbstractSplitPanel):
    """SplitPanel.

    C{SplitPanel} is a component container, that can contain two
    components (possibly containers) which are split by divider element.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    @deprecated: Use L{HorizontalSplitPanel} or L{VerticalSplitPanel} instead.
    """

    CLIENT_WIDGET = None #ClientWidget(VSplitPanelHorizontal, LoadStyle.EAGER)

    #: Components are to be laid out vertically.
    ORIENTATION_VERTICAL = 0

    #: Components are to be laid out horizontally.
    ORIENTATION_HORIZONTAL = 1


    def __init__(self, orientation=None):
        """Creates a new split panel. The orientation of the panels is
        C{ORIENTATION_VERTICAL} by default.

        @param orientation:
                   the orientation of the layout.
        """
        super(SplitPanel, self).__init__()

        # Orientation of the layout.
        if orientation is None:
            self._orientation = self.ORIENTATION_VERTICAL
        else:
            self.setOrientation(orientation)

        self.setSizeFull()


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        super(SplitPanel, self).paintContent(target)
        if self._orientation == self.ORIENTATION_VERTICAL:
            target.addAttribute('vertical', True)


    def getOrientation(self):
        """Gets the orientation of the split panel.

        @return: the Value of property orientation.
        """
        return self._orientation


    def setOrientation(self, orientation):
        """Sets the orientation of the split panel.

        @param orientation:
                   the New value of property orientation.
        """
        # Checks the validity of the argument
        if (orientation < self.ORIENTATION_VERTICAL
                or orientation > self.ORIENTATION_HORIZONTAL):
            raise ValueError

        self._orientation = orientation
        self.requestRepaint()
