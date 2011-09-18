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
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)


class VAcceptCriterion(object):

    def accept(self, *args):
        """Checks if current drag event has valid drop target and target accepts the
        transferable. If drop target is valid, callback is used.

        @param drag
        @param configuration
        @param callback
        """
        _0 = args
        _1 = len(args)
        if _1 == 2:
            drag, configuration = _0
        elif _1 == 3:
            drag, configuration, callback = _0
            if self.needsServerSideCheck(drag, configuration):

                class acceptCallback(VDragEventServerCallback):

                    def handleResponse(self, accepted, response):
                        if accepted:
                            self.callback.accepted(self.drag)

                VDragAndDropManager.get().visitServer(self.acceptCallback)
            else:
                validates = self.accept(drag, configuration)
                if validates:
                    callback.accepted(drag)
        else:
            raise ARGERROR(2, 3)

    def needsServerSideCheck(self, drag, criterioUIDL):
        return False
