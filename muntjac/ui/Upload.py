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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.Component import (Component,)
from com.vaadin.ui.AbstractComponent import (AbstractComponent,)
# from com.vaadin.terminal.StreamVariable.StreamingProgressEvent import (StreamingProgressEvent,)
# from java.io.OutputStream import (OutputStream,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.util.Collections import (Collections,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.Map import (Map,)


class Upload(AbstractComponent, Component, Focusable):
    """Component for uploading files from client to server.

    <p>
    The visible component consists of a file name input box and a browse button
    and an upload submit button to start uploading.

    <p>
    The Upload component needs a java.io.OutputStream to write the uploaded data.
    You need to implement the Upload.Receiver interface and return the output
    stream in the receiveUpload() method.

    <p>
    You can get an event regarding starting (StartedEvent), progress
    (ProgressEvent), and finishing (FinishedEvent) of upload by implementing
    StartedListener, ProgressListener, and FinishedListener, respectively. The
    FinishedListener is called for both failed and succeeded uploads. If you wish
    to separate between these two cases, you can use SucceededListener
    (SucceededEvenet) and FailedListener (FailedEvent).

    <p>
    The upload component does not itself show upload progress, but you can use
    the ProgressIndicator for providing progress feedback by implementing
    ProgressListener and updating the indicator in updateProgress().

    <p>
    Setting upload component immediate initiates the upload as soon as a file is
    selected, instead of the common pattern of file selection field and upload
    button.

    <p>
    Note! Because of browser dependent implementations of <input type="file">
    element, setting size for Upload component is not supported. For some
    browsers setting size may work to some extend.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Should the field be focused on next repaint?
    _focus = False
    # The tab order number of this field.
    _tabIndex = 0
    # The output of the upload is redirected to this receiver.
    _receiver = None
    _isUploading = None
    _contentLength = -1
    _totalBytes = None
    _buttonCaption = 'Upload'
    # ProgressListeners to which information about progress is sent during
    # upload

    _progressListeners = None
    _interrupted = False
    _notStarted = None
    _nextid = None
    # Flag to indicate that submitting file has been requested.
    _forceSubmit = None

    def __init__(self, *args):
        """Creates a new instance of Upload.

        The receiver must be set before performing an upload.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 2:
            caption, uploadReceiver = _0
            self.setCaption(caption)
            self._receiver = uploadReceiver
        else:
            raise ARGERROR(0, 2)

    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see com.vaadin.ui.AbstractComponent#changeVariables(java.lang.Object,
             java.util.Map)
        """
        if 'pollForStart' in variables:
            id = variables['pollForStart']
            if not self._isUploading and id == self._nextid:
                self._notStarted = True
                self.requestRepaint()
            else:
                pass

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   Target to paint the content on.
        @throws PaintException
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

    class Receiver(Serializable):
        """Interface that must be implemented by the upload receivers to provide the
        Upload component an output stream to write the uploaded data.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        # Upload events

        def receiveUpload(self, filename, mimeType):
            """Invoked when a new upload arrives.

            @param filename
                       the desired filename of the upload, usually as specified
                       by the client.
            @param mimeType
                       the MIME type of the uploaded file.
            @return Stream to which the uploaded file should be written.
            """
            pass

    _UPLOAD_FINISHED_METHOD = None
    _UPLOAD_FAILED_METHOD = None
    _UPLOAD_SUCCEEDED_METHOD = None
    _UPLOAD_STARTED_METHOD = None
    # This should never happen
    try:
        _UPLOAD_FINISHED_METHOD = self.FinishedListener.getDeclaredMethod('uploadFinished', [self.FinishedEvent])
        _UPLOAD_FAILED_METHOD = self.FailedListener.getDeclaredMethod('uploadFailed', [self.FailedEvent])
        _UPLOAD_STARTED_METHOD = self.StartedListener.getDeclaredMethod('uploadStarted', [self.StartedEvent])
        _UPLOAD_SUCCEEDED_METHOD = self.SucceededListener.getDeclaredMethod('uploadSucceeded', [self.SucceededEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error finding methods in Upload')

    class FinishedEvent(Component.Event):
        """Upload.FinishedEvent is sent when the upload receives a file, regardless
        of whether the reception was successful or failed. If you wish to
        distinguish between the two cases, use either SucceededEvent or
        FailedEvent, which are both subclasses of the FinishedEvent.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        # Length of the received file.
        _length = None
        # MIME type of the received file.
        _type = None
        # Received file name.
        _filename = None

        def __init__(self, source, filename, MIMEType, length):
            """@param source
                       the source of the file.
            @param filename
                       the received file name.
            @param MIMEType
                       the MIME type of the received file.
            @param length
                       the length of the received file.
            """
            super(FinishedEvent, self)(source)
            self._type = MIMEType
            self._filename = filename
            self._length = length

        def getUpload(self):
            """Uploads where the event occurred.

            @return the Source of the event.
            """
            return self.getSource()

        def getFilename(self):
            """Gets the file name.

            @return the filename.
            """
            return self._filename

        def getMIMEType(self):
            """Gets the MIME Type of the file.

            @return the MIME type.
            """
            return self._type

        def getLength(self):
            """Gets the length of the file.

            @return the length.
            """
            return self._length

    class FailedEvent(FinishedEvent):
        """Upload.FailedEvent event is sent when the upload is received, but the
        reception is interrupted for some reason.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        _reason = None

        def __init__(self, *args):
            """@param source
            @param filename
            @param MIMEType
            @param length
            @param exception
            ---
            @param source
            @param filename
            @param MIMEType
            @param length
            @param exception
            """
            _0 = args
            _1 = len(args)
            if _1 == 4:
                source, filename, MIMEType, length = _0
                super(FailedEvent, self)(source, filename, MIMEType, length)
            elif _1 == 5:
                source, filename, MIMEType, length, reason = _0
                self.__init__(source, filename, MIMEType, length)
                self._reason = reason
            else:
                raise ARGERROR(4, 5)

        def getReason(self):
            """Gets the exception that caused the failure.

            @return the exception that caused the failure, null if n/a
            """
            return self._reason

    class NoOutputStreamEvent(FailedEvent):
        """FailedEvent that indicates that an output stream could not be obtained."""

        def __init__(self, source, filename, MIMEType, length):
            """@param source
            @param filename
            @param MIMEType
            @param length
            """
            super(NoOutputStreamEvent, self)(source, filename, MIMEType, length)

    class NoInputStreamEvent(FailedEvent):
        """FailedEvent that indicates that an input stream could not be obtained."""

        def __init__(self, source, filename, MIMEType, length):
            """@param source
            @param filename
            @param MIMEType
            @param length
            """
            super(NoInputStreamEvent, self)(source, filename, MIMEType, length)

    class SucceededEvent(FinishedEvent):
        """Upload.SucceededEvent event is sent when the upload is received
        successfully.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """

        def __init__(self, source, filename, MIMEType, length):
            """@param source
            @param filename
            @param MIMEType
            @param length
            """
            super(SucceededEvent, self)(source, filename, MIMEType, length)

    class StartedEvent(Component.Event):
        """Upload.StartedEvent event is sent when the upload is started to received.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 5.0
        """
        _filename = None
        _type = None
        # Length of the received file.
        _length = None

        def __init__(self, source, filename, MIMEType, contentLength):
            """@param source
            @param filename
            @param MIMEType
            @param length
            """
            super(StartedEvent, self)(source)
            self._filename = filename
            self._type = MIMEType
            self._length = contentLength

        def getUpload(self):
            """Uploads where the event occurred.

            @return the Source of the event.
            """
            return self.getSource()

        def getFilename(self):
            """Gets the file name.

            @return the filename.
            """
            return self._filename

        def getMIMEType(self):
            """Gets the MIME Type of the file.

            @return the MIME type.
            """
            return self._type

        def getContentLength(self):
            """@return the length of the file that is being uploaded"""
            return self._length

    class StartedListener(Serializable):
        """Receives the events when the upload starts.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 5.0
        """

        def uploadStarted(self, event):
            """Upload has started.

            @param event
                       the Upload started event.
            """
            pass

    class FinishedListener(Serializable):
        """Receives the events when the uploads are ready.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """

        def uploadFinished(self, event):
            """Upload has finished.

            @param event
                       the Upload finished event.
            """
            pass

    class FailedListener(Serializable):
        """Receives events when the uploads are finished, but unsuccessful.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """

        def uploadFailed(self, event):
            """Upload has finished unsuccessfully.

            @param event
                       the Upload failed event.
            """
            pass

    class SucceededListener(Serializable):
        """Receives events when the uploads are successfully finished.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """

        def uploadSucceeded(self, event):
            """Upload successfull..

            @param event
                       the Upload successfull event.
            """
            pass

    def addListener(self, *args):
        """Adds the upload started event listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the upload received event listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the upload interrupted event listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the upload success event listener.

        @param listener
                   the Listener to be added.
        ---
        Adds the upload success event listener.

        @param listener
                   the Listener to be added.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], FailedListener):
                listener, = _0
                self.addListener(self.FailedEvent, listener, self._UPLOAD_FAILED_METHOD)
            elif isinstance(_0[0], FinishedListener):
                listener, = _0
                self.addListener(self.FinishedEvent, listener, self._UPLOAD_FINISHED_METHOD)
            elif isinstance(_0[0], ProgressListener):
                listener, = _0
                if self._progressListeners is None:
                    self._progressListeners = LinkedHashSet()
                self._progressListeners.add(listener)
            elif isinstance(_0[0], StartedListener):
                listener, = _0
                self.addListener(self.StartedEvent, listener, self._UPLOAD_STARTED_METHOD)
            else:
                listener, = _0
                self.addListener(self.SucceededEvent, listener, self._UPLOAD_SUCCEEDED_METHOD)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Removes the upload started event listener.

        @param listener
                   the Listener to be removed.
        ---
        Removes the upload received event listener.

        @param listener
                   the Listener to be removed.
        ---
        Removes the upload interrupted event listener.

        @param listener
                   the Listener to be removed.
        ---
        Removes the upload success event listener.

        @param listener
                   the Listener to be removed.
        ---
        Removes the upload success event listener.

        @param listener
                   the Listener to be removed.
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], FailedListener):
                listener, = _0
                self.removeListener(self.FailedEvent, listener, self._UPLOAD_FAILED_METHOD)
            elif isinstance(_0[0], FinishedListener):
                listener, = _0
                self.removeListener(self.FinishedEvent, listener, self._UPLOAD_FINISHED_METHOD)
            elif isinstance(_0[0], ProgressListener):
                listener, = _0
                if self._progressListeners is not None:
                    self._progressListeners.remove(listener)
            elif isinstance(_0[0], StartedListener):
                listener, = _0
                self.removeListener(self.StartedEvent, listener, self._UPLOAD_STARTED_METHOD)
            else:
                listener, = _0
                self.removeListener(self.SucceededEvent, listener, self._UPLOAD_SUCCEEDED_METHOD)
        else:
            raise ARGERROR(1, 1)

    def fireStarted(self, filename, MIMEType):
        """Emit upload received event.

        @param filename
        @param MIMEType
        @param length
        """
        self.fireEvent(Upload.StartedEvent(self, filename, MIMEType, self._contentLength))

    def fireUploadInterrupted(self, *args):
        """Emits the upload failed event.

        @param filename
        @param MIMEType
        @param length
        """
        _0 = args
        _1 = len(args)
        if _1 == 3:
            filename, MIMEType, length = _0
            self.fireEvent(Upload.FailedEvent(self, filename, MIMEType, length))
        elif _1 == 4:
            filename, MIMEType, length, e = _0
            self.fireEvent(Upload.FailedEvent(self, filename, MIMEType, length, e))
        else:
            raise ARGERROR(3, 4)

    def fireNoInputStream(self, filename, MIMEType, length):
        self.fireEvent(Upload.NoInputStreamEvent(self, filename, MIMEType, length))

    def fireNoOutputStream(self, filename, MIMEType, length):
        self.fireEvent(Upload.NoOutputStreamEvent(self, filename, MIMEType, length))

    def fireUploadSuccess(self, filename, MIMEType, length):
        """Emits the upload success event.

        @param filename
        @param MIMEType
        @param length
        """
        self.fireEvent(Upload.SucceededEvent(self, filename, MIMEType, length))

    def fireUpdateProgress(self, totalBytes, contentLength):
        """Emits the progress event.

        @param totalBytes
                   bytes received so far
        @param contentLength
                   actual size of the file being uploaded, if known
        """
        # this is implemented differently than other listeners to maintain
        # backwards compatibility
        if self._progressListeners is not None:
            _0 = True
            it = self._progressListeners
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                l = it.next()
                l.updateProgress(totalBytes, contentLength)

    def getReceiver(self):
        """Returns the current receiver.

        @return the StreamVariable.
        """
        return self._receiver

    def setReceiver(self, receiver):
        """Sets the receiver.

        @param receiver
                   the receiver to set.
        """
        self._receiver = receiver

    def focus(self):
        """{@inheritDoc}"""
        super(Upload, self).focus()

    def getTabIndex(self):
        """Gets the Tabulator index of this Focusable component.

        @see com.vaadin.ui.Component.Focusable#getTabIndex()
        """
        return self._tabIndex

    def setTabIndex(self, tabIndex):
        """Sets the Tabulator index of this Focusable component.

        @see com.vaadin.ui.Component.Focusable#setTabIndex(int)
        """
        self._tabIndex = tabIndex

    def startUpload(self):
        """Go into upload state. This is to prevent double uploading on same
        component.

        Warning: this is an internal method used by the framework and should not
        be used by user of the Upload component. Using it results in the Upload
        component going in wrong state and not working. It is currently public
        because it is used by another class.
        """
        if self._isUploading:
            raise self.IllegalStateException('uploading already started')
        self._isUploading = True
        self._nextid += 1

    def interruptUpload(self):
        """Interrupts the upload currently being received. The interruption will be
        done by the receiving tread so this method will return immediately and
        the actual interrupt will happen a bit later.
        """
        if self._isUploading:
            self._interrupted = True

    def endUpload(self):
        """Go into state where new uploading can begin.

        Warning: this is an internal method used by the framework and should not
        be used by user of the Upload component.
        """
        self._isUploading = False
        self._contentLength = -1
        self._interrupted = False
        self.requestRepaint()

    def isUploading(self):
        return self._isUploading

    def getBytesRead(self):
        """Gets read bytes of the file currently being uploaded.

        @return bytes
        """
        return self._totalBytes

    def getUploadSize(self):
        """Returns size of file currently being uploaded. Value sane only during
        upload.

        @return size in bytes
        """
        return self._contentLength

    def setProgressListener(self, progressListener):
        """This method is deprecated, use addListener(ProgressListener) instead.

        @deprecated Use addListener(ProgressListener) instead.
        @param progressListener
        """
        self.addListener(progressListener)

    def getProgressListener(self):
        """This method is deprecated.

        @deprecated Replaced with addListener/removeListener
        @return listener
        """
        if (self._progressListeners is None) or self._progressListeners.isEmpty():
            return None
        else:
            return self._progressListeners.next()

    class ProgressListener(Serializable):
        """ProgressListener receives events to track progress of upload."""

        def updateProgress(self, readBytes, contentLength):
            """Updates progress to listener

            @param readBytes
                       bytes transferred
            @param contentLength
                       total size of file currently being uploaded, -1 if unknown
            """
            pass

    def getButtonCaption(self):
        """@return String to be rendered into button that fires uploading"""
        return self._buttonCaption

    def setButtonCaption(self, buttonCaption):
        """In addition to the actual file chooser, upload components have button
        that starts actual upload progress. This method is used to set text in
        that button.
        <p>
        In case the button text is set to null, the button is hidden. In this
        case developer must explicitly initiate the upload process with
        {@link #submitUpload()}.
        <p>
        In case the Upload is used in immediate mode using
        {@link #setImmediate(boolean)}, the file choose (html input with type
        "file") is hidden and only the button with this text is shown.
        <p>

        <p>
        <strong>Note</strong> the string given is set as is to the button. HTML
        formatting is not stripped. Be sure to properly validate your value
        according to your needs.

        @param buttonCaption
                   text for upload components button.
        """
        self._buttonCaption = buttonCaption
        self.requestRepaint()

    def submitUpload(self):
        """Forces the upload the send selected file to the server.
        <p>
        In case developer wants to use this feature, he/she will most probably
        want to hide the uploads internal submit button by setting its caption to
        null with {@link #setButtonCaption(String)} method.
        <p>
        Note, that the upload runs asynchronous. Developer should use normal
        upload listeners to trac the process of upload. If the field is empty
        uploaded the file name will be empty string and file length 0 in the
        upload finished event.
        <p>
        Also note, that the developer should not remove or modify the upload in
        the same user transaction where the upload submit is requested. The
        upload may safely be hidden or removed once the upload started event is
        fired.
        """
        self.requestRepaint()
        self._forceSubmit = True

    def requestRepaint(self):
        # Handle to terminal via Upload monitors and controls the upload during it
        # is being streamed.

        self._forceSubmit = False
        super(Upload, self).requestRepaint()

    _streamVariable = None

    def getStreamVariable(self):
        if self._streamVariable is None:

            class _0_(com.vaadin.terminal.StreamVariable):
                _lastStartedEvent = None

                def listenProgress(self):
                    return self.progressListeners is not None and not self.progressListeners.isEmpty()

                def onProgress(self, event):
                    self.fireUpdateProgress(event.getBytesReceived(), event.getContentLength())

                def isInterrupted(self):
                    return self.interrupted

                def getOutputStream(self):
                    receiveUpload = self.receiver.receiveUpload(self._lastStartedEvent.getFileName(), self._lastStartedEvent.getMimeType())
                    self._lastStartedEvent = None
                    return receiveUpload

                def streamingStarted(self, event):
                    self.startUpload()
                    self.contentLength = event.getContentLength()
                    self.fireStarted(event.getFileName(), event.getMimeType())
                    self._lastStartedEvent = event

                def streamingFinished(self, event):
                    self.fireUploadSuccess(event.getFileName(), event.getMimeType(), event.getContentLength())
                    self.endUpload()
                    self.requestRepaint()

                def streamingFailed(self, event):
                    exception = event.getException()
                    if isinstance(exception, NoInputStreamException):
                        self.fireNoInputStream(event.getFileName(), event.getMimeType(), 0)
                    elif isinstance(exception, NoOutputStreamException):
                        self.fireNoOutputStream(event.getFileName(), event.getMimeType(), 0)
                    else:
                        self.fireUploadInterrupted(event.getFileName(), event.getMimeType(), 0, exception)
                    self.endUpload()

            _0_ = self._0_()
            self._streamVariable = _0_
        return self._streamVariable

    def getListeners(self, eventType):
        if StreamingProgressEvent.isAssignableFrom(eventType):
            if self._progressListeners is None:
                return Collections.EMPTY_LIST
            else:
                return Collections.unmodifiableCollection(self._progressListeners)
        return super(Upload, self).getListeners(eventType)
