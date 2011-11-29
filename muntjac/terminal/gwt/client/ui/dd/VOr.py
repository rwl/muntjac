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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VAnd import (VAnd,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VOr(VAcceptCriterion, VAcceptCallback):
    _accepted = None

    def accept(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            drag, configuration = _0
            return False
            # not used here
        elif _1 == 3:
            drag, configuration, callback = _0
            childCount = configuration.getChildCount()
            self._accepted = False
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < childCount):
                    break
                crit = VAnd.getCriteria(drag, configuration, i)
                crit.accept(drag, configuration.getChildUIDL(i), self)
                if self._accepted == True:
                    callback.accepted(drag)
                    return
        else:
            raise ARGERROR(2, 3)

    def needsServerSideCheck(self, drag, criterioUIDL):
        return False

    def accepted(self, event):
        self._accepted = True
