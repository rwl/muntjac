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


class StreamVariable(object):
    """StreamVariable is a special kind of variable whose value is streamed to an
    {@link OutputStream} provided by the {@link #getOutputStream()} method. E.g.
    in web terminals {@link StreamVariable} can be used to send large files from
    browsers to the server without consuming large amounts of memory.
    <p>
    Note, writing to the {@link OutputStream} is not synchronized by the terminal
    (to avoid stalls in other operations when eg. streaming to a slow network
    service or file system). If UI is changed as a side effect of writing to the
    output stream, developer must handle synchronization manually.
    <p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 6.5
    @see PaintTarget#addVariable(VariableOwner, String, StreamVariable)
    """

    def getOutputStream(self):
        """Invoked by the terminal when a new upload arrives, after
        {@link #streamingStarted(StreamingStartEvent)} method has been called.
        The terminal implementation will write the streamed variable to the
        returned output stream.

        @return Stream to which the uploaded file should be written.
        """
        pass


    def listenProgress(self):
        """Whether the {@link #onProgress(long, long)} method should be called
        during the upload.
        <p>
        {@link #onProgress(long, long)} is called in a synchronized block when
        the content is being received. This is potentially bit slow, so we are
        calling that method only if requested. The value is requested after the
        {@link #uploadStarted(StreamingStartEvent)} event, but not after reading
        each buffer.

        @return true if this {@link StreamVariable} wants to by notified during
                the upload of the progress of streaming.
        @see #onProgress(StreamingProgressEvent)
        """
        pass


    def onProgress(self, event):
        """This method is called by the terminal if {@link #listenProgress()}
        returns true when the streaming starts.
        """
        pass


    def streamingStarted(self, event):
        pass


    def streamingFinished(self, event):
        pass


    def streamingFailed(self, event):
        # Not synchronized to avoid stalls (caused by UIDL requests) while
        # streaming the content. Implementations also most commonly atomic even
        # without the restriction.

        pass


    def isInterrupted(self):
        """If this method returns true while the content is being streamed the
        Terminal to stop receiving current upload.
        <p>
        Note, the usage of this method is not synchronized over the Application
        instance by the terminal like other methods. The implementation should
        only return a boolean field and especially not modify UI or implement a
        synchronization by itself.

        @return true if the streaming should be interrupted as soon as possible.
        """
        pass


class StreamingEvent(object):

    def getFileName(self):
        """@return the file name of the streamed file if known"""
        pass


    def getMimeType(self):
        """@return the mime type of the streamed file if known"""
        pass


    def getContentLength(self):
        """@return the length of the stream (in bytes) if known, else -1"""
        pass


    def getBytesReceived(self):
        """@return then number of bytes streamed to StreamVariable"""
        pass


class StreamingStartEvent(StreamingEvent):
    """Event passed to {@link #uploadStarted(StreamingStartEvent)} method before
    the streaming of the content to {@link StreamVariable} starts.
    """

    def disposeStreamVariable(self):
        """The owner of the StreamVariable can call this method to inform the
        terminal implementation that this StreamVariable will not be used to
        accept more post.
        """
        pass


class StreamingProgressEvent(StreamingEvent):
    """Event passed to {@link #onProgress(StreamingProgressEvent)} method during
    the streaming progresses.
    """
    pass


class StreamingEndEvent(StreamingEvent):
    """Event passed to {@link #uploadFinished(StreamingEndEvent)} method the
    contents have been streamed to StreamVariable successfully.
    """
    pass


class StreamingErrorEvent(StreamingEvent):
    """Event passed to {@link #uploadFailed(StreamingErrorEvent)} method when
    the streaming ended before the end of the input. The streaming may fail
    due an interruption by {@link } or due an other unknown exception in
    communication. In the latter case the exception is also passed to
    {@link Application#terminalError(com.vaadin.terminal.Terminal.ErrorEvent)}
    .
    """

    def getException(self):
        """@return the exception that caused the receiving not to finish cleanly"""
        pass
