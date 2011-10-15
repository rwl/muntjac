# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from muntjac.test.server.component.AbstractListenerMethodsTest import (AbstractListenerMethodsTest,)
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
