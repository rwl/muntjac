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

from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriteria import (VAcceptCriteria,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VAnd(VAcceptCriterion, VAcceptCallback):
    _b1 = None

    @classmethod
    def getCriteria(cls, drag, configuration, i):
        childUIDL = configuration.getChildUIDL(i)
        return VAcceptCriteria.get(childUIDL.getStringAttribute('name'))

    def accept(self, drag, configuration):
        childCount = configuration.getChildCount()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < childCount):
                break
            crit = self.getCriteria(drag, configuration, i)
            self._b1 = False
            crit.accept(drag, configuration.getChildUIDL(i), self)
            if not self._b1:
                return False
        return True

    def accepted(self, event):
        self._b1 = True
