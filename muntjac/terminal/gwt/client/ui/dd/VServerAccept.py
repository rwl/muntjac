# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragEventServerCallback import (VDragEventServerCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VServerAccept(VAcceptCriterion):

    def accept(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            drag, configuration = _0
            return False
            # not used
        elif _1 == 3:
            drag, configuration, callback = _0

            class acceptCallback(VDragEventServerCallback):

                def handleResponse(self, accepted, response):
                    if accepted:
                        self.callback.accepted(self.drag)

            VDragAndDropManager.get().visitServer(acceptCallback)
        else:
            raise ARGERROR(2, 3)

    def needsServerSideCheck(self, drag, criterioUIDL):
        return True
