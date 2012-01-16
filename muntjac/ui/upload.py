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

"""For uploading files from client to server."""

from warnings import warn

from muntjac.ui.abstract_component import AbstractComponent

from muntjac.ui.component import \
    IFocusable, Event as ComponentEvent

from muntjac.terminal.stream_variable import \
    IStreamVariable, IStreamingEvent

from muntjac.terminal.gwt.server.exceptions import \
    NoInputStreamException, NoOutputStreamException


class IStartedListener(object):
    """Receives the events when the upload starts.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def uploadStarted(self, event):
        """Upload has started.

        @param event:
                   the Upload started event.
        """
        raise NotImplementedError


class IFinishedListener(object):
    """Receives the events when the uploads are ready.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def uploadFinished(self, event):
        """Upload has finished.

        @param event:
                   the Upload finished event.
        """
        raise NotImplementedError


class IFailedListener(object):
    """Receives events when the uploads are finished, but unsuccessful.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def uploadFailed(self, event):
        """Upload has finished unsuccessfully.

        @param event:
                   the Upload failed event.
        """
        raise NotImplementedError


class ISucceededListener(object):
    """Receives events when the uploads are successfully finished.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def uploadSucceeded(self, event):
        """Upload successfull..

        @param event:
                   the Upload successful event.
        """
        raise NotImplementedError


class IProgressListener(object):
    """IProgressListener receives events to track progress of upload."""

    def updateProgress(self, readBytes, contentLength):
        """Updates progress to listener.

        @param readBytes:
                   bytes transferred
        @param contentLength:
                   total size of file currently being uploaded, -1 if unknown
        """
        raise NotImplementedError


_UPLOAD_FINISHED_METHOD = getattr(IFinishedListener, 'uploadFinished')
_UPLOAD_FAILED_METHOD = getattr(IFailedListener, 'uploadFailed')
_UPLOAD_STARTED_METHOD = getattr(IStartedListener, 'uploadStarted')
_UPLOAD_SUCCEEDED_METHOD = getattr(ISucceededListener, 'uploadSucceeded')


