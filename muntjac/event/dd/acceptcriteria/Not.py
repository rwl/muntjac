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

from com.vaadin.event.dd.acceptcriteria.ClientSideCriterion import (ClientSideCriterion,)


class Not(ClientSideCriterion):
    """Criterion that wraps another criterion and inverts its return value.

    @since 6.3
    """
    _serialVersionUID = 1131422338558613244L
    _acceptCriterion = None

    def __init__(self, acceptCriterion):
        self._acceptCriterion = acceptCriterion

    def paintContent(self, target):
        super(Not, self).paintContent(target)
        self._acceptCriterion.paint(target)

    def accept(self, dragEvent):
        return not self._acceptCriterion.accept(dragEvent)
