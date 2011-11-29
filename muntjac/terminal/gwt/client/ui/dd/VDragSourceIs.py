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

from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VDragSourceIs(VAcceptCriterion):
    """TODO Javadoc!

    @since 6.3
    """

    def accept(self, drag, configuration):
        try:
            component = drag.getTransferable().getDragSource()
            c = configuration.getIntAttribute('c')
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < c):
                    break
                requiredPid = configuration.getStringAttribute('component' + i)
                paintable = VDragAndDropManager.get().getCurrentDropHandler().getApplicationConnection().getPaintable(requiredPid)
                if paintable == component:
                    return True
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return False
