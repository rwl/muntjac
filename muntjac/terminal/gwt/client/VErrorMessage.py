# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from java.util.Iterator import (Iterator,)


class VErrorMessage(FlowPanel):
    CLASSNAME = 'v-errormessage'

    def __init__(self):
        super(VErrorMessage, self)()
        self.setStyleName(self.CLASSNAME)

    def updateFromUIDL(self, uidl):
        self.clear()
        if uidl.getChildCount() == 0:
            self.add(HTML(' '))
        else:
            _0 = True
            it = uidl.getChildIterator()
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                child = it.next()
                if isinstance(child, str):
                    errorMessage = child
                    self.add(HTML(errorMessage))
                else:
                    # TODO XML type error, check if this can even happen
                    # anymore??
                    try:
                        childError = VErrorMessage()
                        childError.updateFromUIDL(child)
                        self.add(childError)
                    except Exception, e:
                        xml = child
                        self.add(HTML(xml.getXMLAsString()))

    def showAt(self, indicatorElement):
        """Shows this error message next to given element.

        @param indicatorElement
        """
        errorContainer = self.getParent()
        if errorContainer is None:
            errorContainer = VOverlay()
            errorContainer.setWidget(self)
        errorContainer.setPopupPosition(DOM.getAbsoluteLeft(indicatorElement) + (2 * DOM.getElementPropertyInt(indicatorElement, 'offsetHeight')), DOM.getAbsoluteTop(indicatorElement) + (2 * DOM.getElementPropertyInt(indicatorElement, 'offsetHeight')))
        errorContainer.show()

    def hide(self):
        errorContainer = self.getParent()
        if errorContainer is not None:
            errorContainer.hide()
