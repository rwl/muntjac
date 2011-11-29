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
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriteria import (VAcceptCriteria,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VNot(VAcceptCriterion):
    """TODO implementation could now be simplified/optimized"""
    _b1 = None
    _crit1 = None

    def accept(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            drag, configuration = _0
            return False
            # not used
        elif _1 == 3:
            drag, configuration, callback = _0
            if self._crit1 is None:
                self._crit1 = self.getCriteria(drag, configuration, 0)
                if self._crit1 is None:
                    VConsole.log('Not criteria didn\'t found a child criteria')
                    return
            self._b1 = False

            class accept1cb(VAcceptCallback):

                def accepted(self, event):
                    VNot_this._b1 = True

            self._crit1.accept(drag, configuration.getChildUIDL(0), accept1cb)
            if not self._b1:
                callback.accepted(drag)
        else:
            raise ARGERROR(2, 3)

    def getCriteria(self, drag, configuration, i):
        childUIDL = configuration.getChildUIDL(i)
        return VAcceptCriteria.get(childUIDL.getStringAttribute('name'))

    def needsServerSideCheck(self, drag, criterioUIDL):
        return False
        # TODO enforce on server side
