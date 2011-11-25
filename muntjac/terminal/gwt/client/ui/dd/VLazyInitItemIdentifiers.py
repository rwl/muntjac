# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragEventServerCallback import (VDragEventServerCallback,)
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
                        VLazyInitItemIdentifiers_this._hashSet = set()
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
                            VLazyInitItemIdentifiers_this._hashSet.add(stringArrayAttribute[i])
                        VLazyInitItemIdentifiers_this._loaded = True
                        if accepted:
                            self.callback.accepted(self.drag)

                VDragAndDropManager.get().visitServer(acceptCallback)
        else:
            raise ARGERROR(2, 3)

    def needsServerSideCheck(self, drag, criterioUIDL):
        return self._loaded
