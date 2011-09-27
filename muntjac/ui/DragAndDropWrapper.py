# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.terminal.gwt.client.ui.dd.VerticalDropLocation import \
    VerticalDropLocation

from muntjac.event.dd.DragSource import DragSource
from muntjac.ui.Html5File import Html5File
from muntjac.event.TransferableImpl import TransferableImpl
from muntjac.terminal.gwt.client.MouseEventDetails import MouseEventDetails

from muntjac.terminal.StreamVariable import \
    StreamVariable, StreamingEndEvent, StreamingErrorEvent, \
    StreamingProgressEvent, StreamingStartEvent

from muntjac.event.dd.TargetDetailsImpl import TargetDetailsImpl
from muntjac.ui.CustomComponent import CustomComponent
from muntjac.event.dd.DropTarget import DropTarget

from muntjac.terminal.gwt.client.ui.dd.HorizontalDropLocation import \
    HorizontalDropLocation

#from muntjac.ui.ClientWidget import LoadStyle
#
#from muntjac.terminal.gwt.client.ui.VDragAndDropWrapper import \
#    VDragAndDropWrapper


class DragAndDropWrapper(CustomComponent, DropTarget, DragSource):

#    CLIENT_WIDGET = VDragAndDropWrapper
#    LOAD_STYLE = LoadStyle.EAGER

    def __init__(self, root):
        """Wraps given component in a {@link DragAndDropWrapper}.

        @param root
                   the component to be wrapped
        """
        super(DragAndDropWrapper, self)(root)

        self._receivers = dict()
        self._dragStartMode = DragStartMode.NONE

        self._dropHandler = None


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
                idd = entry.getKey()
                html5File = entry.getValue()
                if html5File.getStreamVariable() is not None:
                    target.addVariable(self, 'rec-' + idd, self.ProxyReceiver(html5File))
                    # these are cleaned from receivers once the upload has
                    # started
                else:
                    # instructs the client side not to send the file
                    target.addVariable(self, 'rec-' + idd, None)
                    # forget the file from subsequent paints
                    it.remove()


    def getDropHandler(self):
        return self._dropHandler


    def setDropHandler(self, dropHandler):
        self._dropHandler = dropHandler
        self.requestRepaint()


    def translateDropTargetDetails(self, clientVariables):
        return WrapperTargetDetails(clientVariables, self)


    def getTransferable(self, rawVariables):
        return WrapperTransferable(self, rawVariables)


    def setDragStartMode(self, dragStartMode):
        self._dragStartMode = dragStartMode
        self.requestRepaint()


    def getDragStartMode(self):
        return self._dragStartMode


class WrapperTransferable(TransferableImpl):

    def __init__(self, sourceComponent, rawVariables):
        super(WrapperTransferable, self)(sourceComponent, rawVariables)

        self._files = None

        fc = rawVariables.get('filecount')
        if fc is not None:
            self._files = [None] * fc
            for i in range(fc):
                fd = Html5File(rawVariables.get('fn' + i),
                               rawVariables.get('fs' + i),
                               rawVariables.get('ft' + i))  # mime
                idd = rawVariables.get('fi' + i)
                self._files[i] = fd
                self.receivers[idd] = fd
                self.requestRepaint()  # paint Receivers


    def getDraggedComponent(self):
        """The component in wrapper that is being dragged or null if the
        transferrable is not a component (most likely an html5 drag).

        @return
        """
        obj = self.getData('component')
        return obj


    def getMouseDownEvent(self):
        """@return the mouse down event that started the drag and drop operation"""
        return MouseEventDetails.deSerialize(self.getData('mouseDown'))


    def getFiles(self):
        return self._files


    def getText(self):
        data = self.getData('Text')  # IE, html5

        if data is None:
            # check for "text/plain" (webkit)
            data = self.getData('text/plain')

        return data


    def getHtml(self):
        data = self.getData('Html')  # IE, html5

        if data is None:
            # check for "text/plain" (webkit)
            data = self.getData('text/html')

        return data


class WrapperTargetDetails(TargetDetailsImpl):

    def __init__(self, rawDropData, _DragAndDropWrapper_this):
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
        return VerticalDropLocation.valueOf[self.getData('verticalLocation')]


    def getHorizontalDropLocation(self):
        """@return a detail about the drags horizontal position over the wrapper."""
        return HorizontalDropLocation.valueOf[self.getData('horizontalLocation')]


    def verticalDropLocation(self):
        """@deprecated use {@link #getVerticalDropLocation()} instead"""
        return self.getVerticalDropLocation()


    def horizontalDropLocation(self):
        """@deprecated use {@link #getHorizontalDropLocation()} instead"""
        return self.getHorizontalDropLocation()


class DragStartMode(object):
    # {@link DragAndDropWrapper} does not start drag events at all
    NONE = 'NONE'

    # The component on which the drag started will be shown as drag image.
    COMPONENT = 'COMPONENT'

    # The whole wrapper is used as a drag image when dragging.
    WRAPPER = 'WRAPPER'

    _values = [NONE, COMPONENT, WRAPPER]

    @classmethod
    def values(cls):
        return cls._values[:]


class ProxyReceiver(StreamVariable):  # FIXME: nested classes

    def __init__(self, fd):
        self._file = fd
        self._listenProgressOfUploadedFile = None


    def getOutputStream(self):
        if self._file.getStreamVariable() is None:
            return None
        return self._file.getStreamVariable().getOutputStream()


    def listenProgress(self):
        return self._file.getStreamVariable().listenProgress()


    def onProgress(self, event):
        self._file.getStreamVariable().onProgress( ReceivingEventWrapper(event, self._file, self) )


    def streamingStarted(self, event):
        self._listenProgressOfUploadedFile = self._file.getStreamVariable() is not None
        if self._listenProgressOfUploadedFile:
            self._file.getStreamVariable().streamingStarted( ReceivingEventWrapper(event, self._file, self) )
        # no need tell to the client about this receiver on next paint
        self.receivers.remove(self._file)
        # let the terminal GC the streamvariable and not to accept other
        # file uploads to this variable
        event.disposeStreamVariable()


    def streamingFinished(self, event):
        if self._listenProgressOfUploadedFile:
            self._file.getStreamVariable().streamingFinished( ReceivingEventWrapper(event, self._file, self) )


    def streamingFailed(self, event):
        if self._listenProgressOfUploadedFile:
            self._file.getStreamVariable().streamingFailed( ReceivingEventWrapper(event, self._file, self) )


    def isInterrupted(self):
        return self._file.getStreamVariable().isInterrupted()


class ReceivingEventWrapper(StreamingErrorEvent, StreamingEndEvent,
                            StreamingStartEvent, StreamingProgressEvent):
    # With XHR2 file posts we can't provide as much information from the
    # terminal as with multipart request. This helper class wraps the
    # terminal event and provides the lacking information from the
    # Html5File.

    def __init__(self, e, fd, _ProxyReceiver_this):
        self._wrappedEvent = e
        self._file = fd
        self._ProxyReceiver_this = _ProxyReceiver_this

    def getMimeType(self):
        return self._file.getType()


    def getFileName(self):
        return self._file.getFileName()


    def getContentLength(self):
        return self._file.getFileSize()


    def getReceiver(self):
        return self._ProxyReceiver_this

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
