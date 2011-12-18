# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from __pyjamas__ import JS

import pygwt as GWT

from pyjamas.ui import Event

from pyjamas.Timer import Timer

from muntjac.terminal.gwt.client.ui.dd.v_has_dropHandler import VHasDropHandler
from muntjac.terminal.gwt.client.paintable import Paintable
from muntjac.terminal.gwt.client.ui.v_custom_component import VCustomComponent
from muntjac.terminal.gwt.client.ui.dd.dd_util import DDUtil
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.render_information import Size
from muntjac.terminal.gwt.client.ui.dd.v_accept_callback import VAcceptCallback
from muntjac.terminal.gwt.client.ui.dd.v_transferable import VTransferable
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails

from muntjac.terminal.gwt.client.ui.dd.v_drag_and_drop_manager \
    import VDragAndDropManager

from muntjac.terminal.gwt.client.ui.dd.v_abstract_drop_handler \
    import VAbstractDropHandler


class VDragAndDropWrapper(VCustomComponent, VHasDropHandler):
    """Must have features pending:

    drop details: locations + sizes in document hierarchy up to wrapper
    """

    _CLASSNAME = 'v-ddwrapper'

    _NONE = 0
    _COMPONENT = 1
    _WRAPPER = 2

    _OVER_STYLE = 'v-ddwrapper-over'

    def __init__(self):
        self._client = None
        self._dropHandler = None
        self._vaadinDragEvent = None
        self._dragStarMode = None
        self._filecounter = 0
        self._fileIdToReceiver = None

        self._uploading = None
        self._dragleavetimer = None
        self.acceptedTypes = ['Text', 'Url', 'text/html', 'text/plain',
                'text/rtf']

        self.readyStateChangeHandler = MyReadyStateChangeHandler()

        self._fileIds = list()
        self._files = list()

        self.verticalDropLocation = None
        self.horizontalDropLocation = None
        self._emphasizedVDrop = None
        self._emphasizedHDrop = None
        # Flag used by html5 dd
        self._currentlyValid = None

        super(VDragAndDropWrapper, self).__init__()

        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        self.hookHtml5Events(self.getElement())
        self.setStyleName(self._CLASSNAME)

        class _0_(MouseDownHandler):

            def onMouseDown(self, event):
                if VDragAndDropWrapper_this.startDrag(event.getNativeEvent()):
                    event.preventDefault()  # prevent text selection

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
        """Starts a drag and drop operation from mousedown or touchstart event
        if required conditions are met.

        @return: true if the event was handled as a drag start event
        """
        if self._dragStarMode > 0:
            transferable = VTransferable()
            transferable.setDragSource(self)

            w = Util.findWidget(event.getEventTarget(), None)
            while w is not None and not isinstance(w, Paintable):
                w = w.getParent()
            paintable = w

            transferable.setData('component', paintable)
            dragEvent = VDragAndDropManager.get().startDrag(transferable,
                    event, True)

            transferable.setData('mouseDown',
                    MouseEventDetails(event).serialize())

            if self._dragStarMode == self._WRAPPER:
                dragEvent.createDragImage(self.getElement(), True)
            else:
                dragEvent.createDragImage(paintable.getElement(), True)

            return True

        return False


    def updateFromUIDL(self, uidl, client):
        self._client = client
        super(VDragAndDropWrapper, self).updateFromUIDL(uidl, client)
        if not uidl.hasAttribute('cached') and not uidl.hasAttribute('hidden'):
            acceptCrit = uidl.getChildByTagName('-ac')
            if acceptCrit is None:
                self._dropHandler = None
            else:
                if self._dropHandler is None:
                    self._dropHandler = CustomDropHandler()

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
                        self._fileIdToReceiver[fileId] = receiverUrl

            self.startNextUpload()

            self._dragStarMode = uidl.getIntAttribute('dragStartMode')


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

            if (VDragAndDropManager.get().getCurrentDropHandler()
                    != self.getDropHandler()):
                transferable = VTransferable()
                transferable.setDragSource(self)

                self._vaadinDragEvent = VDragAndDropManager.get().startDrag(
                        transferable, event, False)
                VDragAndDropManager.get().setCurrentDropHandler(
                        self.getDropHandler())

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
            for i in range(len(types)):
                type = types.get(i)
                if self.isAcceptedType(type):
                    data = event.getDataAsText(type)
                    if data is not None:
                        transferable.setData(type, data)

            fileCount = event.getFileCount()
            if fileCount > 0:
                transferable.setData('filecount', fileCount)
                for i in range(fileCount):
                    fileId = self._filecounter
                    self._filecounter += 1
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


    def isAcceptedType(self, type):
        for t in self.acceptedTypes:
            if t == type:
                return True
        return False

    # Currently supports only FF36 as no other browser supports natively File
    # api.

    def queueFilePost(self, fileId, file):
        self._fileIds.add(fileId)
        self._files.add(file)


    def getPid(self):
        return self._client.getPid(self)


    def getDropHandler(self):
        return self._dropHandler


    def hookHtml5Events(self, el):
        """Prototype code, memory leak risk.
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
        self.verticalDropLocation = DDUtil.getVerticalDropLocation(
                self.getElement(), drag.getCurrentGwtEvent(), 0.2)
        drag.getDropDetails()['verticalLocation'] = \
                str(self.verticalDropLocation)
        oldHL = self.horizontalDropLocation
        self.horizontalDropLocation = DDUtil.getHorizontalDropLocation(
                self.getElement(), drag.getCurrentGwtEvent(), 0.2)
        drag.getDropDetails()['horizontalLocation'] = \
                str(self.horizontalDropLocation)
        if ((oldHL != self.horizontalDropLocation)
                or (oldVL != self.verticalDropLocation)):
            return True
        else:
            return False


    def deEmphasis(self, doLayout):
        size = None
        if doLayout:
            size = Size(self.getOffsetWidth(), self.getOffsetHeight())

        if self._emphasizedVDrop is not None:
            VDragAndDropWrapper.setStyleName(self.getElement(),
                    self._OVER_STYLE, False)
            VDragAndDropWrapper.setStyleName(self.getElement(),
                    self._OVER_STYLE + '-'
                    + str(self._emphasizedVDrop).lower(), False)
            VDragAndDropWrapper.setStyleName(self.getElement(),
                    self._OVER_STYLE + '-'
                    + str(self._emphasizedHDrop).lower(), False)

        if doLayout:
            self.handleVaadinRelatedSizeChange(size)


    def emphasis(self, drag):
        size = Size(self.getOffsetWidth(), self.getOffsetHeight())
        self.deEmphasis(False)
        VDragAndDropWrapper.setStyleName(self.getElement(),
                self._OVER_STYLE, True)
        VDragAndDropWrapper.setStyleName(self.getElement(),
                self._OVER_STYLE + '-'
                + str(self.verticalDropLocation).lower(), True)
        VDragAndDropWrapper.setStyleName(self.getElement(),
                self._OVER_STYLE + '-'
                + str(self.horizontalDropLocation).lower(), True)
        self._emphasizedVDrop = self.verticalDropLocation
        self._emphasizedHDrop = self.horizontalDropLocation
        # TODO build (to be an example) an emphasis mode where drag image
        # is fitted before or after the content
        self.handleVaadinRelatedSizeChange(size)


    def handleVaadinRelatedSizeChange(self, originalSize):
        if self.isDynamicHeight() or self.isDynamicWidth():
            if (not (originalSize == Size(self.getOffsetWidth(),
                    self.getOffsetHeight()))):
                Util.notifyParentOfSizeChange(self, False)
        self._client.handleComponentRelativeSize(self)
        Util.notifyParentOfSizeChange(self, False)


class MyReadyStateChangeHandler(ReadyStateChangeHandler):

    def __init__(self, dndw):
        self._dndw = dndw

    def onReadyStateChange(self, xhr):
        if xhr.getReadyState() == XMLHttpRequest.DONE:
            # visit server for possible
            # variable changes
            self._dndw._client.sendPendingVariableChanges()
            self._dndw._uploading = False
            self._dndw.startNextUpload()
            xhr.clearOnReadyStateChange()


class ExtendedXHR(XMLHttpRequest):

    def __init__(self):
        pass

    def postFile(self, file):
        JS("""
            @{{self}}.setRequestHeader('Content-Type', 'multipart/form-data');
            @{{self}}.send(@{{file}});
        """)
        pass


class CustomDropHandler(VAbstractDropHandler):

    def __init__(self, dndw):
        self._dndw = dndw


    def dragEnter(self, drag):
        self._dndw.updateDropDetails(drag)
        self._dndw._currentlyValid = False
        super(CustomDropHandler, self).dragEnter(drag)


    def dragLeave(self, drag):
        self._dndw.deEmphasis(True)
        self._dndw._dragleavetimer = None


    def dragOver(self, drag):
        detailsChanged = self._dndw.updateDropDetails(drag)
        if detailsChanged:
            self._dndw._currentlyValid = False

            class _5_(VAcceptCallback):

                def accepted(self, event):
                    CustomDropHandler_this.dragAccepted(self.drag)

            _5_ = _5_()
            self.validate(_5_, drag)


    def drop(self, drag):
        self._dndw.deEmphasis(True)
        dd = drag.getDropDetails()
        # this is absolute layout based, and we may want to set
        # component relatively to where the drag ended.
        # need to add current location of the drop area
        absoluteLeft = self.getAbsoluteLeft()
        absoluteTop = self.getAbsoluteTop()
        dd['absoluteLeft'] = absoluteLeft
        dd['absoluteTop'] = absoluteTop
        if self._dndw.verticalDropLocation is not None:
            dd['verticalLocation'] = str(self._dndw.verticalDropLocation)
            dd['horizontalLocation'] = str(self._dndw.horizontalDropLocation)

        return super(CustomDropHandler, self).drop(drag)


    def dragAccepted(self, drag):
        self._dndw._currentlyValid = True
        self._dndw.emphasis(drag)


    def getPaintable(self):
        return self._dndw


    def getApplicationConnection(self):
        return self._dndw._client
