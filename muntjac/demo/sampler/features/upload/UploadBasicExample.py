# -*- coding: utf-8 -*-


class UploadBasicExample(VerticalLayout):
    _result = ALabel()
    _counter = LineBreakCounter()
    _upload = Upload('Upload a file', _counter)

    def __init__(self):
        self.addComponent(self._upload)
        self.addComponent(self._result)

        class _0_(Upload.FinishedListener):

            def uploadFinished(self, event):
                UploadBasicExample_this._result.setValue('Uploaded file contained ' + UploadBasicExample_this._counter.getLineBreakCount() + ' linebreaks')

        _0_ = _0_()
        self._upload.addListener(_0_)

    class LineBreakCounter(Receiver):
        _fileName = None
        _mtype = None
        _counter = None

        def receiveUpload(self, filename, MIMEType):
            """return an OutputStream that simply counts lineends"""
            self._counter = 0
            self._fileName = filename
            self._mtype = MIMEType

            class _1_(OutputStream):
                _searchedByte = '\n'

                def write(self, b):
                    if b == self._searchedByte:
                        LineBreakCounter_this._counter += 1

            _1_ = _1_()
            return _1_

        def getFileName(self):
            return self._fileName

        def getMimeType(self):
            return self._mtype

        def getLineBreakCount(self):
            return self._counter
