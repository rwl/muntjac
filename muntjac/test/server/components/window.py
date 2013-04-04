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

import mox

from unittest import TestCase

from muntjac.ui.window import Window
from muntjac.ui import window


class TestWindow(TestCase):

    def setUp(self):
        super(TestWindow, self).setUp()

        self.mox = mox.Mox()
        self._window = Window()


    def testCloseListener(self):
        cl = self.mox.CreateMock(window.ICloseListener)

        # Expectations
        cl.windowClose(mox.IsA(window.CloseEvent))

        # Start actual test
        mox.Replay(cl)

        # Add listener and send a close event -> should end up in listener once
        self._window.addListener(cl, window.ICloseListener)
        self.sendClose(self._window)

        # Ensure listener was called once
        mox.Verify(cl)

        # Remove the listener and send close event -> should not end up in
        # listener
        self._window.removeListener(cl, window.ICloseListener)
        self.sendClose(self._window)

        # Ensure listener still has been called only once
        mox.Verify(cl)


    def testResizeListener(self):
        rl = self.mox.CreateMock(window.IResizeListener)

        # Expectations
        rl.windowResized(mox.IsA(window.ResizeEvent))

        # Start actual test
        mox.Replay(rl)

        # Add listener and send a resize event -> should end up
        # in listener once
        self._window.addListener(rl, window.IResizeListener)
        self.sendResize(self._window)

        # Ensure listener was called once
        mox.Verify(rl)

        # Remove the listener and send close event -> should not
        # end up in listener
        self._window.removeListener(rl, window.IResizeListener)
        self.sendResize(self._window)

        # Ensure listener still has been called only once
        mox.Verify(rl)


    def sendResize(self, window2):
        variables = dict()
        variables['height'] = 1234
        self._window.changeVariables(self._window, variables)


    @classmethod
    def sendClose(cls, window):
        variables = dict()
        variables['close'] = True
        window.changeVariables(window, variables)
