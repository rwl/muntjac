
from StringIO import StringIO

from muntjac.api import VerticalLayout, Label
from muntjac.ui.upload import Upload, IReceiver, IFinishedListener


class UploadBasicExample(VerticalLayout):

    def __init__(self):
        super(UploadBasicExample, self).__init__()

        self._result = Label()
        self._counter = LineBreakCounter()

        self._upload = Upload('Upload a file', self._counter)

        self.addComponent(self._upload)
        self.addComponent(self._result)

        self._upload.addListener(FinishedListener(self), IFinishedListener)


class FinishedListener(IFinishedListener):

    def __init__(self, c):
        self._c = c

    def uploadFinished(self, event):
        self._c._result.setValue('Uploaded file contained '
            + self._c._counter.getLineBreakCount() + ' linebreaks')


class LineBreakCounter(IReceiver):

    def __init__(self):
        self._fileName = None
        self._mtype = None
        self._counter = None


    def receiveUpload(self, filename, MIMEType):
        """return an OutputStream that simply counts line ends"""
        self._counter = 0
        self._fileName = filename
        self._mtype = MIMEType

        return OutputStream(self)


    def getFileName(self):
        return self._fileName


    def getMimeType(self):
        return self._mtype


    def getLineBreakCount(self):
        return self._counter


class OutputStream(StringIO):

    def __init__(self, lbc):
        super(OutputStream, self).__init__()
        self._lbc = lbc

    def write(self, b):
        if b == '\n':
            self._lbc._counter += 1
