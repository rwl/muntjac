# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.ClickEventHandler import (ClickEventHandler,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)


class LayoutClickEventHandler(ClickEventHandler):

    def __init__(self, paintable, clickEventIdentifier):
        super(LayoutClickEventHandler, self)(paintable, clickEventIdentifier)

    def getChildComponent(self, element):
        pass

    def fireClick(self, event):
        client = self.getApplicationConnection()
        pid = self.getApplicationConnection().getPid(self.paintable)
        mouseDetails = MouseEventDetails(event, self.getRelativeToElement())
        childComponent = self.getChildComponent(event.getEventTarget())
        parameters = dict()
        parameters.put('mouseDetails', mouseDetails.serialize())
        parameters.put('component', childComponent)
        client.updateVariable(pid, self.clickEventIdentifier, parameters, True)