class Upload(AbstractComponent, IFocusable): #IComponent,
    """IComponent for uploading files from client to server.

    The visible component consists of a file name input box and a browse
    button and an upload submit button to start uploading.

    The Upload component needs a StringIO to write the uploaded
    data. You need to implement the upload.IReceiver interface and return the
    output stream in the receiveUpload() method.

    You can get an event regarding starting (StartedEvent), progress
    (ProgressEvent), and finishing (FinishedEvent) of upload by implementing
    IStartedListener, IProgressListener, and IFinishedListener, respectively.
    The IFinishedListener is called for both failed and succeeded uploads. If
    you wish to separate between these two cases, you can use
    ISucceededListener (SucceededEvenet) and IFailedListener (FailedEvent).

    The upload component does not itself show upload progress, but you can use
    the ProgressIndicator for providing progress feedback by implementing
    IProgressListener and updating the indicator in updateProgress().

    Setting upload component immediate initiates the upload as soon as a file
    is selected, instead of the common pattern of file selection field and
    upload button.

    Note! Because of browser dependent implementations of <input type="file">
    element, setting size for Upload component is not supported. For some
    browsers setting size may work to some extent.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VUpload, LoadStyle.LAZY)

    def __init__(self, caption=None, uploadReceiver=None):
        """Creates a new instance of Upload.

        The receiver must be set before performing an upload.
        """
        super(Upload, self).__init__()

        #: Should the field be focused on next repaint?
        self._focus = False

        #: The tab order number of this field.
        self._tabIndex = 0

        #: The output of the upload is redirected to this receiver.
        self._receiver = None

        self._isUploading = False

        self._contentLength = -1

        self._totalBytes = None

        self._buttonCaption = 'Upload'

        #: ProgressListeners to which information about progress
        #  is sent during upload
        self._progressListeners = set()

        self._progressCallbacks = dict()

        self._interrupted = False

        self._notStarted = None

        self._nextid = 0

        #: Flag to indicate that submitting file has been requested.
        self._forceSubmit = None

        if caption:
            self.setCaption(caption)

        if uploadReceiver is not None:
            self._receiver = uploadReceiver

        self._streamVariable = None


    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see: L{AbstractComponent.changeVariables}
        """
        if 'pollForStart' in variables:
            idd = variables.get('pollForStart')
            if not self._isUploading and idd == self._nextid:
                self._notStarted = True
                self.requestRepaint()
            else:
                pass


    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   Target to paint the content on.
        @raise PaintException:
                    if the paint operation failed.
        """
        if self._notStarted:
            target.addAttribute('notStarted', True)
            self._notStarted = False
            return

        if self._forceSubmit:
            target.addAttribute('forceSubmit', True)
            self._forceSubmit = True
            return

        # The field should be focused
        if self._focus:
            target.addAttribute('focus', True)

        # The tab ordering number
        if self._tabIndex >= 0:
            target.addAttribute('tabindex', self._tabIndex)

        target.addAttribute('state', self._isUploading)

        if self._buttonCaption is not None:
            target.addAttribute('buttoncaption', self._buttonCaption)

        target.addAttribute('nextid', self._nextid)

        # Post file to this strean variable
        target.addVariable(self, 'action', self.getStreamVariable())


    def addListener(self, listener, iface=None):
        """Adds an event listener.

        @param listener:
                   the listener to be added.
        """
        if (isinstance(listener, IFailedListener) and
                (iface is None or issubclass(iface, IFailedListener))):
            self.registerListener(FailedEvent,
                    listener, _UPLOAD_FAILED_METHOD)

        if (isinstance(listener, IFinishedListener) and
                (iface is None or issubclass(iface, IFinishedListener))):
            self.registerListener(FinishedEvent,
                    listener, _UPLOAD_FINISHED_METHOD)

        if (isinstance(listener, IProgressListener) and
                (iface is None or issubclass(iface, IProgressListener))):
            self._progressListeners.add(listener)

        if (isinstance(listener, IStartedListener) and
                (iface is None or issubclass(iface, IStartedListener))):
            self.registerListener(StartedEvent,
                    listener, _UPLOAD_STARTED_METHOD)

        if (isinstance(listener, ISucceededListener) and
                (iface is None or issubclass(iface, ISucceededListener))):
            self.registerListener(SucceededEvent,
                    listener, _UPLOAD_SUCCEEDED_METHOD)

        super(Upload, self).addListener(listener, iface)


    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, FailedEvent):
            self.registerCallback(FailedEvent, callback, None, *args)

        elif issubclass(eventType, FinishedEvent):
            self.registerCallback(FinishedEvent, callback, None, *args)

        elif issubclass(eventType, IProgressListener):  # no progress event
            self._progressCallbacks[callback] = args

        elif issubclass(eventType, StartedEvent):
            self.registerCallback(StartedEvent, callback, None, *args)

        elif issubclass(eventType, SucceededEvent):
            self.registerCallback(SucceededEvent, callback, None, *args)

        else:
            super(Upload, self).addCallback(callback, eventType, *args)


    def removeListener(self, listener, iface=None):
        """Removes an event listener.

        @param listener:
                   the listener to be removed.
        """
        if (isinstance(listener, IFailedListener) and
                (iface is None or issubclass(iface, IFailedListener))):
            self.withdrawListener(FailedEvent,
                    listener, _UPLOAD_FAILED_METHOD)

        if (isinstance(listener, IFinishedListener) and
                (iface is None or issubclass(iface, IFinishedListener))):
            self.withdrawListener(FinishedEvent,
                    listener, _UPLOAD_FINISHED_METHOD)

        if (isinstance(listener, IProgressListener) and
                (iface is None or issubclass(iface, IProgressListener))):
            if listener in self._progressListeners:
                self._progressListeners.remove(listener)

        if (isinstance(listener, IStartedListener) and
                (iface is None or issubclass(iface, IStartedListener))):
            self.withdrawListener(StartedEvent,
                    listener, _UPLOAD_STARTED_METHOD)

        if (isinstance(listener, ISucceededListener) and
                (iface is None or issubclass(iface, ISucceededListener))):
            self.withdrawListener(SucceededEvent,
                    listener, _UPLOAD_SUCCEEDED_METHOD)

        super(Upload, self).removeListener(listener, iface)


    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType

        if issubclass(eventType, FailedEvent):
            self.withdrawCallback(FailedEvent, callback)

        elif issubclass(eventType, FinishedEvent):
            self.withdrawCallback(FinishedEvent, callback)

        elif issubclass(eventType, IProgressListener):  # no progress event
            if callback in self._progressCallbacks:
                del self._progressListeners[callback]

        elif issubclass(eventType, StartedEvent):
            self.withdrawCallback(StartedEvent, callback)

        elif issubclass(eventType, SucceededEvent):
            self.withdrawCallback(SucceededEvent, callback)

        else:
            super(Upload, self).removeCallback(callback, eventType)


    def fireStarted(self, filename, MIMEType):
        """Emit upload received event.
        """
        evt = StartedEvent(self, filename, MIMEType, self._contentLength)
        self.fireEvent(evt)


    def fireUploadInterrupted(self, filename, MIMEType, length, e=None):
        """Emits the upload failed event.
        """
        if e is None:
            evt = FailedEvent(self, filename, MIMEType, length)
        else:
            evt = FailedEvent(self, filename, MIMEType, length, e)

        self.fireEvent(evt)


    def fireNoInputStream(self, filename, MIMEType, length):
        evt = NoInputStreamEvent(self, filename, MIMEType, length)
        self.fireEvent(evt)


    def fireNoOutputStream(self, filename, MIMEType, length):
        evt = NoOutputStreamEvent(self, filename, MIMEType, length)
        self.fireEvent(evt)


    def fireUploadSuccess(self, filename, MIMEType, length):
        """Emits the upload success event.
        """
        evt = SucceededEvent(self, filename, MIMEType, length)
        self.fireEvent(evt)


    def fireUpdateProgress(self, totalBytes, contentLength):
        """Emits the progress event.

        @param totalBytes:
                   bytes received so far
        @param contentLength:
                   actual size of the file being uploaded, if known
        """
        # this is implemented differently than other listeners to
        # maintain backwards compatibility
        for l in self._progressListeners:
            l.updateProgress(totalBytes, contentLength)

        for callback, args in self._progressCallbacks.iteritems():
            callback(totalBytes, contentLength, *args)


    def getReceiver(self):
        """Returns the current receiver.

        @return: the IStreamVariable.
        """
        return self._receiver


    def setReceiver(self, receiver):
        """Sets the receiver.

        @param receiver:
                   the receiver to set.
        """
        self._receiver = receiver


    def focus(self):
        super(Upload, self).focus()


    def getTabIndex(self):
        """Gets the Tabulator index of this IFocusable component.

        @see: L{IFocusable.getTabIndex}
        """
        return self._tabIndex


    def setTabIndex(self, tabIndex):
        """Sets the Tabulator index of this IFocusable component.

        @see: L{IFocusable.setTabIndex}
        """
        self._tabIndex = tabIndex


    def startUpload(self):
        """Go into upload state. This is to prevent double uploading on same
        component.

        Warning: this is an internal method used by the framework and should
        not be used by user of the Upload component. Using it results in the
        Upload component going in wrong state and not working. It is currently
        public because it is used by another class.
        """
        if self._isUploading:
            raise ValueError, 'uploading already started'

        self._isUploading = True
        self._nextid += 1


    def interruptUpload(self):
        """Interrupts the upload currently being received. The interruption
        will be done by the receiving tread so this method will return
        immediately and the actual interrupt will happen a bit later.
        """
        if self._isUploading:
            self._interrupted = True


    def endUpload(self):
        """Go into state where new uploading can begin.

        Warning: this is an internal method used by the framework and should
        not be used by user of the Upload component.
        """
        self._isUploading = False
        self._contentLength = -1
        self._interrupted = False
        self.requestRepaint()


    def isUploading(self):
        return self._isUploading


    def getBytesRead(self):
        """Gets read bytes of the file currently being uploaded.

        @return: bytes
        """
        return self._totalBytes


    def getUploadSize(self):
        """Returns size of file currently being uploaded. Value sane only
        during upload.

        @return: size in bytes
        """
        return self._contentLength


    def setProgressListener(self, progressListener):
        """This method is deprecated, use addListener(IProgressListener)
        instead.

        @deprecated: Use addListener(IProgressListener) instead.
        """
        warn('use addListener() instead', DeprecationWarning)

        self.addListener(progressListener, IProgressListener)


    def getProgressListener(self):
        """This method is deprecated.

        @deprecated: Replaced with addListener/removeListener
        @return: listener
        """
        warn('replaced with addListener/removeListener', DeprecationWarning)

        if len(self._progressListeners) == 0:
            return None
        else:
            return iter(self._progressListeners).next()


    def getButtonCaption(self):
        """@return: String to be rendered into button that fires uploading"""
        return self._buttonCaption


    def setButtonCaption(self, buttonCaption):
        """In addition to the actual file chooser, upload components have
        button that starts actual upload progress. This method is used to set
        text in that button.

        In case the button text is set to null, the button is hidden. In this
        case developer must explicitly initiate the upload process with
        L{submitUpload}.

        In case the Upload is used in immediate mode using
        L{setImmediate}, the file choose (html input with type
        "file") is hidden and only the button with this text is shown.

        B{Note} the string given is set as is to the button.
        HTML formatting is not stripped. Be sure to properly validate your
        value according to your needs.

        @param buttonCaption:
                   text for upload components button.
        """
        self._buttonCaption = buttonCaption
        self.requestRepaint()


    def submitUpload(self):
        """Forces the upload the send selected file to the server.

        In case developer wants to use this feature, he/she will most probably
        want to hide the uploads internal submit button by setting its caption
        to null with L{setButtonCaption} method.

        Note, that the upload runs asynchronous. Developer should use normal
        upload listeners to trac the process of upload. If the field is empty
        uploaded the file name will be empty string and file length 0 in the
        upload finished event.

        Also note, that the developer should not remove or modify the upload
        in the same user transaction where the upload submit is requested. The
        upload may safely be hidden or removed once the upload started event
        is fired.
        """
        self.requestRepaint()
        self._forceSubmit = True


    def requestRepaint(self):
        self._forceSubmit = False
        super(Upload, self).requestRepaint()


    def getStreamVariable(self):
        # Handle to terminal via Upload monitors and controls the upload
        # during it is being streamed.
        if self._streamVariable is None:
            self._streamVariable = InnerStreamVariable(self)

        return self._streamVariable


    def getListeners(self, eventType):
        if issubclass(eventType, IStreamingEvent):
            return list(self._progressListeners)

        return super(Upload, self).getListeners(eventType)


    def getCallbacks(self, eventType):
        if issubclass(eventType, IStreamingEvent):
            return dict(self._progressCallbacks)

        return super(Upload, self).getCallbacks(eventType)


class InnerStreamVariable(IStreamVariable):

    def __init__(self, upload):
        self._upload = upload
        self._lastStartedEvent = None


    def listenProgress(self):
        return (self._upload.progressListeners is not None
                and len(self._upload.progressListeners) > 0)


    def onProgress(self, event):
        self._upload.fireUpdateProgress(event.getBytesReceived(),
                event.getContentLength())


    def isInterrupted(self):
        return self._upload.interrupted


    def getOutputStream(self):
        receiveUpload = self._upload.receiver.receiveUpload(
                self._lastStartedEvent.getFileName(),
                self._lastStartedEvent.getMimeType())
        self._lastStartedEvent = None
        return receiveUpload


    def streamingStarted(self, event):
        self.startUpload()
        self._upload.contentLength = event.getContentLength()
        self._upload.fireStarted(event.getFileName(),
                event.getMimeType())
        self._lastStartedEvent = event


    def streamingFinished(self, event):
        self._upload.fireUploadSuccess(event.getFileName(),
                event.getMimeType(), event.getContentLength())
        self._upload.endUpload()
        self._upload.requestRepaint()


    def streamingFailed(self, event):
        exception = event.getException()
        if isinstance(exception, NoInputStreamException):
            self._upload.fireNoInputStream(event.getFileName(),
                    event.getMimeType(), 0)

        elif isinstance(exception, NoOutputStreamException):
            self._upload.fireNoOutputStream(event.getFileName(),
                    event.getMimeType(), 0)
        else:
            self._upload.fireUploadInterrupted(event.getFileName(),
                    event.getMimeType(), 0, exception)

        self._upload.endUpload()


class IReceiver(object):
    """Interface that must be implemented by the upload receivers to provide
    the Upload component an output stream to write the uploaded data.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def receiveUpload(self, filename, mimeType):
        """Invoked when a new upload arrives.

        @param filename:
                   the desired filename of the upload, usually as specified
                   by the client.
        @param mimeType:
                   the MIME type of the uploaded file.
        @return: Stream to which the uploaded file should be written.
        """
        raise NotImplementedError


