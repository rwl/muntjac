# -*- coding: utf-8 -*-
from com.vaadin.tests.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
# from com.vaadin.terminal.StreamVariable.StreamingProgressEvent import (StreamingProgressEvent,)
# from com.vaadin.ui.Upload import (Upload,)
# from com.vaadin.ui.Upload.FailedEvent import (FailedEvent,)
# from com.vaadin.ui.Upload.FailedListener import (FailedListener,)
# from com.vaadin.ui.Upload.FinishedEvent import (FinishedEvent,)
# from com.vaadin.ui.Upload.FinishedListener import (FinishedListener,)
# from com.vaadin.ui.Upload.ProgressListener import (ProgressListener,)
# from com.vaadin.ui.Upload.StartedEvent import (StartedEvent,)
# from com.vaadin.ui.Upload.StartedListener import (StartedListener,)
# from com.vaadin.ui.Upload.SucceededEvent import (SucceededEvent,)
# from com.vaadin.ui.Upload.SucceededListener import (SucceededListener,)


class UploadListeners(AbstractListenerMethodsTest):

    def testProgressListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Upload, StreamingProgressEvent, ProgressListener)

    def testSucceededListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Upload, SucceededEvent, SucceededListener)

    def testStartedListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Upload, StartedEvent, StartedListener)

    def testFailedListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Upload, FailedEvent, FailedListener)

    def testFinishedListenerAddGetRemove(self):
        self.testListenerAddGetRemove(Upload, FinishedEvent, FinishedListener)
