# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.upload import \
    (Upload, IProgressListener, SucceededEvent, ISucceededListener,
     StartedEvent, IStartedListener, FailedEvent, IFailedListener,
     FinishedEvent, IFinishedListener)

from muntjac.terminal.stream_variable import IStreamingProgressEvent


class UploadListeners(AbstractListenerMethodsTest):

    def testProgressListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, IStreamingProgressEvent,
                IProgressListener)

    def testSucceededListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, SucceededEvent,
                ISucceededListener)

    def testStartedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, StartedEvent,
                IStartedListener)


    def testFailedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, FailedEvent,
                IFailedListener)

    def testFinishedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, FinishedEvent,
                IFinishedListener)
