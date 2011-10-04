# -*- coding: utf-8 -*-
# from com.vaadin.ui.Upload.FailedEvent import (FailedEvent,)
# from com.vaadin.ui.Upload.FinishedEvent import (FinishedEvent,)
# from com.vaadin.ui.Upload.Receiver import (Receiver,)
# from com.vaadin.ui.Upload.StartedEvent import (StartedEvent,)
# from com.vaadin.ui.Upload.SucceededEvent import (SucceededEvent,)
# from java.io.IOException import (IOException,)
# from java.io.OutputStream import (OutputStream,)


class ImmediateUploadExample(VerticalLayout):
    _status = Label('Please select a file to upload')
    _pi = ProgressIndicator()
    _receiver = MyReceiver()
    _progressLayout = HorizontalLayout()
    _upload = Upload(None, _receiver)

    def __init__(self):
        self.setSpacing(True)
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
        self._progressLayout.setComponentAlignment(self._pi, Alignment.MIDDLE_LEFT)
        cancelProcessing = Button('Cancel')

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                ImmediateUploadExample_this._upload.interruptUpload()

        _0_ = _0_()
        cancelProcessing.addListener(_0_)
        cancelProcessing.setStyleName('small')
        self._progressLayout.addComponent(cancelProcessing)
        # =========== Add needed listener for the upload component: start,
        # progress, finish, success, fail ===========

        class _1_(Upload.StartedListener):

            def uploadStarted(self, event):
                # This method gets called immediatedly after upload is started
                ImmediateUploadExample_this._upload.setVisible(False)
                ImmediateUploadExample_this._progressLayout.setVisible(True)
                ImmediateUploadExample_this._pi.setValue(0.0)
                ImmediateUploadExample_this._pi.setPollingInterval(500)
                ImmediateUploadExample_this._status.setValue('Uploading file \"' + event.getFilename() + '\"')

        _1_ = _1_()
        self._upload.addListener(_1_)

        class _2_(Upload.ProgressListener):

            def updateProgress(self, readBytes, contentLength):
                # This method gets called several times during the update
                ImmediateUploadExample_this._pi.setValue(float(readBytes / contentLength))

        _2_ = _2_()
        self._upload.addListener(_2_)

        class _3_(Upload.SucceededListener):

            def uploadSucceeded(self, event):
                # This method gets called when the upload finished successfully
                ImmediateUploadExample_this._status.setValue('Uploading file \"' + event.getFilename() + '\" succeeded')

        _3_ = _3_()
        self._upload.addListener(_3_)

        class _4_(Upload.FailedListener):

            def uploadFailed(self, event):
                # This method gets called when the upload failed
                ImmediateUploadExample_this._status.setValue('Uploading interrupted')

        _4_ = _4_()
        self._upload.addListener(_4_)

        class _5_(Upload.FinishedListener):

            def uploadFinished(self, event):
                # This method gets called always when the upload finished,
                # either succeeding or failing
                ImmediateUploadExample_this._progressLayout.setVisible(False)
                ImmediateUploadExample_this._upload.setVisible(True)
                ImmediateUploadExample_this._upload.setCaption('Select another file')

        _5_ = _5_()
        self._upload.addListener(_5_)

    class MyReceiver(Receiver):
        _fileName = None
        _mtype = None
        _sleep = None
        _total = 0

        def receiveUpload(self, filename, mimetype):
            self._fileName = filename
            self._mtype = mimetype

            class _6_(OutputStream):

                def write(self, b):
                    MyReceiver_this._total += 1
                    if MyReceiver_this._sleep and MyReceiver_this._total % 10000 == 0:
                        # TODO Auto-generated catch block
                        try:
                            self.Thread.sleep(100)
                        except self.InterruptedException, e:
                            e.printStackTrace()

            _6_ = _6_()
            return _6_

        def getFileName(self):
            return self._fileName

        def getMimeType(self):
            return self._mtype

        def setSlow(self, value):
            self._sleep = value
