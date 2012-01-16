# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

from muntjac.event.transferable_impl import TransferableImpl
from muntjac.event.dd.drag_source import IDragSource
from muntjac.event.dd.drop_target import IDropTarget
from muntjac.event.dd.target_details_impl import TargetDetailsImpl
from muntjac.ui.html5_file import Html5File
from muntjac.ui.custom_component import CustomComponent
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails

from muntjac.terminal.stream_variable import \
    (IStreamVariable, IStreamingEndEvent, IStreamingErrorEvent,
    IStreamingProgressEvent, IStreamingStartEvent)


from muntjac.terminal.gwt.client.ui.dd.horizontal_drop_location import \
    HorizontalDropLocation

from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import \
    VerticalDropLocation


class DragAndDropWrapper(CustomComponent, IDropTarget, IDragSource):

    CLIENT_WIDGET = None #ClientWidget(VDragAndDropWrapper, LoadStyle.EAGER)

    def __init__(self, root):
        """Wraps given component in a L{DragAndDropWrapper}.

        @param root: the component to be wrapped
        """
        super(DragAndDropWrapper, self).__init__(root)

        self._receivers = dict()

        self._dragStartMode = DragStartMode.NONE

        self._dropHandler = None


    def paintContent(self, target):
        super(DragAndDropWrapper, self).paintContent(target)
        target.addAttribute('dragStartMode',
                DragStartMode.ordinal(self._dragStartMode))

        if self.getDropHandler() is not None:
            self.getDropHandler().getAcceptCriterion().paint(target)

        if self._receivers is not None and len(self._receivers) > 0:
            for idd, html5File in self._receivers.iteritems():
                if html5File.getStreamVariable() is not None:
                    target.addVariable(self, 'rec-' + idd,
                            ProxyReceiver(html5File))
                    # these are cleaned from receivers once the upload
                    # has started
                else:
                    # instructs the client side not to send the file
                    target.addVariable(self, 'rec-' + idd, None)
                    # forget the file from subsequent paints
                    del self._receivers[idd]


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
        super(WrapperTransferable, self).__init__(sourceComponent, rawVariables)

        self._files = None

        fc = rawVariables.get('filecount')
        if fc is not None:
            self._files = [None] * fc
            for i in range(fc):
                fd = Html5File(rawVariables.get('fn%d' % i),  # name
                        rawVariables.get('fs%d' % i),  # size
                        rawVariables.get('ft%d' % i))  # mime
                idd = rawVariables.get('fi%d' % i)
                self._files[i] = fd
                self._sourceComponent._receivers[idd] = fd
                self._sourceComponent.requestRepaint()  # paint receivers


    def getDraggedComponent(self):
        """The component in wrapper that is being dragged or null if the
        transferrable is not a component (most likely an html5 drag).
        """
        return self.getData('component')


    def getMouseDownEvent(self):
        """@return: the mouse down event that started the drag and drop
        operation
        """
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

    def __init__(self, rawDropData, wrapper):
        super(WrapperTargetDetails, self).__init__(rawDropData, wrapper)


    def getAbsoluteLeft(self):
        """@return: the absolute position of wrapper on the page"""
        return self.getData('absoluteLeft')


    def getAbsoluteTop(self):
        """@return: the absolute position of wrapper on the page"""
        return self.getData('absoluteTop')


    def getMouseEvent(self):
        """@return: details about the actual event that caused the event
                    details. Practically mouse move or mouse up.
        """
        return MouseEventDetails.deSerialize(self.getData('mouseEvent'))


    def getVerticalDropLocation(self):
        """@return: a detail about the drags vertical position over the
                    wrapper.
        """
        data = self.getData('verticalLocation')
        return VerticalDropLocation.valueOf[data]


    def getHorizontalDropLocation(self):
        """@return: a detail about the drags horizontal position over the
                    wrapper.
        """
        data = self.getData('horizontalLocation')
        return HorizontalDropLocation.valueOf[data]


    def verticalDropLocation(self):
        """@deprecated: use L{getVerticalDropLocation} instead"""
        return self.getVerticalDropLocation()


    def horizontalDropLocation(self):
        """@deprecated: use L{getHorizontalDropLocation} instead"""
        return self.getHorizontalDropLocation()


class DragStartMode(object):
    #: L{DragAndDropWrapper} does not start drag events at all
    NONE = 'NONE'

    #: The component on which the drag started will be shown as drag image.
    COMPONENT = 'COMPONENT'

    #: The whole wrapper is used as a drag image when dragging.
    WRAPPER = 'WRAPPER'

    _values = [NONE, COMPONENT, WRAPPER]

    @classmethod
    def values(cls):
        return cls._values[:]

    @classmethod
    def ordinal(cls, val):
        return cls._values.index(val)


class ProxyReceiver(IStreamVariable):

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
        wrapper = ReceivingEventWrapper(event, self._file, self)
        self._file.getStreamVariable().onProgress(wrapper)


    def streamingStarted(self, event):
        self._listenProgressOfUploadedFile = \
                self._file.getStreamVariable() is not None

        if self._listenProgressOfUploadedFile:
            wrapper = ReceivingEventWrapper(event, self._file, self)
            self._file.getStreamVariable().streamingStarted(wrapper)

        # no need tell to the client about this receiver on next paint
        self.receivers.remove(self._file)

        # let the terminal GC the stream variable and not to accept
        # other file uploads to this variable
        event.disposeStreamVariable()


    def streamingFinished(self, event):
        if self._listenProgressOfUploadedFile:
            wrapper = ReceivingEventWrapper(event, self._file, self)
            self._file.getStreamVariable().streamingFinished(wrapper)


    def streamingFailed(self, event):
        if self._listenProgressOfUploadedFile:
            wrapper = ReceivingEventWrapper(event, self._file, self)
            self._file.getStreamVariable().streamingFailed(wrapper)


    def isInterrupted(self):
        return self._file.getStreamVariable().isInterrupted()


class ReceivingEventWrapper(IStreamingErrorEvent, IStreamingEndEvent,
            IStreamingStartEvent, IStreamingProgressEvent):
    # With XHR2 file posts we can't provide as much information from the
    # terminal as with multipart request. This helper class wraps the
    # terminal event and provides the lacking information from the
    # Html5File.

    def __init__(self, e, fd, receiver):
        self._wrappedEvent = e
        self._file = fd
        self._receiver = receiver


    def getMimeType(self):
        return self._file.getType()


    def getFileName(self):
        return self._file.getFileName()


    def getContentLength(self):
        return self._file.getFileSize()


    def getReceiver(self):
        return self._receiver

    def getException(self):
        if isinstance(self._wrappedEvent, IStreamingErrorEvent):
            return self._wrappedEvent.getException()
        return None


    def getBytesReceived(self):
        return self._wrappedEvent.getBytesReceived()


    def disposeStreamVariable(self):
        """Calling this method has no effect. DD files are receive only
        once anyway.
        """
        pass
