# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterion import (VAcceptCriterion,)


class VTargetDetailIs(VAcceptCriterion):

    def accept(self, drag, configuration):
        name = configuration.getStringAttribute('p')
        t = configuration.getStringAttribute('t').intern() if configuration.hasAttribute('t') else 's'
        value = None
        if t == 's':
            value = configuration.getStringAttribute('v')
        elif t == 'b':
            value = configuration.getBooleanAttribute('v')
        if value is not None:
            object = drag.getDropDetails().get(name)
            if isinstance(object, self.Enum):
                return object.name() == value
            else:
                return value == object
        else:
            return False
