# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
