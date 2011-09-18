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
from com.vaadin.ui.AbstractSplitPanel import (AbstractSplitPanel,)


class SplitPanel(AbstractSplitPanel):
    """SplitPanel.

    <code>SplitPanel</code> is a component container, that can contain two
    components (possibly containers) which are split by divider element.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.0
    @deprecated in 6.5. Use {@link HorizontalSplitPanel} or
                {@link VerticalSplitPanel} instead.
    """
    # Predefined orientations
    # Components are to be laid out vertically.
    ORIENTATION_VERTICAL = 0
    # Components are to be laid out horizontally.
    ORIENTATION_HORIZONTAL = 1
    # Orientation of the layout.
    _orientation = None

    def __init__(self, *args):
        """Creates a new split panel. The orientation of the panels is
        <code>ORIENTATION_VERTICAL</code>.
        ---
        Create a new split panels. The orientation of the panel is given as
        parameters.

        @param orientation
                   the Orientation of the layout.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(SplitPanel, self)()
            self._orientation = self.ORIENTATION_VERTICAL
            self.setSizeFull()
        elif _1 == 1:
            orientation, = _0
            self.__init__()
            self.setOrientation(orientation)
        else:
            raise ARGERROR(0, 1)

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the paint operation failed.
        """
        super(SplitPanel, self).paintContent(target)
        if self._orientation == self.ORIENTATION_VERTICAL:
            target.addAttribute('vertical', True)

    def getOrientation(self):
        """Gets the orientation of the split panel.

        @return the Value of property orientation.
        """
        return self._orientation

    def setOrientation(self, orientation):
        """Sets the orientation of the split panel.

        @param orientation
                   the New value of property orientation.
        """
        # Checks the validity of the argument
        if (
            (orientation < self.ORIENTATION_VERTICAL) or (orientation > self.ORIENTATION_HORIZONTAL)
        ):
            raise self.IllegalArgumentException()
        self._orientation = orientation
        self.requestRepaint()
