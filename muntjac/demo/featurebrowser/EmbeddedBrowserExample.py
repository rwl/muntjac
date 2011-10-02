# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.terminal.ExternalResource import (ExternalResource,)
# from com.vaadin.ui.Embedded import (Embedded,)
# from com.vaadin.ui.Select import (Select,)
# from com.vaadin.ui.Window.Notification import (Notification,)
# from java.net.MalformedURLException import (MalformedURLException,)
# from java.net.URL import (URL,)


class EmbeddedBrowserExample(VerticalLayout, Select.ValueChangeListener):
    """Demonstrates the use of Embedded and "suggesting" Select by creating a simple
    web-browser. Note: does not check for recursion.

    @author IT Mill Ltd.
    @see com.vaadin.ui.Window
    """
    # Default URL to open.
    _DEFAULT_URL = 'http://www.vaadin.com/'
    # The embedded page
    _emb = Embedded()

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__([self._DEFAULT_URL, 'http://www.vaadin.com/learn', 'http://www.vaadin.com/api', 'http://www.vaadin.com/book'])
        elif _1 == 1:
            urls, = _0
            self.setSizeFull()
            # create the address combobox
            select = Select()
            # allow input
            select.setNewItemsAllowed(True)
            # no empty selection
            select.setNullSelectionAllowed(False)
            # no 'go' -button clicking necessary
            select.setImmediate(True)
            # add some pre-configured URLs
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < urls.length):
                    break
                select.addItem(urls[i])
            # add to layout
            self.addComponent(select)
            # add listener and select initial URL
            select.addListener(self)
            select.setValue(urls[0])
            select.setWidth('100%')
            # configure the embedded and add to layout
            self._emb.setType(Embedded.TYPE_BROWSER)
            self._emb.setSizeFull()
            self.addComponent(self._emb)
            # make the embedded as large as possible
            self.setExpandRatio(self._emb, 1)
        else:
            raise ARGERROR(0, 1)

    def valueChange(self, event):
        url = event.getProperty().getValue()
        if url is not None:
            # the selected url has changed, let's go there
            try:
                u = URL(url)
                self._emb.setSource(ExternalResource(url))
            except MalformedURLException, e:
                self.getWindow().showNotification('Invalid address', e.getMessage() + ' (example: http://www.vaadin.com)', Notification.TYPE_WARNING_MESSAGE)
