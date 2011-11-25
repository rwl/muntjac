# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.dd.VHasDropHandler import (VHasDropHandler,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragEvent import (VDragEvent,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
# from com.google.gwt.core.client.Scheduler import (Scheduler,)
# from com.google.gwt.core.client.Scheduler.RepeatingCommand import (RepeatingCommand,)
# from com.google.gwt.dom.client.Element import (Element,)
# from com.google.gwt.dom.client.EventTarget import (EventTarget,)
# from com.google.gwt.dom.client.Node import (Node,)
# from com.google.gwt.dom.client.Style import (Style,)
# from com.google.gwt.dom.client.Style.Display import (Display,)
# from com.google.gwt.event.dom.client.KeyCodes import (KeyCodes,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.Command import (Command,)
# from com.google.gwt.user.client.Event import (Event,)
# from com.google.gwt.user.client.Event.NativePreviewEvent import (NativePreviewEvent,)
# from com.google.gwt.user.client.Event.NativePreviewHandler import (NativePreviewHandler,)
# from com.google.gwt.user.client.Timer import (Timer,)
# from com.google.gwt.user.client.ui.RootPanel import (RootPanel,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)


class VDragAndDropManager(object):
    """Helper class to manage the state of drag and drop event on Vaadin client
    side. Can be used to implement most of the drag and drop operation
    automatically via cross-browser event preview method or just as a helper when
    implementing own low level drag and drop operation (like with HTML5 api).
    <p>
    Singleton. Only one drag and drop operation can be active anyways. Use
    {@link #get()} to get instance.

    TODO cancel drag and drop if more than one touches !?
    """
    ACTIVE_DRAG_SOURCE_STYLENAME = 'v-active-drag-source'

    def DefaultDragAndDropEventHandler(VDragAndDropManager_this, *args, **kwargs):

        class DefaultDragAndDropEventHandler(NativePreviewHandler):

            def onPreviewNativeEvent(self, event):
                nativeEvent = event.getNativeEvent()
                typeInt = event.getTypeInt()
                if typeInt == Event.ONKEYDOWN:
                    keyCode = event.getNativeEvent().getKeyCode()
                    if keyCode == KeyCodes.KEY_ESCAPE:
                        # end drag if ESC is hit
                        VDragAndDropManager_this.interruptDrag()
                        event.cancel()
                        event.getNativeEvent().preventDefault()
                    # no use for handling for any key down event
                    return
                VDragAndDropManager_this._currentDrag.setCurrentGwtEvent(nativeEvent)
                VDragAndDropManager_this.updateDragImagePosition()
                targetElement = Element.as_(nativeEvent.getEventTarget())
                if (
                    Util.isTouchEvent(nativeEvent) or (VDragAndDropManager_this._dragElement is not None and VDragAndDropManager_this._dragElement.isOrHasChild(targetElement))
                ):
                    # to detect the "real" target, hide dragelement temporary and
                    # use elementFromPoint
                    display = VDragAndDropManager_this._dragElement.getStyle().getDisplay()
                    VDragAndDropManager_this._dragElement.getStyle().setDisplay(Display.NONE)
                    try:
                        x = Util.getTouchOrMouseClientX(nativeEvent)
                        y = Util.getTouchOrMouseClientY(nativeEvent)
                        # Util.browserDebugger();
                        targetElement = Util.getElementFromPoint(x, y)
                        if targetElement is None:
                            # ApplicationConnection.getConsole().log(
                            # "Event on dragImage, ignored");
                            event.cancel()
                            nativeEvent.stopPropagation()
                            return
                        else:
                            # ApplicationConnection.getConsole().log(
                            # "Event on dragImage, target changed");
                            # special handling for events over dragImage
                            # pretty much all events are mousemove althout below
                            # kind of happens mouseover
                            _0 = typeInt
                            _1 = False
                            while True:
                                if _0 == Event.ONMOUSEOVER:
                                    _1 = True
                                if (_1 is True) or (_0 == Event.ONMOUSEOUT):
                                    _1 = True
                                    return
                                if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                                    _1 = True
                                if (_1 is True) or (_0 == Event.ONTOUCHMOVE):
                                    _1 = True
                                    findDragTarget = VDragAndDropManager_this.findDragTarget(targetElement)
                                    if findDragTarget != VDragAndDropManager_this._currentDropHandler:
                                        # dragleave on old
                                        if VDragAndDropManager_this._currentDropHandler is not None:
                                            VDragAndDropManager_this._currentDropHandler.dragLeave(VDragAndDropManager_this._currentDrag)
                                            VDragAndDropManager_this._currentDrag.getDropDetails().clear()
                                            VDragAndDropManager_this._serverCallback = None
                                        # dragenter on new
                                        VDragAndDropManager_this._currentDropHandler = findDragTarget
                                        if findDragTarget is not None:
                                            # ApplicationConnection.getConsole().log(
                                            # "DropHandler now"
                                            # + currentDropHandler
                                            # .getPaintable());
                                            pass
                                        if VDragAndDropManager_this._currentDropHandler is not None:
                                            VDragAndDropManager_this._currentDrag.setElementOver(targetElement)
                                            VDragAndDropManager_this._currentDropHandler.dragEnter(VDragAndDropManager_this._currentDrag)
                                    elif findDragTarget is not None:
                                        VDragAndDropManager_this._currentDrag.setElementOver(targetElement)
                                        VDragAndDropManager_this._currentDropHandler.dragOver(VDragAndDropManager_this._currentDrag)
                                    # prevent text selection on IE
                                    nativeEvent.preventDefault()
                                    return
                                if True:
                                    _1 = True
                                    VDragAndDropManager_this._currentDrag.setElementOver(targetElement)
                                    break
                                break
                    except RuntimeError, e:
                        raise e
                    finally:
                        VDragAndDropManager_this._dragElement.getStyle().setProperty('display', display)
                    # ApplicationConnection.getConsole().log(
                    # "ERROR during elementFromPoint hack.");
                _2 = typeInt
                _3 = False
                while True:
                    if _2 == Event.ONMOUSEOVER:
                        _3 = True
                        target = findDragTarget(targetElement)
                        if (
                            target is not None and target != VDragAndDropManager_this._currentDropHandler
                        ):
                            if VDragAndDropManager_this._currentDropHandler is not None:
                                VDragAndDropManager_this._currentDropHandler.dragLeave(VDragAndDropManager_this._currentDrag)
                                VDragAndDropManager_this._currentDrag.getDropDetails().clear()
                            VDragAndDropManager_this._currentDropHandler = target
                            # ApplicationConnection.getConsole().log(
                            # "DropHandler now"
                            # + currentDropHandler.getPaintable());
                            target.dragEnter(VDragAndDropManager_this._currentDrag)
                        elif (
                            target is None and VDragAndDropManager_this._currentDropHandler is not None
                        ):
                            # ApplicationConnection.getConsole().log("Invalid state!?");
                            VDragAndDropManager_this._currentDropHandler.dragLeave(VDragAndDropManager_this._currentDrag)
                            VDragAndDropManager_this._currentDrag.getDropDetails().clear()
                            VDragAndDropManager_this._currentDropHandler = None
                        break
                    if (_3 is True) or (_2 == Event.ONMOUSEOUT):
                        _3 = True
                        relatedTarget = Element.as_(nativeEvent.getRelatedEventTarget())
                        newDragHanler = findDragTarget(relatedTarget)
                        if (
                            VDragAndDropManager_this._dragElement is not None and VDragAndDropManager_this._dragElement.isOrHasChild(relatedTarget)
                        ):
                            # ApplicationConnection.getConsole().log(
                            # "Mouse out of dragImage, ignored");
                            return
                        if (
                            VDragAndDropManager_this._currentDropHandler is not None and VDragAndDropManager_this._currentDropHandler != newDragHanler
                        ):
                            VDragAndDropManager_this._currentDropHandler.dragLeave(VDragAndDropManager_this._currentDrag)
                            VDragAndDropManager_this._currentDrag.getDropDetails().clear()
                            VDragAndDropManager_this._currentDropHandler = None
                            VDragAndDropManager_this._serverCallback = None
                        break
                    if (_3 is True) or (_2 == Event.ONMOUSEMOVE):
                        _3 = True
                    if (_3 is True) or (_2 == Event.ONTOUCHMOVE):
                        _3 = True
                        if VDragAndDropManager_this._currentDropHandler is not None:
                            VDragAndDropManager_this._currentDropHandler.dragOver(VDragAndDropManager_this._currentDrag)
                        nativeEvent.preventDefault()
                        break
                    if (_3 is True) or (_2 == Event.ONTOUCHEND):
                        _3 = True
                        event.getNativeEvent().preventDefault()
                    if (_3 is True) or (_2 == Event.ONMOUSEUP):
                        _3 = True
                        VDragAndDropManager_this.endDrag()
                        break
                    if True:
                        _3 = True
                        break
                    break

        return DefaultDragAndDropEventHandler(*args, **kwargs)

    class DragEventType(object):
        ENTER = 'ENTER'
        LEAVE = 'LEAVE'
        OVER = 'OVER'
        DROP = 'DROP'
        _values = [ENTER, LEAVE, OVER, DROP]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    _DD_SERVICE = 'DD'
    _instance = None
    _handlerRegistration = None
    _currentDrag = None
    # If dragging is currently on a drophandler, this field has reference to it
    _currentDropHandler = None

    def getCurrentDropHandler(self):
        return self._currentDropHandler

    def setCurrentDropHandler(self, currentDropHandler):
        """If drag and drop operation is not handled by {@link VDragAndDropManager}s
        internal handler, this can be used to update current {@link VDropHandler}
        .

        @param currentDropHandler
        """
        self._currentDropHandler = currentDropHandler

    _serverCallback = None
    _deferredStartRegistration = None

    @classmethod
    def get(cls):
        # Singleton
        if cls._instance is None:
            cls._instance = GWT.create(VDragAndDropManager)
        return cls._instance

    def __init__(self):
        pass

    _defaultDragAndDropEventHandler = DefaultDragAndDropEventHandler()
    # Flag to indicate if drag operation has really started or not. Null check
    # of currentDrag field is not enough as a lazy start may be pending.

    _isStarted = None

    def startDrag(self, transferable, startEvent, handleDragEvents):
        """This method is used to start Vaadin client side drag and drop operation.
        Operation may be started by virtually any Widget.
        <p>
        Cancels possible existing drag. TODO figure out if this is always a bug
        if one is active. Maybe a good and cheap lifesaver thought.
        <p>
        If possible, method automatically detects current {@link VDropHandler}
        and fires {@link VDropHandler#dragEnter(VDragEvent)} event on it.
        <p>
        May also be used to control the drag and drop operation. If this option
        is used, {@link VDropHandler} is searched on mouse events and appropriate
        methods on it called automatically.

        @param transferable
        @param nativeEvent
        @param handleDragEvents
                   if true, {@link VDragAndDropManager} handles the drag and drop
                   operation GWT event preview.
        @return
        """
        self.interruptDrag()
        self._isStarted = False
        self._currentDrag = VDragEvent(transferable, startEvent)
        self._currentDrag.setCurrentGwtEvent(startEvent)

        class startDrag(Command):

            def execute(self):
                VDragAndDropManager_this._isStarted = True
                self.addActiveDragSourceStyleName()
                dh = None
                if self.startEvent is not None:
                    dh = VDragAndDropManager_this.findDragTarget(Element.as_(VDragAndDropManager_this._currentDrag.getCurrentGwtEvent().getEventTarget()))
                if dh is not None:
                    # drag has started on a DropHandler, kind of drag over
                    # happens
                    VDragAndDropManager_this._currentDropHandler = dh
                    dh.dragEnter(VDragAndDropManager_this._currentDrag)
                if self.handleDragEvents:
                    VDragAndDropManager_this._handlerRegistration = Event.addNativePreviewHandler(VDragAndDropManager_this._defaultDragAndDropEventHandler)
                    if (
                        VDragAndDropManager_this._dragElement is not None and VDragAndDropManager_this._dragElement.getParentElement() is None
                    ):
                        # deferred attaching drag image is on going, we can
                        # hurry with it now
                        VDragAndDropManager_this.lazyAttachDragElement.cancel()
                        VDragAndDropManager_this.lazyAttachDragElement.run()
                # just capture something to prevent text selection in IE
                Event.setCapture(RootPanel.getBodyElement())

            def addActiveDragSourceStyleName(self):
                dragSource = VDragAndDropManager_this._currentDrag.getTransferable().getDragSource()
                dragSource.addStyleName(VDragAndDropManager_this.ACTIVE_DRAG_SOURCE_STYLENAME)

        eventType = Event.as_(startEvent).getTypeInt()
        if (
            handleDragEvents and (eventType == Event.ONMOUSEDOWN) or (eventType == Event.ONTOUCHSTART)
        ):
            # only really start drag event on mousemove

            class _1_(NativePreviewHandler):

                def onPreviewNativeEvent(self, event):
                    typeInt = event.getTypeInt()
                    _0 = typeInt
                    _1 = False
                    while True:
                        if _0 == Event.ONMOUSEOVER:
                            _1 = True
                            if VDragAndDropManager_this._dragElement is None:
                                break
                            currentEventTarget = event.getNativeEvent().getCurrentEventTarget()
                            if (
                                Node.is_(currentEventTarget) and not VDragAndDropManager_this._dragElement.isOrHasChild(Node.as_(currentEventTarget))
                            ):
                                # drag image appeared below, ignore
                                break
                        if (_1 is True) or (_0 == Event.ONKEYDOWN):
                            _1 = True
                        if (_1 is True) or (_0 == Event.ONKEYPRESS):
                            _1 = True
                        if (_1 is True) or (_0 == Event.ONKEYUP):
                            _1 = True
                        if (_1 is True) or (_0 == Event.ONBLUR):
                            _1 = True
                        if (_1 is True) or (_0 == Event.ONFOCUS):
                            _1 = True
                            break
                        if (_1 is True) or (_0 == Event.ONMOUSEOUT):
                            _1 = True
                            if VDragAndDropManager_this._dragElement is None:
                                break
                            relatedEventTarget = event.getNativeEvent().getRelatedEventTarget()
                            if (
                                Node.is_(relatedEventTarget) and not VDragAndDropManager_this._dragElement.isOrHasChild(Node.as_(relatedEventTarget))
                            ):
                                # drag image appeared below, ignore
                                break
                        if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                            _1 = True
                        if (_1 is True) or (_0 == Event.ONTOUCHMOVE):
                            _1 = True
                            if VDragAndDropManager_this._deferredStartRegistration is not None:
                                VDragAndDropManager_this._deferredStartRegistration.removeHandler()
                                VDragAndDropManager_this._deferredStartRegistration = None
                            VDragAndDropManager_this._currentDrag.setCurrentGwtEvent(event.getNativeEvent())
                            VDragAndDropManager_this.startDrag.execute()
                            break
                        if True:
                            _1 = True
                            if VDragAndDropManager_this._deferredStartRegistration is not None:
                                VDragAndDropManager_this._deferredStartRegistration.removeHandler()
                                VDragAndDropManager_this._deferredStartRegistration = None
                            VDragAndDropManager_this._currentDrag = None
                            VDragAndDropManager_this.clearDragElement()
                            break
                        break

            _1_ = _1_()
            Event.addNativePreviewHandler(_1_)
            self._deferredStartRegistration = _1_
        else:
            startDrag.execute()
        return self._currentDrag

    def updateDragImagePosition(self):
        if (
            self._currentDrag.getCurrentGwtEvent() is not None and self._dragElement is not None
        ):
            style = self._dragElement.getStyle()
            clientY = Util.getTouchOrMouseClientY(self._currentDrag.getCurrentGwtEvent())
            clientX = Util.getTouchOrMouseClientX(self._currentDrag.getCurrentGwtEvent())
            style.setTop(clientY, Unit.PX)
            style.setLeft(clientX, Unit.PX)

    def findDragTarget(self, element):
        """First seeks the widget from this element, then iterates widgets until one
        implement HasDropHandler. Returns DropHandler from that.

        @param element
        @return
        """
        # ApplicationConnection.getConsole().log(
        # "FIXME: Exception when detecting drop handler");
        # e.printStackTrace();
        try:
            w = Util.findWidget(element, None)
            if w is None:
                return None
            while not isinstance(w, VHasDropHandler):
                w = w.getParent()
                if w is None:
                    break
            if w is None:
                return None
            else:
                dh = w.getDropHandler()
                return dh
        except Exception, e:
            return None

    def endDrag(self, *args):
        """Drag is ended (drop happened) on current drop handler. Calls drop method
        on current drop handler and does appropriate cleanup.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.endDrag(True)
        elif _1 == 1:
            doDrop, = _0
            if self._handlerRegistration is not None:
                self._handlerRegistration.removeHandler()
                self._handlerRegistration = None
            sendTransferableToServer = False
            if self._currentDropHandler is not None:
                if doDrop:
                    # we have dropped on a drop target
                    sendTransferableToServer = self._currentDropHandler.drop(self._currentDrag)
                    if sendTransferableToServer:
                        self.doRequest(self.DragEventType.DROP)
                        # Clean active source class name deferred until response is
                        # handled. E.g. hidden on start, removed in drophandler ->
                        # would flicker in case removed eagerly.

                        dragSource = self._currentDrag.getTransferable().getDragSource()
                        client = self._currentDropHandler.getApplicationConnection()

                        class _2_(RepeatingCommand):

                            def execute(self):
                                if not self.client.hasActiveRequest():
                                    VDragAndDropManager_this.removeActiveDragSourceStyleName(self.dragSource)
                                    return False
                                return True

                        _2_ = _2_()
                        Scheduler.get().scheduleFixedDelay(_2_, 30)
                else:
                    self._currentDrag.setCurrentGwtEvent(None)
                    self._currentDropHandler.dragLeave(self._currentDrag)
                self._currentDropHandler = None
                self._serverCallback = None
                self._visitId = 0
                # reset to ignore ongoing server check
            # Remove class name indicating drag source when server visit is done
            # iff server visit was not initiated. Otherwise it will be removed once
            # the server visit is done.

            if not sendTransferableToServer and self._currentDrag is not None:
                self.removeActiveDragSourceStyleName(self._currentDrag.getTransferable().getDragSource())
            self._currentDrag = None
            self.clearDragElement()
            # release the capture (set to prevent text selection in IE)
            Event.releaseCapture(RootPanel.getBodyElement())
        else:
            raise ARGERROR(0, 1)

    def interruptDrag(self):
        """The drag and drop operation is ended, but drop did not happen. If
        operation is currently on a drop handler, its dragLeave method is called
        and appropriate cleanup happens.
        """
        self.endDrag(False)

    def removeActiveDragSourceStyleName(self, dragSource):
        dragSource.removeStyleName(self.ACTIVE_DRAG_SOURCE_STYLENAME)

    def clearDragElement(self):
        if self._dragElement is not None:
            if self._dragElement.getParentElement() is not None:
                RootPanel.getBodyElement().removeChild(self._dragElement)
            self._dragElement = None

    _visitId = 0
    _dragElement = None

    def visitServer(self, acceptCallback):
        """Visits server during drag and drop procedure. Transferable and event type
        is given to server side counterpart of DropHandler.

        If another server visit is started before the current is received, the
        current is just dropped. TODO consider if callback should have
        interrupted() method for cleanup.

        @param acceptCallback
        """
        self.doRequest(self.DragEventType.ENTER)
        self._serverCallback = acceptCallback

    def doRequest(self, drop):
        if self._currentDropHandler is None:
            return
        paintable = self._currentDropHandler.getPaintable()
        client = self._currentDropHandler.getApplicationConnection()
        # For drag events we are using special id that are routed to
        # "drag service" which then again finds the corresponding DropHandler
        # on server side.
        # 
        # TODO add rest of the data in Transferable
        # 
        # TODO implement partial updates to Transferable (currently the whole
        # Transferable is sent on each request)

        self._visitId += 1
        client.updateVariable(self._DD_SERVICE, 'visitId', self._visitId, False)
        client.updateVariable(self._DD_SERVICE, 'eventId', self._currentDrag.getEventId(), False)
        client.updateVariable(self._DD_SERVICE, 'dhowner', paintable, False)
        transferable = self._currentDrag.getTransferable()
        client.updateVariable(self._DD_SERVICE, 'component', transferable.getDragSource(), False)
        client.updateVariable(self._DD_SERVICE, 'type', drop.ordinal(), False)
        if self._currentDrag.getCurrentGwtEvent() is not None:
            # NOP, (at least oophm on Safari) can't serialize html dd event
            # to mouseevent
            try:
                mouseEventDetails = MouseEventDetails(self._currentDrag.getCurrentGwtEvent())
                self._currentDrag.getDropDetails().put('mouseEvent', mouseEventDetails.serialize())
            except Exception, e:
                pass # astStmt: [Stmt([]), None]
        else:
            self._currentDrag.getDropDetails().put('mouseEvent', None)
        client.updateVariable(self._DD_SERVICE, 'evt', self._currentDrag.getDropDetails(), False)
        client.updateVariable(self._DD_SERVICE, 'tra', transferable.getVariableMap(), True)

    def handleServerResponse(self, valueMap):
        if self._serverCallback is None:
            return
        uidl = valueMap
        visitId = uidl.getIntAttribute('visitId')
        if self._visitId == visitId:
            self._serverCallback.handleResponse(uidl.getBooleanAttribute('accepted'), uidl)
            self._serverCallback = None
        self.runDeferredCommands()

    def runDeferredCommands(self):
        if self._deferredCommand is not None:
            command = self._deferredCommand
            self._deferredCommand = None
            command.execute()
            if not self.isBusy():
                self.runDeferredCommands()

    def setDragElement(self, node):
        if self._currentDrag is not None:
            if self._dragElement is not None and self._dragElement != node:
                self.clearDragElement()
            elif node == self._dragElement:
                return
            self._dragElement = node
            self._dragElement.addClassName('v-drag-element')
            self.updateDragImagePosition()
            if self._isStarted:
                self.lazyAttachDragElement.run()
            else:
                # To make our default dnd handler as compatible as possible, we
                # need to defer the appearance of dragElement. Otherwise events
                # that are derived from sequences of other events might not
                # fire as domchanged will fire between them or mouse up might
                # happen on dragElement.

                self.lazyAttachDragElement.schedule(300)

    def getDragElement(self):
        return self._dragElement

    class lazyAttachDragElement(Timer):

        def run(self):
            if (
                VDragAndDropManager_this._dragElement is not None and VDragAndDropManager_this._dragElement.getParentElement() is None
            ):
                RootPanel.getBodyElement().appendChild(VDragAndDropManager_this._dragElement)

    _deferredCommand = None

    def isBusy(self):
        return self._serverCallback is not None

    def defer(self, command):
        """Method to que tasks until all dd related server visits are done

        @param command
        """
        self._deferredCommand = command

    def executeWhenReady(self, command):
        """Method to execute commands when all existing dd related tasks are
        completed (some may require server visit).
        <p>
        Using this method may be handy if criterion that uses lazy initialization
        are used. Check
        <p>
        TODO Optimization: consider if we actually only need to keep the last
        command in queue here.

        @param command
        """
        if self.isBusy():
            self.defer(command)
        else:
            command.execute()
