# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
# from com.google.gwt.event.dom.client.BlurHandler import (BlurHandler,)
# from com.google.gwt.event.dom.client.FocusHandler import (FocusHandler,)
# from com.google.gwt.event.dom.client.HasBlurHandlers import (HasBlurHandlers,)
# from com.google.gwt.event.dom.client.HasFocusHandlers import (HasFocusHandlers,)
BLUR = EventId.BLUR
FOCUS = EventId.FOCUS


class EventHelper(object):
    """Helper class for attaching/detaching handlers for Vaadin client side
    components, based on identifiers in UIDL. Helpers expect Paintables to be
    both listeners and sources for events. This helper cannot be used for more
    complex widgets.
    <p>
    Possible current registration is given as parameter. The returned
    registration (possibly the same as given, should be store for next update.
    <p>
    Pseudocode what helpers do:

    <pre>

    if paintable has event listener in UIDL
         if registration is null
                 register paintable as as handler for event
         return the registration
    else
         if registration is not null
                 remove the handler from paintable
         return null


    </pre>
    """

    @classmethod
    def updateFocusHandler(cls, paintable, client, handlerRegistration):
        if client.hasEventListeners(paintable, FOCUS):
            if handlerRegistration is None:
                handlerRegistration = paintable.addFocusHandler(paintable)
            return handlerRegistration
        elif handlerRegistration is not None:
            handlerRegistration.removeHandler()
            handlerRegistration = None
        return None

    @classmethod
    def updateBlurHandler(cls, paintable, client, handlerRegistration):
        if client.hasEventListeners(paintable, BLUR):
            if handlerRegistration is None:
                handlerRegistration = paintable.addBlurHandler(paintable)
            return handlerRegistration
        elif handlerRegistration is not None:
            handlerRegistration.removeHandler()
            handlerRegistration = None
        return None
