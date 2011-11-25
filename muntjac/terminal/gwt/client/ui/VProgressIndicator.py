# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.Util import (Util,)


class VProgressIndicator(Widget, Paintable):
    _CLASSNAME = 'v-progressindicator'
    _wrapper = DOM.createDiv()
    _indicator = DOM.createDiv()
    _client = None
    _poller = None
    _indeterminate = False
    _pollerSuspendedDueDetach = None
    _interval = None

    def __init__(self):
        self.setElement(DOM.createDiv())
        self.getElement().appendChild(self._wrapper)
        self.setStyleName(self._CLASSNAME)
        self._wrapper.appendChild(self._indicator)
        self._indicator.setClassName(self._CLASSNAME + '-indicator')
        self._wrapper.setClassName(self._CLASSNAME + '-wrapper')
        self._poller = self.Poller()

    def updateFromUIDL(self, uidl, client):
        self._client = client
        if not uidl.getBooleanAttribute('cached'):
            self._poller.cancel()
        if client.updateComponent(self, uidl, True):
            return
        self._indeterminate = uidl.getBooleanAttribute('indeterminate')
        if self._indeterminate:
            basename = self._CLASSNAME + '-indeterminate'
            VProgressIndicator.setStyleName(self.getElement(), basename, True)
            VProgressIndicator.setStyleName(self.getElement(), basename + '-disabled', uidl.getBooleanAttribute('disabled'))
        else:
            try:
                f = self.float(uidl.getStringAttribute('state'))
                size = self.Math.round(100 * f)
                DOM.setStyleAttribute(self._indicator, 'width', size + '%')
            except Exception, e:
                pass # astStmt: [Stmt([]), None]
        if not uidl.getBooleanAttribute('disabled'):
            self._interval = uidl.getIntAttribute('pollinginterval')
            self._poller.scheduleRepeating(self._interval)

    def onAttach(self):
        super(VProgressIndicator, self).onAttach()
        if self._pollerSuspendedDueDetach:
            self._poller.scheduleRepeating(self._interval)

    def onDetach(self):
        super(VProgressIndicator, self).onDetach()
        if self._interval > 0:
            self._poller.cancel()
            self._pollerSuspendedDueDetach = True

    def setVisible(self, visible):
        super(VProgressIndicator, self).setVisible(visible)
        if not visible:
            self._poller.cancel()

    def Poller(VProgressIndicator_this, *args, **kwargs):

        class Poller(Timer):

            def run(self):
                if (
                    not VProgressIndicator_this._client.hasActiveRequest() and Util.isAttachedAndDisplayed(VProgressIndicator_this)
                ):
                    VProgressIndicator_this._client.sendPendingVariableChanges()

        return Poller(*args, **kwargs)
