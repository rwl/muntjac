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


class IStreamVariable(object):
    """IStreamVariable is a special kind of variable whose value is streamed
    to an {@link OutputStream} provided by the {@link #getOutputStream()}
    method. E.g. in web terminals {@link IStreamVariable} can be used to send
    large files from browsers to the server without consuming large amounts
    of memory.

    Note, writing to the {@link OutputStream} is not synchronized by the
    terminal (to avoid stalls in other operations when eg. streaming to a
    slow network service or file system). If UI is changed as a side effect
    of writing to the output stream, developer must handle synchronization
    manually.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 6.5
    @see PaintTarget#addVariable(VariableOwner, String, IStreamVariable)
    """

    def getOutputStream(self):
        """Invoked by the terminal when a new upload arrives, after
        {@link #streamingStarted(IStreamingStartEvent)} method has been called.
        The terminal implementation will write the streamed variable to the
        returned output stream.

        @return Stream to which the uploaded file should be written.
        """
        raise NotImplementedError


    def listenProgress(self):
        """Whether the {@link #onProgress(long, long)} method should be
        called during the upload.

        {@link #onProgress(long, long)} is called in a synchronized block
        when the content is being received. This is potentially bit slow,
        so we are calling that method only if requested. The value is
        requested after the {@link #uploadStarted(IStreamingStartEvent)}
        event, but not after reading each buffer.

        @return true if this {@link IStreamVariable} wants to by notified
                during the upload of the progress of streaming.
        @see #onProgress(IStreamingProgressEvent)
        """
        raise NotImplementedError


    def onProgress(self, event):
        """This method is called by the terminal if {@link #listenProgress()}
        returns true when the streaming starts.
        """
        raise NotImplementedError


    def streamingStarted(self, event):
        raise NotImplementedError


    def streamingFinished(self, event):
        raise NotImplementedError


    def streamingFailed(self, event):
        raise NotImplementedError


    def isInterrupted(self):
        """If this method returns true while the content is being streamed
        the Terminal to stop receiving current upload.

        Note, the usage of this method is not synchronized over the
        Application instance by the terminal like other methods. The
        implementation should only return a boolean field and especially
        not modify UI or implement a synchronization by itself.

        @return true if the streaming should be interrupted as soon as
                possible.
        """
        raise NotImplementedError


class IStreamingEvent(object):

    def getFileName(self):
        """@return the file name of the streamed file if known"""
        raise NotImplementedError


    def getMimeType(self):
        """@return the mime type of the streamed file if known"""
        raise NotImplementedError


    def getContentLength(self):
        """@return the length of the stream (in bytes) if known, else -1"""
        raise NotImplementedError


    def getBytesReceived(self):
        """@return then number of bytes streamed to IStreamVariable"""
        raise NotImplementedError


class IStreamingStartEvent(IStreamingEvent):
    """Event passed to {@link #uploadStarted(IStreamingStartEvent)} method
    before the streaming of the content to {@link IStreamVariable} starts.
    """

    def disposeStreamVariable(self):
        """The owner of the IStreamVariable can call this method to inform
        the terminal implementation that this IStreamVariable will not be
        used to accept more post.
        """
        raise NotImplementedError


class IStreamingProgressEvent(IStreamingEvent):
    """Event passed to {@link #onProgress(IStreamingProgressEvent)} method
    during the streaming progresses.
    """
    raise NotImplementedError


class IStreamingEndEvent(IStreamingEvent):
    """Event passed to {@link #uploadFinished(IStreamingEndEvent)} method
    the contents have been streamed to IStreamVariable successfully.
    """
    raise NotImplementedError


class IStreamingErrorEvent(IStreamingEvent):
    """Event passed to {@link #uploadFailed(IStreamingErrorEvent)} method
    when the streaming ended before the end of the input. The streaming may
    fail due an interruption by {@link } or due an other unknown exception
    in communication. In the latter case the exception is also passed to
    {@link Application#terminalError(event)}.
    """

    def getException(self):
        """@return the exception that caused the receiving not to finish
        cleanly"""
        raise NotImplementedError
