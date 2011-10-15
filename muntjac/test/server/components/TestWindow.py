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

# from com.vaadin.ui.Window import (Window,)
# from com.vaadin.ui.Window.CloseEvent import (CloseEvent,)
# from com.vaadin.ui.Window.CloseListener import (CloseListener,)
# from com.vaadin.ui.Window.ResizeEvent import (ResizeEvent,)
# from com.vaadin.ui.Window.ResizeListener import (ResizeListener,)
# from junit.framework.TestCase import (TestCase,)
# from org.easymock.EasyMock import (EasyMock,)


class TestWindow(TestCase):
    _window = None

    def setUp(self):
        self._window = Window()

    def testCloseListener(self):
        cl = EasyMock.createMock(Window.CloseListener)
        # Expectations
        cl.windowClose(EasyMock.isA(CloseEvent))
        # Start actual test
        EasyMock.replay(cl)
        # Add listener and send a close event -> should end up in listener once
        self._window.addListener(cl)
        self.sendClose(self._window)
        # Ensure listener was called once
        EasyMock.verify(cl)
        # Remove the listener and send close event -> should not end up in
        # listener
        self._window.removeListener(cl)
        self.sendClose(self._window)
        # Ensure listener still has been called only once
        EasyMock.verify(cl)

    def testResizeListener(self):
        rl = EasyMock.createMock(Window.ResizeListener)
        # Expectations
        rl.windowResized(EasyMock.isA(ResizeEvent))
        # Start actual test
        EasyMock.replay(rl)
        # Add listener and send a resize event -> should end up in listener
        # once
        self._window.addListener(rl)
        self.sendResize(self._window)
        # Ensure listener was called once
        EasyMock.verify(rl)
        # Remove the listener and send close event -> should not end up in
        # listener
        self._window.removeListener(rl)
        self.sendResize(self._window)
        # Ensure listener still has been called only once
        EasyMock.verify(rl)

    def sendResize(self, window2):
        variables = dict()
        variables.put('height', 1234)
        self._window.changeVariables(self._window, variables)

    @classmethod
    def sendClose(cls, window):
        variables = dict()
        variables.put('close', True)
        window.changeVariables(window, variables)
