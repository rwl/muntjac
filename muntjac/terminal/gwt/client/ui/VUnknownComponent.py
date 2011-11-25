# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.VUIDLBrowser import (VUIDLBrowser,)
# from com.google.gwt.user.client.ui.Composite import (Composite,)
# from com.google.gwt.user.client.ui.VerticalPanel import (VerticalPanel,)
import pyjamas.ui.Label
import pyjamas.ui.Label


class VUnknownComponent(Composite, Paintable):
    _caption = pyjamas.ui.Label.Label()
    _uidlTree = None
    _panel = None
    _serverClassName = 'unkwnown'

    def __init__(self):
        self._panel = VerticalPanel()
        self._panel.add(self._caption)
        self.initWidget(self._panel)
        self.setStyleName('vaadin-unknown')
        self._caption.setStyleName('vaadin-unknown-caption')

    def setServerSideClassName(self, serverClassName):
        self._serverClassName = serverClassName

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, False):
            return
        self.setCaption('Widgetset does not contain implementation for ' + self._serverClassName + '. Check its @ClientWidget mapping, widgetsets ' + 'GWT module description file and re-compile your' + ' widgetset. In case you have downloaded a vaadin' + ' add-on package, you might want to refer to ' + '<a href=\'http://vaadin.com/using-addons\'>add-on ' + 'instructions</a>. Unrendered UIDL:')
        if self._uidlTree is not None:
            self._uidlTree.removeFromParent()
        self._uidlTree = VUIDLBrowser(uidl, client.getConfiguration())
        self._uidlTree.open(True)
        self._uidlTree.setText('Unrendered UIDL')
        self._panel.add(self._uidlTree)

    def setCaption(self, c):
        self._caption.getElement().setInnerHTML(c)
