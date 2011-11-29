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


class VIsOverId(VAcceptCriterion):

    def accept(self, drag, configuration):
        try:
            pid = configuration.getStringAttribute('s')
            paintable = VDragAndDropManager.get().getCurrentDropHandler().getPaintable()
            pid2 = VDragAndDropManager.get().getCurrentDropHandler().getApplicationConnection().getPid(paintable)
            if pid2 == pid:
                searchedId = drag.getDropDetails().get('itemIdOver')
                stringArrayAttribute = configuration.getStringArrayAttribute('keys')
                for string in stringArrayAttribute:
                    if string == searchedId:
                        return True
        except Exception, e:
            pass # astStmt: [Stmt([]), None]
        return False
