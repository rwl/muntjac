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

"""A special kind of variable whose value is streamed."""


class IStreamVariable(object):
    """IStreamVariable is a special kind of variable whose value is streamed
    to an L{StringIO} provided by the L{getOutputStream} method. E.g. in web
    terminals L{IStreamVariable} can be used to send large files from browsers
    to the server without consuming large amounts of memory.

    Note, writing to the L{OutputStream} is not synchronized by the
    terminal (to avoid stalls in other operations when eg. streaming to a
    slow network service or file system). If UI is changed as a side effect
    of writing to the output stream, developer must handle synchronization
    manually.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    @see: L{PaintTarget.addVariable}
    """

    def getOutputStream(self):
        """Invoked by the terminal when a new upload arrives, after
        L{streamingStarted} method has been called.
        The terminal implementation will write the streamed variable to the
        returned output stream.

        @return: Stream to which the uploaded file should be written.
        """
        raise NotImplementedError


    def listenProgress(self):
        """Whether the L{onProgress} method should be called during the upload.

        L{onProgress} is called in a synchronized block
        when the content is being received. This is potentially bit slow,
        so we are calling that method only if requested. The value is
        requested after the L{uploadStarted} event, but not after reading each
        buffer.

        @return: true if this L{IStreamVariable} wants to by notified
                during the upload of the progress of streaming.
        @see: L{onProgress}
        """
        raise NotImplementedError


    def onProgress(self, event):
        """This method is called by the terminal if L{listenProgress}
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

        @return: true if the streaming should be interrupted as soon as
                possible.
        """
        raise NotImplementedError


class IStreamingEvent(object):

    def getFileName(self):
        """@return: the file name of the streamed file if known"""
        raise NotImplementedError


    def getMimeType(self):
        """@return: the mime type of the streamed file if known"""
        raise NotImplementedError


    def getContentLength(self):
        """@return: the length of the stream (in bytes) if known, else -1"""
        raise NotImplementedError


    def getBytesReceived(self):
        """@return: then number of bytes streamed to IStreamVariable"""
        raise NotImplementedError


class IStreamingStartEvent(IStreamingEvent):
    """Event passed to L{uploadStarted} method before the streaming of the
    content to L{IStreamVariable} starts.
    """

    def disposeStreamVariable(self):
        """The owner of the IStreamVariable can call this method to inform
        the terminal implementation that this IStreamVariable will not be
        used to accept more post.
        """
        raise NotImplementedError


class IStreamingProgressEvent(IStreamingEvent):
    """Event passed to L{onProgress} method during the streaming progresses.
    """
    pass


class IStreamingEndEvent(IStreamingEvent):
    """Event passed to L{uploadFinished} method the contents have been
    streamed to IStreamVariable successfully.
    """
    pass


class IStreamingErrorEvent(IStreamingEvent):
    """Event passed to L{uploadFailed} method
    when the streaming ended before the end of the input. The streaming may
    fail due an interruption by [] or due an other unknown exception
    in communication. In the latter case the exception is also passed to
    L{Application.terminalError}.
    """

    def getException(self):
        """@return: the exception that caused the receiving not to finish
        cleanly"""
        raise NotImplementedError
