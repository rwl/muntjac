# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragEventServerCallback import (VDragEventServerCallback,)
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

                VDragAndDropManager.get().visitServer(acceptCallback)
            else:
                validates = self.accept(drag, configuration)
                if validates:
                    callback.accepted(drag)
        else:
            raise ARGERROR(2, 3)

    def needsServerSideCheck(self, drag, criterioUIDL):
        return False
