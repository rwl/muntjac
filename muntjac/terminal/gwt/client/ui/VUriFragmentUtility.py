# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.event.logical.shared.ValueChangeEvent import (ValueChangeEvent,)
# from com.google.gwt.event.logical.shared.ValueChangeHandler import (ValueChangeHandler,)
# from com.google.gwt.user.client.History import (History,)


class VUriFragmentUtility(Widget, Paintable, ValueChangeHandler):
    """Client side implementation for UriFragmentUtility. Uses GWT's History object
    as an implementation.
    """
    _fragment = None
    _client = None
    _paintableId = None
    _immediate = None
    _historyValueHandlerRegistration = None

    def __init__(self):
        self.setElement(Document.get().createDivElement())
        if BrowserInfo.get().isIE6():
            self.getElement().getStyle().setProperty('overflow', 'hidden')
            self.getElement().getStyle().setProperty('height', '0')

    def onAttach(self):
        super(VUriFragmentUtility, self).onAttach()
        self._historyValueHandlerRegistration = History.addValueChangeHandler(self)
        History.fireCurrentHistoryState()

    def onDetach(self):
        super(VUriFragmentUtility, self).onDetach()
        self._historyValueHandlerRegistration.removeHandler()

    def updateFromUIDL(self, uidl, client):
        if client.updateComponent(self, uidl, False):
            return
        uidlFragment = uidl.getStringVariable('fragment')
        self._immediate = uidl.getBooleanAttribute('immediate')
        if self._client is None:
            # initial paint has some special logic
            self._client = client
            self._paintableId = uidl.getId()
            if not (self._fragment == uidlFragment):
                # initial server side fragment (from link/bookmark/typed) does
                # not equal the one on
                # server, send initial fragment to server
                History.fireCurrentHistoryState()
        elif uidlFragment is not None and not (uidlFragment == self._fragment):
            self._fragment = uidlFragment
            # normal fragment change from server, add new history item
            History.newItem(uidlFragment, False)

    def onValueChange(self, event):
        historyToken = event.getValue()
        self._fragment = historyToken
        if self._client is not None:
            self._client.updateVariable(self._paintableId, 'fragment', self._fragment, self._immediate)
