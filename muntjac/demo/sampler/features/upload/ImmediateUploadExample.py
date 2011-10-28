
import time

from StringIO import StringIO

from muntjac.api import \
    (VerticalLayout, Label, ProgressIndicator, HorizontalLayout,
     Upload, Alignment, Button)

from muntjac.ui import button, upload


class ImmediateUploadExample(VerticalLayout):

    def __init__(self):
        super(ImmediateUploadExample, self).__init__()

        self.setSpacing(True)

        self._status = Label('Please select a file to upload')
        self._pi = ProgressIndicator()
        self._receiver = MyReceiver()
        self._progressLayout = HorizontalLayout()
        self._upload = Upload(None, self._receiver)

        # Slow down the upload
        self._receiver.setSlow(True)
        self.addComponent(self._status)
        self.addComponent(self._upload)
        self.addComponent(self._progressLayout)

        # Make uploading start immediately when file is selected
        self._upload.setImmediate(True)
        self._upload.setButtonCaption('Select file')

        self._progressLayout.setSpacing(True)
        self._progressLayout.setVisible(False)
        self._progressLayout.addComponent(self._pi)
        self._progressLayout.setComponentAlignment(self._pi,
                Alignment.MIDDLE_LEFT)

        cancelProcessing = Button('Cancel')
        cancelProcessing.addListener(CancelListener(self),
                button.IClickListener)
        cancelProcessing.setStyleName('small')
        self._progressLayout.addComponent(cancelProcessing)

        # =========== Add needed listener for the upload component: start,
        # progress, finish, success, fail ===========

        self._upload.addListener(StartedListener(self),
                upload.IStartedListener)

        self._upload.addListener(ProgressListener(self),
                upload.IProgressListener)

        self._upload.addListener(SucceededListener(self),
                upload.ISucceededListener)

        self._upload.addListener(FailedListener(self),
                upload.IFailedListener)

        self._upload.addListener(FinishedListener(self),
                upload.IFinishedListener)


class CancelListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._upload.interruptUpload()


class StartedListener(upload.IStartedListener):

    def __init__(self, c):
        self._c = c

    def uploadStarted(self, event):
        # This method gets called immediatedly after upload is started
        self._c._upload.setVisible(False)
        self._c._progressLayout.setVisible(True)
        self._c._pi.setValue(0.0)
        self._c._pi.setPollingInterval(500)
        self._c._status.setValue('Uploading file \"'
                + event.getFilename() + '\"')


class ProgressListener(upload.IProgressListener):

    def __init__(self, c):
        self._c = c

    def updateProgress(self, readBytes, contentLength):
        # This method gets called several times during the update
        self._c._pi.setValue(float(readBytes / contentLength))


class SucceededListener(upload.ISucceededListener):

    def __init__(self, c):
        self._c = c

    def uploadSucceeded(self, event):
        # This method gets called when the upload finished successfully
        self._c._status.setValue('Uploading file \"'
                + event.getFilename() + '\" succeeded')


class FailedListener(upload.IFailedListener):

    def __init__(self, c):
        self._c = c

    def uploadFailed(self, event):
        # This method gets called when the upload failed
        self._c._status.setValue('Uploading interrupted')


class FinishedListener(upload.IFinishedListener):

    def __init__(self, c):
        self._c = c

    def uploadFinished(self, event):
        # This method gets called always when the upload finished,
        # either succeeding or failing
        self._c._progressLayout.setVisible(False)
        self._c._upload.setVisible(True)
        self._c._upload.setCaption('Select another file')


class MyReceiver(upload.IReceiver):

    def __init__(self):
        self._fileName = None
        self._mtype = None
        self._sleep = None
        self._total = 0

    def receiveUpload(self, filename, mimetype):
        self._fileName = filename
        self._mtype = mimetype

        return UploadStream(self)

    def getFileName(self):
        return self._fileName

    def getMimeType(self):
        return self._mtype

    def setSlow(self, value):
        self._sleep = value


class UploadStream(StringIO):

    def __init__(self, r):
        super(UploadStream, self).__init__()
        self._r = r

    def write(self, b):
        self._r._total += 1
        if self._r._sleep and (self._r._total % 10000 == 0):
            time.sleep(100)
