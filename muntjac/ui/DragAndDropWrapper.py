# Copyright (C) 2011 Vaadin Ltd
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

from com.vaadin.terminal.gwt.client.ui.dd.VerticalDropLocation import (VerticalDropLocation,)
from com.vaadin.event.dd.DragSource import (DragSource,)
from com.vaadin.ui.Html5File import (Html5File,)
from com.vaadin.event.TransferableImpl import (TransferableImpl,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.StreamVariable import (StreamVariable, StreamingEndEvent, StreamingErrorEvent, StreamingProgressEvent, StreamingStartEvent,)
from com.vaadin.event.dd.TargetDetailsImpl import (TargetDetailsImpl,)
from com.vaadin.ui.CustomComponent import (CustomComponent,)
from com.vaadin.event.dd.DropTarget import (DropTarget,)
from com.vaadin.terminal.gwt.client.ui.dd.HorizontalDropLocation import (HorizontalDropLocation,)
# from java.io.OutputStream import (OutputStream,)
# from java.util.HashMap import (HashMap,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)
# from java.util.Map.Entry import (Entry,)


class DragAndDropWrapper(CustomComponent, DropTarget, DragSource):

    class WrapperTransferable(TransferableImpl):
        _files = None

        def __init__(self, sourceComponent, rawVariables):
            super(WrapperTransferable, self)(sourceComponent, rawVariables)
            fc = rawVariables['filecount']
            if fc is not None:
                self._files = [None] * fc
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < fc):
                        break
                    file = Html5File(rawVariables['fn' + i], rawVariables['fs' + i], rawVariables['ft' + i])
                    # mime
                    id = rawVariables['fi' + i]
                    self._files[i] = file
                    self.receivers.put(id, file)
                    self.requestRepaint()
                    # paint Receivers

        def getDraggedComponent(self):
            """The component in wrapper that is being dragged or null if the
            transferrable is not a component (most likely an html5 drag).

            @return
            """
            object = self.getData('component')
            return object

        def getMouseDownEvent(self):
            """@return the mouse down event that started the drag and drop operation"""
            return MouseEventDetails.deSerialize(self.getData('mouseDown'))

        def getFiles(self):
            return self._files

        def getText(self):
            data = self.getData('Text')
            # IE, html5
            if data is None:
                # check for "text/plain" (webkit)
                data = self.getData('text/plain')
            return data

        def getHtml(self):
            data = self.getData('Html')
            # IE, html5
            if data is None:
                # check for "text/plain" (webkit)
                data = self.getData('text/html')
            return data

    _receivers = dict()

    class WrapperTargetDetails(TargetDetailsImpl):

        def __init__(self, rawDropData):
            super(WrapperTargetDetails, self)(rawDropData, _DragAndDropWrapper_this)

        def getAbsoluteLeft(self):
            """@return the absolute position of wrapper on the page"""
            return self.getData('absoluteLeft')

        def getAbsoluteTop(self):
            """@return the absolute position of wrapper on the page"""
            return self.getData('absoluteTop')

        def getMouseEvent(self):
            """@return details about the actual event that caused the event details.
                    Practically mouse move or mouse up.
            """
            return MouseEventDetails.deSerialize(self.getData('mouseEvent'))

        def getVerticalDropLocation(self):
            """@return a detail about the drags vertical position over the wrapper."""
            return VerticalDropLocation.valueOf(self.getData('verticalLocation'))

        def getHorizontalDropLocation(self):
            """@return a detail about the drags horizontal position over the wrapper."""
            return HorizontalDropLocation.valueOf(self.getData('horizontalLocation'))

        def verticalDropLocation(self):
            """@deprecated use {@link #getVerticalDropLocation()} instead"""
            return self.getVerticalDropLocation()

        def horizontalDropLocation(self):
            """@deprecated use {@link #getHorizontalDropLocation()} instead"""
            return self.getHorizontalDropLocation()

    class DragStartMode(object):
        # {@link DragAndDropWrapper} does not start drag events at all
        # The component on which the drag started will be shown as drag image.
        # The whole wrapper is used as a drag image when dragging.
        NONE = 'NONE'
        COMPONENT = 'COMPONENT'
        WRAPPER = 'WRAPPER'
        _values = [NONE, COMPONENT, WRAPPER]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    _dragStartMode = DragStartMode.NONE

    def __init__(self, root):
        """Wraps given component in a {@link DragAndDropWrapper}.

        @param root
                   the component to be wrapped
        """
        super(DragAndDropWrapper, self)(root)

    def paintContent(self, target):
        super(DragAndDropWrapper, self).paintContent(target)
        target.addAttribute('dragStartMode', self._dragStartMode.ordinal())
        if self.getDropHandler() is not None:
            self.getDropHandler().getAcceptCriterion().paint(target)
        if self._receivers is not None and len(self._receivers) > 0:
            _0 = True
            it = self._receivers.entrySet()
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                entry = it.next()
                id = entry.getKey()
                html5File = entry.getValue()
                if html5File.getStreamVariable() is not None:
                    target.addVariable(self, 'rec-' + id, self.ProxyReceiver(html5File))
                    # these are cleaned from receivers once the upload has
                    # started
                else:
                    # instructs the client side not to send the file
                    target.addVariable(self, 'rec-' + id, None)
                    # forget the file from subsequent paints
                    it.remove()

    _dropHandler = None

    def getDropHandler(self):
        return self._dropHandler

    def setDropHandler(self, dropHandler):
        self._dropHandler = dropHandler
        self.requestRepaint()

    def translateDropTargetDetails(self, clientVariables):
        return self.WrapperTargetDetails(clientVariables)

    def getTransferable(self, rawVariables):
        return self.WrapperTransferable(self, rawVariables)

    def setDragStartMode(self, dragStartMode):
        self._dragStartMode = dragStartMode
        self.requestRepaint()

    def getDragStartMode(self):
        return self._dragStartMode

    class ProxyReceiver(StreamVariable):
        _file = None

        def __init__(self, file):
            self._file = file

        _listenProgressOfUploadedFile = None

        def getOutputStream(self):
            if self._file.getStreamVariable() is None:
                return None
            return self._file.getStreamVariable().getOutputStream()

        def listenProgress(self):
            return self._file.getStreamVariable().listenProgress()

        def onProgress(self, event):
            self._file.getStreamVariable().onProgress(self.ReceivingEventWrapper(event))

        def streamingStarted(self, event):
            self._listenProgressOfUploadedFile = self._file.getStreamVariable() is not None
            if self._listenProgressOfUploadedFile:
                self._file.getStreamVariable().streamingStarted(self.ReceivingEventWrapper(event))
            # no need tell to the client about this receiver on next paint
            self.receivers.remove(self._file)
            # let the terminal GC the streamvariable and not to accept other
            # file uploads to this variable
            event.disposeStreamVariable()

        def streamingFinished(self, event):
            if self._listenProgressOfUploadedFile:
                self._file.getStreamVariable().streamingFinished(self.ReceivingEventWrapper(event))

        def streamingFailed(self, event):
            if self._listenProgressOfUploadedFile:
                self._file.getStreamVariable().streamingFailed(self.ReceivingEventWrapper(event))

        def isInterrupted(self):
            # With XHR2 file posts we can't provide as much information from the
            # terminal as with multipart request. This helper class wraps the
            # terminal event and provides the lacking information from the
            # Html5File.

            return self._file.getStreamVariable().isInterrupted()

        class ReceivingEventWrapper(StreamingErrorEvent, StreamingEndEvent, StreamingStartEvent, StreamingProgressEvent):
            _wrappedEvent = None

            def __init__(self, e):
                self._wrappedEvent = e

            def getMimeType(self):
                return self.file.getType()

            def getFileName(self):
                return self.file.getFileName()

            def getContentLength(self):
                return self.file.getFileSize()

            def getReceiver(self):
                return _ProxyReceiver_this

            def getException(self):
                if isinstance(self._wrappedEvent, StreamingErrorEvent):
                    return self._wrappedEvent.getException()
                return None

            def getBytesReceived(self):
                return self._wrappedEvent.getBytesReceived()

            def disposeStreamVariable(self):
                """Calling this method has no effect. DD files are receive only once
                anyway.
                """
                pass
