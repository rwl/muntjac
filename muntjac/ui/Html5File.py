# -*- coding: utf-8 -*-
# from java.io.Serializable import (Serializable,)


class Html5File(Serializable):
    """{@link DragAndDropWrapper} can receive also files from client computer if
    appropriate HTML 5 features are supported on client side. This class wraps
    information about dragged file on server side.
    """
    _name = None
    _size = None
    _streamVariable = None
    _type = None

    def __init__(self, name, size, mimeType):
        self._name = name
        self._size = size
        self._type = mimeType

    def getFileName(self):
        return self._name

    def getFileSize(self):
        return self._size

    def getType(self):
        return self._type

    def setStreamVariable(self, streamVariable):
        """Sets the {@link StreamVariable} that into which the file contents will be
        written. Usage of StreamVariable is similar to {@link Upload} component.
        <p>
        If the {@link StreamVariable} is not set in the {@link DropHandler} the file
        contents will not be sent to server.
        <p>
        <em>Note!</em> receiving file contents is experimental feature depending
        on HTML 5 API's. It is supported only by modern web browsers like Firefox
        3.6 and above and recent webkit based browsers (Safari 5, Chrome 6) at
        this time.

        @param streamVariable
                   the callback that returns stream where the implementation
                   writes the file contents as it arrives.
        """
        self._streamVariable = streamVariable

    def getStreamVariable(self):
        return self._streamVariable