class FinishedEvent(ComponentEvent):
    """Upload.FinishedEvent is sent when the upload receives a file,
    regardless of whether the reception was successful or failed. If
    you wish to distinguish between the two cases, use either SucceededEvent
    or FailedEvent, which are both subclasses of the FinishedEvent.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source, filename, MIMEType, length):
        """@param source:
                   the source of the file.
        @param filename:
                   the received file name.
        @param MIMEType:
                   the MIME type of the received file.
        @param length:
                   the length of the received file.
        """
        super(FinishedEvent, self).__init__(source)

        #: MIME type of the received file.
        self._type = MIMEType

        #: Received file name.
        self._filename = filename

        #: Length of the received file.
        self._length = length


    def getUpload(self):
        """Uploads where the event occurred.

        @return: the source of the event.
        """
        return self.getSource()


    def getFilename(self):
        """Gets the file name.

        @return: the filename.
        """
        return self._filename


    def getMIMEType(self):
        """Gets the MIME Type of the file.

        @return: the MIME type.
        """
        return self._type


    def getLength(self):
        """Gets the length of the file.

        @return: the length.
        """
        return self._length


class FailedEvent(FinishedEvent):
    """Upload.FailedEvent event is sent when the upload is received,
    but the reception is interrupted for some reason.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source, filename, MIMEType, length, reason=None):
        super(FailedEvent, self).__init__(source, filename, MIMEType, length)

        self._reason = reason


    def getReason(self):
        """Gets the exception that caused the failure.

        @return: the exception that caused the failure, null if n/a
        """
        return self._reason


