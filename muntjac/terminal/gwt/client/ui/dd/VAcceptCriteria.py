# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCriterionFactory import (VAcceptCriterionFactory,)
# from com.google.gwt.core.client.GWT import (GWT,)


class VAcceptCriteria(object):
    """A class via all AcceptCriteria instances are fetched by an identifier."""
    _impl = None
    _impl = GWT.create(VAcceptCriterionFactory)

    @classmethod
    def get(cls, name):
        return cls._impl.get(name)
