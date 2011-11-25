# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)


class Table(Paintable, HasWidgets):
    SELECT_MODE_NONE = 0
    SELECT_MODE_SINGLE = 1
    SELECT_MODE_MULTI = 2