class NoOutputStreamEvent(FailedEvent):
    """FailedEvent that indicates that an output stream could not be obtained.
    """

    def __init__(self, source, filename, MIMEType, length):
        super(NoOutputStreamEvent, self).__init__(source, filename, MIMEType,
                length)


class NoInputStreamEvent(FailedEvent):
    """FailedEvent that indicates that an input stream could not be obtained.
    """

    def __init__(self, source, filename, MIMEType, length):
        super(NoInputStreamEvent, self).__init__(source, filename, MIMEType,
                length)


class SucceededEvent(FinishedEvent):
    """Upload.SucceededEvent event is sent when the upload is received
    successfully.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source, filename, MIMEType, length):
        super(SucceededEvent, self).__init__(source, filename, MIMEType, length)


class StartedEvent(ComponentEvent):
    """Upload.StartedEvent event is sent when the upload is started to
    received.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source, filename, MIMEType, contentLength):
        super(StartedEvent, self).__init__(source)

        self._filename = filename

        self._type = MIMEType

        #: Length of the received file.
        self._length = contentLength


    def getUpload(self):
        """Uploads where the event occurred.

        @return: the source of the event.
        """
        return self.getSource()


    def getFilename(self):
        """Gets the file name.

        @return: the filename.
        """
        return self._filename


    def getMIMEType(self):
        """Gets the MIME Type of the file.

        @return: the MIME type.
        """
        return self._type


    def getContentLength(self):
        """@return: the length of the file that is being uploaded"""
        return self._length
