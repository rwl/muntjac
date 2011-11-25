# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
# from com.google.gwt.dom.client.Document import (Document,)
# from com.google.gwt.dom.client.NativeEvent import (NativeEvent,)
# from com.google.gwt.dom.client.Style.Unit import (Unit,)
# from com.google.gwt.dom.client.TableElement import (TableElement,)
# from com.google.gwt.dom.client.TableSectionElement import (TableSectionElement,)
# from com.google.gwt.event.dom.client.MouseOverEvent import (MouseOverEvent,)
# from com.google.gwt.user.client.Element import (Element,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)


class VDragEvent(object):
    """DragEvent used by Vaadin client side engine. Supports components, items,
    properties and custom payload (HTML5 style).
    """
    _DEFAULT_OFFSET = 10
    _eventId = 0
    _transferable = None
    _currentGwtEvent = None
    _startEvent = None
    _id = None
    _dropDetails = dict()
    _elementOver = None

    def __init__(self, t, startEvent):
        self._transferable = t
        self._startEvent = startEvent
        self._id = POSTINC(globals(), locals(), 'self._eventId')

    def getTransferable(self):
        return self._transferable

    def getCurrentGwtEvent(self):
        """Returns the the latest {@link NativeEvent} that relates to this drag and
        drop operation. For example on {@link VDropHandler#dragEnter(VDragEvent)}
        this is commonly a {@link MouseOverEvent}.

        @return
        """
        return self._currentGwtEvent

    def setCurrentGwtEvent(self, event):
        self._currentGwtEvent = event

    def getEventId(self):
        return self._id

    def getElementOver(self):
        """Detecting the element on which the the event is happening may be
        problematic during drag and drop operation. This is especially the case
        if a drag image (often called also drag proxy) is kept under the mouse
        cursor (see {@link #createDragImage(Element, boolean)}. Drag and drop
        event handlers (like the one provided by {@link VDragAndDropManager} )
        should set elmentOver field to reflect the the actual element on which
        the pointer currently is (drag image excluded). {@link VDropHandler}s can
        then more easily react properly on drag events by reading the element via
        this method.

        @return the element in {@link VDropHandler} on which mouse cursor is on
        """
        if self._elementOver is not None:
            return self._elementOver
        elif self._currentGwtEvent is not None:
            return self._currentGwtEvent.getEventTarget()
        return None

    def setElementOver(self, targetElement):
        self._elementOver = targetElement

    def setDragImage(self, *args):
        """Sets the drag image used for current drag and drop operation. Drag image
        is displayed next to mouse cursor during drag and drop.
        <p>
        The element to be used as drag image will automatically get CSS style
        name "v-drag-element".

        TODO decide if this method should be here or in {@link VTransferable} (in
        HTML5 it is in DataTransfer) or {@link VDragAndDropManager}

        TODO should be possible to override behavior. Like to proxy the element
        to HTML5 DataTransfer

        @param node
        ---
        Sets the drag image used for current drag and drop operation. Drag image
        is displayed next to mouse cursor during drag and drop.
        <p>
        The element to be used as drag image will automatically get CSS style
        name "v-drag-element".

        @param element
                   the dom element to be positioned next to mouse cursor
        @param offsetX
                   the horizontal offset of drag image from mouse cursor
        @param offsetY
                   the vertical offset of drag image from mouse cursor
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            node, = _0
            self.setDragImage(node, self._DEFAULT_OFFSET, self._DEFAULT_OFFSET)
        elif _1 == 3:
            element, offsetX, offsetY = _0
            element.getStyle().setMarginLeft(offsetX, Unit.PX)
            element.getStyle().setMarginTop(offsetY, Unit.PX)
            VDragAndDropManager.get().setDragElement(element)
        else:
            raise ARGERROR(1, 3)

    def getDropDetails(self):
        """TODO consider using similar smaller (than map) api as in Transferable

        TODO clean up when drop handler changes

        @return
        """
        return self._dropDetails

    def getDragImage(self):
        """@return the current Element used as a drag image (aka drag proxy) or null
                if drag image is not currently set for this drag operation.
        """
        return VDragAndDropManager.get().getDragElement()

    def createDragImage(self, element, alignImageToEvent):
        """Automatically tries to create a proxy image from given element.

        @param element
        @param alignImageToEvent
                   if true, proxy image is aligned to start event, else next to
                   mouse cursor
        """
        cloneNode = element.cloneNode(True)
        if BrowserInfo.get().isIE():
            if cloneNode.getTagName().toLowerCase() == 'tr':
                table = Document.get().createTableElement()
                tbody = Document.get().createTBodyElement()
                table.appendChild(tbody)
                tbody.appendChild(cloneNode)
                cloneNode = table
        if alignImageToEvent:
            absoluteTop = element.getAbsoluteTop()
            absoluteLeft = element.getAbsoluteLeft()
            clientX = Util.getTouchOrMouseClientX(self._startEvent)
            clientY = Util.getTouchOrMouseClientY(self._startEvent)
            offsetX = absoluteLeft - clientX
            offsetY = absoluteTop - clientY
            self.setDragImage(cloneNode, offsetX, offsetY)
        else:
            self.setDragImage(cloneNode)
