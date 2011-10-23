
from StringIO import StringIO

from muntjac.api import VerticalLayout, Label, upload
from muntjac.ui.upload import Upload, IReceiver


class UploadBasicExample(VerticalLayout):

    def __init__(self):
        self._result = Label()
        self._counter = LineBreakCounter()
        self._upload = Upload('Upload a file', self._counter)

        self.addComponent(self._upload)
        self.addComponent(self._result)

        class FinishedListener(upload.IFinishedListener):

            def __init__(self, c):
                self._c = c

            def uploadFinished(self, event):
                self._c._result.setValue('Uploaded file contained '
                    + self._c._counter.getLineBreakCount() + ' linebreaks')

        self._upload.addListener(FinishedListener(self))


class LineBreakCounter(IReceiver):

    def __init__(self):
        self._fileName = None
        self._mtype = None
        self._counter = None


    def receiveUpload(self, filename, MIMEType):
        """return an OutputStream that simply counts lineends"""
        self._counter = 0
        self._fileName = filename
        self._mtype = MIMEType

        class OutputStream(StringIO):

            def __init__(self, lbc):
                super(OutputStream, self).__init__()
                self._lbc = lbc

            def write(self, b):
                if b == '\n':
                    self._lbc._counter += 1

        return OutputStream(self)


    def getFileName(self):
        return self._fileName


    def getMimeType(self):
        return self._mtype


    def getLineBreakCount(self):
        return self._counter
