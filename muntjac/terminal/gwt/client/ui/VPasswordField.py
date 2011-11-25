# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VTextField import (VTextField,)


class VPasswordField(VTextField):
    """This class represents a password field.

    @author IT Mill Ltd.
    """

    def __init__(self):
        super(VPasswordField, self)(DOM.createInputPassword())
