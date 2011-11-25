# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.event.dom.client.HasBlurHandlers import (HasBlurHandlers,)
# from com.google.gwt.event.dom.client.HasFocusHandlers import (HasFocusHandlers,)
# from com.google.gwt.event.dom.client.HasKeyDownHandlers import (HasKeyDownHandlers,)
# from com.google.gwt.event.dom.client.HasKeyPressHandlers import (HasKeyPressHandlers,)


class SimpleFocusablePanel(SimplePanel, HasFocusHandlers, HasBlurHandlers, HasKeyDownHandlers, HasKeyPressHandlers, Focusable):
    """Compared to FocusPanel in GWT this panel does not support eg. accesskeys, but
    is simpler by its dom hierarchy nor supports focusing via java api.
    """

    def __init__(self):
        # make focusable, as we don't need access key magic we don't need to
        # use FocusImpl.createFocusable
        self.setTabIndex(0)

    def addFocusHandler(self, handler):
        return self.addDomHandler(handler, FocusEvent.getType())

    def addBlurHandler(self, handler):
        return self.addDomHandler(handler, BlurEvent.getType())

    def addKeyDownHandler(self, handler):
        return self.addDomHandler(handler, KeyDownEvent.getType())

    def addKeyPressHandler(self, handler):
        return self.addDomHandler(handler, KeyPressEvent.getType())

    def addKeyUpHandler(self, handler):
        return self.addDomHandler(handler, KeyUpEvent.getType())

    def setFocus(self, focus):
        if focus:
            FocusImpl.getFocusImplForPanel().focus(self.getElement())
        else:
            FocusImpl.getFocusImplForPanel().blur(self.getElement())

    def focus(self):
        self.setFocus(True)

    def setTabIndex(self, tabIndex):
        self.getElement().setTabIndex(tabIndex)
