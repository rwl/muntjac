# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.upload.UploadBasicExample import (UploadBasicExample,)
# from com.vaadin.ui.CheckBox import (CheckBox,)
# from com.vaadin.ui.FormLayout import (FormLayout,)
LineBreakCounter = UploadBasicExample.LineBreakCounter


class UploadWithProgressMonitoringExample(VerticalLayout):
    _state = ALabel()
    _result = ALabel()
    _fileName = ALabel()
    _textualProgress = ALabel()
    _pi = ProgressIndicator()
    _counter = LineBreakCounter()
    _upload = Upload(None, _counter)

    def __init__(self):
        self.setSpacing(True)
        self.addComponent(ALabel('Upload a file and we\'ll count the number of line break characters (\\n) found in it.'))
        # make analyzing start immediatedly when file is selected
        self._upload.setImmediate(True)
        self._upload.setButtonCaption('Upload File')
        self.addComponent(self._upload)
        handBrake = CheckBox('Simulate slow server')
        handBrake.setValue(True)
        self._counter.setSlow(True)
        handBrake.setDescription('Sleep for 100ms after each kilobyte to simulate slower processing/bandwidth. This is to show progress indicator even with rather small files.')

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                UploadWithProgressMonitoringExample_this._counter.setSlow(event.getButton().booleanValue())

        _0_ = _0_()
        handBrake.addListener(_0_)
        cancelProcessing = Button('Cancel')

        class _1_(Button.ClickListener):

            def buttonClick(self, event):
                UploadWithProgressMonitoringExample_this._upload.interruptUpload()

        _1_ = _1_()
        cancelProcessing.addListener(_1_)
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

        class _2_(Upload.StartedListener):

            def uploadStarted(self, event):
                # this method gets called immediatedly after upload is
                # started
                UploadWithProgressMonitoringExample_this._pi.setValue(0.0)
                UploadWithProgressMonitoringExample_this._pi.setVisible(True)
                UploadWithProgressMonitoringExample_this._pi.setPollingInterval(500)
                # hit server frequantly to get
                UploadWithProgressMonitoringExample_this._textualProgress.setVisible(True)
                # updates to client
                UploadWithProgressMonitoringExample_this._state.setValue('Uploading')
                UploadWithProgressMonitoringExample_this._fileName.setValue(event.getFilename())
                self.cancelProcessing.setVisible(True)

        _2_ = _2_()
        self._upload.addListener(_2_)

        class _3_(Upload.ProgressListener):

            def updateProgress(self, readBytes, contentLength):
                # this method gets called several times during the update
                UploadWithProgressMonitoringExample_this._pi.setValue(float(readBytes / contentLength))
                UploadWithProgressMonitoringExample_this._textualProgress.setValue('Processed ' + readBytes + ' bytes of ' + contentLength)
                UploadWithProgressMonitoringExample_this._result.setValue(UploadWithProgressMonitoringExample_this._counter.getLineBreakCount() + ' (counting...)')

        _3_ = _3_()
        self._upload.addListener(_3_)

        class _4_(Upload.SucceededListener):

            def uploadSucceeded(self, event):
                UploadWithProgressMonitoringExample_this._result.setValue(UploadWithProgressMonitoringExample_this._counter.getLineBreakCount() + ' (total)')

        _4_ = _4_()
        self._upload.addListener(_4_)

        class _5_(Upload.FailedListener):

            def uploadFailed(self, event):
                UploadWithProgressMonitoringExample_this._result.setValue(UploadWithProgressMonitoringExample_this._counter.getLineBreakCount() + ' (counting interrupted at ' + self.Math.round(100 * UploadWithProgressMonitoringExample_this._pi.getValue()) + '%)')

        _5_ = _5_()
        self._upload.addListener(_5_)

        class _6_(Upload.FinishedListener):

            def uploadFinished(self, event):
                UploadWithProgressMonitoringExample_this._state.setValue('Idle')
                UploadWithProgressMonitoringExample_this._pi.setVisible(False)
                UploadWithProgressMonitoringExample_this._textualProgress.setVisible(False)
                self.cancelProcessing.setVisible(False)

        _6_ = _6_()
        self._upload.addListener(_6_)

    class LineBreakCounter(Receiver):
        _fileName = None
        _mtype = None
        _counter = None
        _total = None
        _sleep = None

        def receiveUpload(self, filename, MIMEType):
            """return an OutputStream that simply counts lineends"""
            self._counter = 0
            self._total = 0
            self._fileName = filename
            self._mtype = MIMEType

            class _7_(OutputStream):
                _searchedByte = '\n'

                def write(self, b):
                    LineBreakCounter_this._total += 1
                    if b == self._searchedByte:
                        LineBreakCounter_this._counter += 1
                    if LineBreakCounter_this._sleep and LineBreakCounter_this._total % 1000 == 0:
                        # TODO Auto-generated catch block
                        try:
                            self.Thread.sleep(100)
                        except self.InterruptedException, e:
                            e.printStackTrace()

            _7_ = _7_()
            return _7_

        def getFileName(self):
            return self._fileName

        def getMimeType(self):
            return self._mtype

        def getLineBreakCount(self):
            return self._counter

        def setSlow(self, value):
            self._sleep = value
