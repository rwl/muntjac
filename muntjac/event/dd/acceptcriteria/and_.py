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

"""A compound criterion that accepts the drag if all of its criteria
accepts the drag."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class And(ClientSideCriterion):
    """A compound criterion that accepts the drag if all of its criteria
    accepts the drag.

    @see: L{Or}
    """

    def __init__(self, *criteria):
        """@param criteria:
                   criteria of which the And criterion will be composed
        """
        self.criteria = criteria


    def paintContent(self, target):
        super(And, self).paintContent(target)
        for crit in self.criteria:
            crit.paint(target)


    def accept(self, dragEvent):
        for crit in self.criteria:
            if not crit.accept(dragEvent):
                return False
        return True


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.And'
