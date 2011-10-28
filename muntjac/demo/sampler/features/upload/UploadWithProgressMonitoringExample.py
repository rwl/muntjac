
import time

from StringIO import StringIO

from muntjac.api import \
    (VerticalLayout, Label, ProgressIndicator, Upload, CheckBox,
     Button, Panel, FormLayout, HorizontalLayout)

from muntjac.ui import button, upload


class UploadWithProgressMonitoringExample(VerticalLayout):

    def __init__(self):
        super(UploadWithProgressMonitoringExample, self).__init__()

        self.setSpacing(True)

        self._state = Label()
        self._result = Label()
        self._fileName = Label()
        self._textualProgress = Label()
        self._pi = ProgressIndicator()
        self._counter = LineBreakCounter()
        self._upload = Upload(None, self._counter)

        self.addComponent(Label('Upload a file and we\'ll count the number '
                'of line break characters (\\n) found in it.'))

        # make analyzing start immediatedly when file is selected
        self._upload.setImmediate(True)
        self._upload.setButtonCaption('Upload File')
        self.addComponent(self._upload)

        handBrake = CheckBox('Simulate slow server')
        handBrake.setValue(True)
        self._counter.setSlow(True)
        handBrake.setDescription('Sleep for 100ms after each kilobyte to '
                'simulate slower processing/bandwidth. This is to show '
                'progress indicator even with rather small files.')
        handBrake.addListener(HandBrakeListener(self), button.IClickListener)

        cancelProcessing = Button('Cancel')
        cancelProcessing.addListener(CancelListener(self),
                button.IClickListener)
        cancelProcessing.setVisible(False)
        cancelProcessing.setStyleName('small')

        handBrake.setImmediate(True)
        self.addComponent(handBrake)

        p = Panel('Status')
        p.setSizeUndefined()

        l = FormLayout()
        l.setMargin(True)
        p.setContent(l)

        stateLayout = HorizontalLayout()
        stateLayout.setSpacing(True)
        stateLayout.addComponent(self._state)
        stateLayout.addComponent(cancelProcessing)
        stateLayout.setCaption('Current state')
        self._state.setValue('Idle')
        l.addComponent(stateLayout)

        self._fileName.setCaption('File name')
        l.addComponent(self._fileName)

        self._result.setCaption('Line breaks counted')
        l.addComponent(self._result)

        self._pi.setCaption('Progress')
        self._pi.setVisible(False)
        l.addComponent(self._pi)
        self._textualProgress.setVisible(False)
        l.addComponent(self._textualProgress)

        self.addComponent(p)

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


class HandBrakeListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._counter.setSlow(bool(event.getButton()))


class CancelListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._upload.interruptUpload()


class StartedListener(upload.IStartedListener):

    def __init__(self, c):
        self._c = c

    def uploadStarted(self, event):
        # this method gets called immediatedly after upload is
        # started
        self._c._pi.setValue(0.0)
        self._c._pi.setVisible(True)
        self._c._pi.setPollingInterval(500)
        # hit server frequantly to get
        self._c._textualProgress.setVisible(True)
        # updates to client
        self._c._state.setValue('Uploading')
        self._c._fileName.setValue(event.getFilename())
        self.cancelProcessing.setVisible(True)


class ProgressListener(upload.IProgressListener):

    def __init__(self, c):
        self._c = c

    def updateProgress(self, readBytes, contentLength):
        # this method gets called several times during the update
        self._c._pi.setValue(float(readBytes / contentLength))
        self._c._textualProgress.setValue('Processed ' + readBytes
                + ' bytes of ' + contentLength)
        self._c._result.setValue(self._c._counter.getLineBreakCount()
                + ' (counting...)')


class SucceededListener(upload.ISucceededListener):

    def __init__(self, c):
        self._c = c

    def uploadSucceeded(self, event):
        self._c._result.setValue(self._c._counter.getLineBreakCount()
                + ' (total)')


class FailedListener(upload.IFailedListener):

    def __init__(self, c):
        self._c = c

    def uploadFailed(self, event):
        self._c._result.setValue(self._c._counter.getLineBreakCount()
                + ' (counting interrupted at '
                + round(100 * self._c._pi.getValue()) + '%)')


class FinishedListener(upload.IFinishedListener):

    def __init__(self, c):
        self._c = c

    def uploadFinished(self, event):
        self._c._state.setValue('Idle')
        self._c._pi.setVisible(False)
        self._c._textualProgress.setVisible(False)
        self.cancelProcessing.setVisible(False)


class LineBreakCounter(upload.IReceiver):

    def __init__(self):
        self._fileName = None
        self._mtype = None
        self._counter = None
        self._total = None
        self._sleep = None


    def receiveUpload(self, filename, MIMEType):
        """return an OutputStream that simply counts lineends"""
        self._counter = 0
        self._total = 0
        self._fileName = filename
        self._mtype = MIMEType

        return OutputStream()


    def getFileName(self):
        return self._fileName


    def getMimeType(self):
        return self._mtype


    def getLineBreakCount(self):
        return self._counter


    def setSlow(self, value):
        self._sleep = value


class OutputStream(StringIO):

    def __init__(self, c):
        self._c = c

    def write(self, b):
        self._c._total += 1
        if b == '\n':
            self._c._counter += 1
        if self._c._sleep and self._c._total % 1000 == 0:
            time.sleep(100)
