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
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)
# from java.util.HashSet import (HashSet,)


class VLazyInitItemIdentifiers(VAcceptCriterion):
    _loaded = False
    _hashSet = None
    _lastDragEvent = None

    def accept(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            drag, configuration = _0
            return False
            # not used is this implementation
        elif _1 == 3:
            drag, configuration, callback = _0
            if (self._lastDragEvent is None) or (self._lastDragEvent != drag):
                self._loaded = False
                self._lastDragEvent = drag
            if self._loaded:
                object = drag.getDropDetails().get('itemIdOver')
                if object in self._hashSet:
                    callback.accepted(drag)
            else:

                class acceptCallback(VDragEventServerCallback):

                    def handleResponse(self, accepted, response):
                        self.hashSet = set()
                        stringArrayAttribute = response.getStringArrayAttribute('allowedIds')
                        _0 = True
                        i = 0
                        while True:
                            if _0 is True:
                                _0 = False
                            else:
                                i += 1
                            if not (i < len(stringArrayAttribute)):
                                break
                            self.hashSet.add(stringArrayAttribute[i])
                        self.loaded = True
                        if accepted:
                            self.callback.accepted(self.drag)

                VDragAndDropManager.get().visitServer(self.acceptCallback)
        else:
            raise ARGERROR(2, 3)

    def needsServerSideCheck(self, drag, criterioUIDL):
        return self._loaded
