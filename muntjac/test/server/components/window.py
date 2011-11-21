# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
