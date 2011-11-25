# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (POSTINC,)
from com.vaadin.terminal.gwt.client.ui.dd.VHasDropHandler import (VHasDropHandler,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ui.VCustomComponent import (VCustomComponent,)
from com.vaadin.terminal.gwt.client.ui.dd.DDUtil import (DDUtil,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.ui.dd.VAcceptCallback import (VAcceptCallback,)
from com.vaadin.terminal.gwt.client.ui.dd.VTransferable import (VTransferable,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.gwt.client.ui.dd.VDragAndDropManager import (VDragAndDropManager,)
from com.vaadin.terminal.gwt.client.ui.dd.VAbstractDropHandler import (VAbstractDropHandler,)
# from com.google.gwt.xhr.client.ReadyStateChangeHandler import (ReadyStateChangeHandler,)
# from com.google.gwt.xhr.client.XMLHttpRequest import (XMLHttpRequest,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.List import (List,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)


class VDragAndDropWrapper(VCustomComponent, VHasDropHandler):
    """Must have features pending:

    drop details: locations + sizes in document hierarchy up to wrapper
    """
    _CLASSNAME = 'v-ddwrapper'

    def __init__(self):
        super(VDragAndDropWrapper, self)()
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        self.hookHtml5Events(self.getElement())
        self.setStyleName(self._CLASSNAME)

        class _0_(MouseDownHandler):

            def onMouseDown(self, event):
                if VDragAndDropWrapper_this.startDrag(event.getNativeEvent()):
                    event.preventDefault()
                    # prevent text selection

        _0_ = _0_()
        self.addDomHandler(_0_, MouseDownEvent.getType())

        class _1_(TouchStartHandler):

            def onTouchStart(self, event):
                if VDragAndDropWrapper_this.startDrag(event.getNativeEvent()):
                    # Dont let eg. panel start scrolling.
                    event.stopPropagation()

        _1_ = _1_()
        self.addDomHandler(_1_, TouchStartEvent.getType())
        self.sinkEvents(Event.TOUCHEVENTS)

    def onBrowserEvent(self, event):
        super(VDragAndDropWrapper, self).onBrowserEvent(event)
        if self._client is not None:
            self._client.handleTooltipEvent(event, self)

    def startDrag(self, event):
        """Starts a drag and drop operation from mousedown or touchstart event if
        required conditions are met.

        @param event
        @return true if the event was handled as a drag start event
        """
        if self._dragStarMode > 0:
            transferable = VTransferable()
            transferable.setDragSource(VDragAndDropWrapper_this)
            w = Util.findWidget(event.getEventTarget(), None)
            while w is not None and not isinstance(w, Paintable):
                w = w.getParent()
            paintable = w
            transferable.setData('component', paintable)
            dragEvent = VDragAndDropManager.get().startDrag(transferable, event, True)
            transferable.setData('mouseDown', MouseEventDetails(event).serialize())
            if self._dragStarMode == self._WRAPPER:
                dragEvent.createDragImage(self.getElement(), True)
            else:
                dragEvent.createDragImage(paintable.getElement(), True)
            return True
        return False

    _client = None
    _dropHandler = None
    _vaadinDragEvent = None
    _NONE = 0
    _COMPONENT = 1
    _WRAPPER = 2
    _dragStarMode = None
    _filecounter = 0
    _fileIdToReceiver = None

    def updateFromUIDL(self, uidl, client):
        self._client = client
        super(VDragAndDropWrapper, self).updateFromUIDL(uidl, client)
        if not uidl.hasAttribute('cached') and not uidl.hasAttribute('hidden'):
            acceptCrit = uidl.getChildByTagName('-ac')
            if acceptCrit is None:
                self._dropHandler = None
            else:
                if self._dropHandler is None:
                    self._dropHandler = self.CustomDropHandler()
                self._dropHandler.updateAcceptRules(acceptCrit)
            variableNames = uidl.getVariableNames()
            for fileId in variableNames:
                if fileId.startswith('rec-'):
                    receiverUrl = uidl.getStringVariable(fileId)
                    fileId = fileId[4:]
                    if self._fileIdToReceiver is None:
                        self._fileIdToReceiver = dict()
                    if '' == receiverUrl:
                        id = int(fileId)
                        indexOf = self._fileIds.index(id)
                        if indexOf != -1:
                            self._files.remove(indexOf)
                            self._fileIds.remove(indexOf)
                    else:
                        self._fileIdToReceiver.put(fileId, receiverUrl)
            self.startNextUpload()
            self._dragStarMode = uidl.getIntAttribute('dragStartMode')

    _uploading = None

    class readyStateChangeHandler(ReadyStateChangeHandler):

        def onReadyStateChange(self, xhr):
            if xhr.getReadyState() == XMLHttpRequest.DONE:
                # visit server for possible
                # variable changes
                VDragAndDropWrapper_this._client.sendPendingVariableChanges()
                VDragAndDropWrapper_this._uploading = False
                VDragAndDropWrapper_this.startNextUpload()
                xhr.clearOnReadyStateChange()

    _dragleavetimer = None

    def startNextUpload(self):

        class _3_(Command):

            def execute(self):
                if not VDragAndDropWrapper_this._uploading:
                    if len(VDragAndDropWrapper_this._fileIds) > 0:
                        VDragAndDropWrapper_this._uploading = True
                        fileId = VDragAndDropWrapper_this._fileIds.remove(0)
                        file = VDragAndDropWrapper_this._files.remove(0)
                        receiverUrl = VDragAndDropWrapper_this._client.translateVaadinUri(VDragAndDropWrapper_this._fileIdToReceiver.remove(str(fileId)))
                        extendedXHR = VDragAndDropWrapper_this.ExtendedXHR.create()
                        extendedXHR.setOnReadyStateChange(VDragAndDropWrapper_this.readyStateChangeHandler)
                        extendedXHR.open('POST', receiverUrl)
                        extendedXHR.postFile(file)

        _3_ = _3_()
        Scheduler.get().scheduleDeferred(_3_)

    def html5DragEnter(self, event):
        if self._dropHandler is None:
            return True
        try:
            if self._dragleavetimer is not None:
                # returned quickly back to wrapper
                self._dragleavetimer.cancel()
                self._dragleavetimer = None
            if VDragAndDropManager.get().getCurrentDropHandler() != self.getDropHandler():
                transferable = VTransferable()
                transferable.setDragSource(self)
                self._vaadinDragEvent = VDragAndDropManager.get().startDrag(transferable, event, False)
                VDragAndDropManager.get().setCurrentDropHandler(self.getDropHandler())
            event.preventDefault()
            event.stopPropagation()
            return False
        except Exception, e:
            GWT.getUncaughtExceptionHandler().onUncaughtException(e)
            return True

    def html5DragLeave(self, event):
        if self._dropHandler is None:
            return True
        try:

            class _4_(Timer):

                def run(self):
                    # Yes, dragleave happens before drop. Makes no sense to me.
                    # IMO shouldn't fire leave at all if drop happens (I guess
                    # this
                    # is what IE does).
                    # In Vaadin we fire it only if drop did not happen.
                    if (
                        VDragAndDropWrapper_this._vaadinDragEvent is not None and VDragAndDropManager.get().getCurrentDropHandler() == VDragAndDropWrapper_this.getDropHandler()
                    ):
                        VDragAndDropManager.get().interruptDrag()

            _4_ = _4_()
            self._dragleavetimer = _4_
            self._dragleavetimer.schedule(350)
            event.preventDefault()
            event.stopPropagation()
            return False
        except Exception, e:
            GWT.getUncaughtExceptionHandler().onUncaughtException(e)
            return True

    def html5DragOver(self, event):
        if self._dropHandler is None:
            return True
        if self._dragleavetimer is not None:
            # returned quickly back to wrapper
            self._dragleavetimer.cancel()
            self._dragleavetimer = None
        self._vaadinDragEvent.setCurrentGwtEvent(event)
        self.getDropHandler().dragOver(self._vaadinDragEvent)
        # needed to be set for Safari, otherwise drop will not happen
        if BrowserInfo.get().isWebkit():
            s = event.getEffectAllowed()
            if ('all' == s) or s.contains('opy'):
                event.setDragEffect('copy')
            else:
                event.setDragEffect(s)
        event.preventDefault()
        event.stopPropagation()
        return False

    def html5DragDrop(self, event):
        if (self._dropHandler is None) or (not self._currentlyValid):
            return True
        try:
            transferable = self._vaadinDragEvent.getTransferable()
            types = event.getTypes()
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(types)):
                    break
                type = types.get(i)
                if self.isAcceptedType(type):
                    data = event.getDataAsText(type)
                    if data is not None:
                        transferable.setData(type, data)
            fileCount = event.getFileCount()
            if fileCount > 0:
                transferable.setData('filecount', fileCount)
                _1 = True
                i = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        i += 1
                    if not (i < fileCount):
                        break
                    fileId = POSTINC(globals(), locals(), 'self._filecounter')
                    file = event.getFile(i)
                    transferable.setData('fi' + i, '' + fileId)
                    transferable.setData('fn' + i, file.getName())
                    transferable.setData('ft' + i, file.getType())
                    transferable.setData('fs' + i, file.getSize())
                    self.queueFilePost(fileId, file)
            VDragAndDropManager.get().endDrag()
            self._vaadinDragEvent = None
            event.preventDefault()
            event.stopPropagation()
            return False
        except Exception, e:
            GWT.getUncaughtExceptionHandler().onUncaughtException(e)
            return True

    acceptedTypes = ['Text', 'Url', 'text/html', 'text/plain', 'text/rtf']

    def isAcceptedType(self, type):
        for t in self.acceptedTypes:
            if t == type:
                return True
        return False

    class ExtendedXHR(XMLHttpRequest):
        # Currently supports only FF36 as no other browser supports natively File
        # api.
        # 
        # @param fileId
        # @param data

        def __init__(self):
            pass

        def postFile(self, file):
            JS("""

            @{{self}}.setRequestHeader('Content-Type', 'multipart/form-data');
            @{{self}}.send(@{{file}});
        """)
            pass

    _fileIds = list()
    _files = list()

    def queueFilePost(self, fileId, file):
        self._fileIds.add(fileId)
        self._files.add(file)

    def getPid(self):
        return self._client.getPid(self)

    def getDropHandler(self):
        return self._dropHandler

    verticalDropLocation = None
    horizontalDropLocation = None
    _emphasizedVDrop = None
    _emphasizedHDrop = None
    # Flag used by html5 dd
    _currentlyValid = None
    _OVER_STYLE = 'v-ddwrapper-over'

    def CustomDropHandler(VDragAndDropWrapper_this, *args, **kwargs):

        class CustomDropHandler(VAbstractDropHandler):

            def dragEnter(self, drag):
                VDragAndDropWrapper_this.updateDropDetails(drag)
                VDragAndDropWrapper_this._currentlyValid = False
                super(CustomDropHandler, self).dragEnter(drag)

            def dragLeave(self, drag):
                VDragAndDropWrapper_this.deEmphasis(True)
                VDragAndDropWrapper_this._dragleavetimer = None

            def dragOver(self, drag):
                detailsChanged = VDragAndDropWrapper_this.updateDropDetails(drag)
                if detailsChanged:
                    VDragAndDropWrapper_this._currentlyValid = False

                    class _5_(VAcceptCallback):

                        def accepted(self, event):
                            CustomDropHandler_this.dragAccepted(self.drag)

                    _5_ = _5_()
                    self.validate(_5_, drag)

            def drop(self, drag):
                VDragAndDropWrapper_this.deEmphasis(True)
                dd = drag.getDropDetails()
                # this is absolute layout based, and we may want to set
                # component
                # relatively to where the drag ended.
                # need to add current location of the drop area
                absoluteLeft = self.getAbsoluteLeft()
                absoluteTop = self.getAbsoluteTop()
                dd.put('absoluteLeft', absoluteLeft)
                dd.put('absoluteTop', absoluteTop)
                if VDragAndDropWrapper_this.verticalDropLocation is not None:
                    dd.put('verticalLocation', str(VDragAndDropWrapper_this.verticalDropLocation))
                    dd.put('horizontalLocation', str(VDragAndDropWrapper_this.horizontalDropLocation))
                return super(CustomDropHandler, self).drop(drag)

            def dragAccepted(self, drag):
                VDragAndDropWrapper_this._currentlyValid = True
                VDragAndDropWrapper_this.emphasis(drag)

            def getPaintable(self):
                return VDragAndDropWrapper_this

            def getApplicationConnection(self):
                return VDragAndDropWrapper_this._client

        return CustomDropHandler(*args, **kwargs)

    def hookHtml5Events(self, el):
        """Prototype code, memory leak risk.

        @param el
        """
        JS("""

            var me = @{{self}};
            
            if(@{{el}}.addEventListener) {
                @{{el}}.addEventListener("dragenter",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragEnter(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                }, false);
                
                @{{el}}.addEventListener("dragleave",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragLeave(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                }, false);
        
                @{{el}}.addEventListener("dragover",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragOver(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                }, false);
        
                @{{el}}.addEventListener("drop",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragDrop(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                }, false);
            
            } else {
                @{{el}}.attachEvent("ondragenter",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragEnter(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                });
                
                @{{el}}.attachEvent("ondragleave",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragLeave(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                });
        
                @{{el}}.attachEvent("ondragover",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragOver(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                });
        
                @{{el}}.attachEvent("ondrop",  function(ev) {
                    return me.@com.vaadin.terminal.gwt.client.ui.VDragAndDropWrapper::html5DragDrop(Lcom/vaadin/terminal/gwt/client/ui/dd/VHtml5DragEvent;)(ev);
                });
            }
        
    """)
        pass

    def updateDropDetails(self, drag):
        oldVL = self.verticalDropLocation
        self.verticalDropLocation = DDUtil.getVerticalDropLocation(self.getElement(), drag.getCurrentGwtEvent(), 0.2)
        drag.getDropDetails().put('verticalLocation', str(self.verticalDropLocation))
        oldHL = self.horizontalDropLocation
        self.horizontalDropLocation = DDUtil.getHorizontalDropLocation(self.getElement(), drag.getCurrentGwtEvent(), 0.2)
        drag.getDropDetails().put('horizontalLocation', str(self.horizontalDropLocation))
        if (
            (oldHL != self.horizontalDropLocation) or (oldVL != self.verticalDropLocation)
        ):
            return True
        else:
            return False

    def deEmphasis(self, doLayout):
        size = None
        if doLayout:
            size = RenderInformation.Size(self.getOffsetWidth(), self.getOffsetHeight())
        if self._emphasizedVDrop is not None:
            VDragAndDropWrapper.setStyleName(self.getElement(), self._OVER_STYLE, False)
            VDragAndDropWrapper.setStyleName(self.getElement(), self._OVER_STYLE + '-' + str(self._emphasizedVDrop).toLowerCase(), False)
            VDragAndDropWrapper.setStyleName(self.getElement(), self._OVER_STYLE + '-' + str(self._emphasizedHDrop).toLowerCase(), False)
        if doLayout:
            self.handleVaadinRelatedSizeChange(size)

    def emphasis(self, drag):
        size = RenderInformation.Size(self.getOffsetWidth(), self.getOffsetHeight())
        self.deEmphasis(False)
        VDragAndDropWrapper.setStyleName(self.getElement(), self._OVER_STYLE, True)
        VDragAndDropWrapper.setStyleName(self.getElement(), self._OVER_STYLE + '-' + str(self.verticalDropLocation).toLowerCase(), True)
        VDragAndDropWrapper.setStyleName(self.getElement(), self._OVER_STYLE + '-' + str(self.horizontalDropLocation).toLowerCase(), True)
        self._emphasizedVDrop = self.verticalDropLocation
        self._emphasizedHDrop = self.horizontalDropLocation
        # TODO build (to be an example) an emphasis mode where drag image
        # is fitted before or after the content
        self.handleVaadinRelatedSizeChange(size)

    def handleVaadinRelatedSizeChange(self, originalSize):
        if self.isDynamicHeight() or self.isDynamicWidth():
            if (
                not (originalSize == RenderInformation.Size(self.getOffsetWidth(), self.getOffsetHeight()))
            ):
                Util.notifyParentOfSizeChange(VDragAndDropWrapper_this, False)
        self._client.handleComponentRelativeSize(VDragAndDropWrapper_this)
        Util.notifyParentOfSizeChange(self, False)
