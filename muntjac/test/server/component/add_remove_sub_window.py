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

from unittest import TestCase
from muntjac.ui.window import Window
from muntjac.application import Application


class AddRemoveSubWindow(TestCase):

    def testAddSubWindow(self):
        app = TestApp()
        app.init()
        subWindow = Window('Sub window')
        mainWindow = app.getMainWindow()
        mainWindow.addWindow(subWindow)

        # Added to main window so the parent of the sub window should be the
        # main window
        self.assertEquals(subWindow.getParent(), mainWindow)

        # Try to add the same sub window to another window
        try:
            mainWindow.addWindow(subWindow)
            self.assertTrue(False, 'Window.addWindow did not throw the '
                    'expected exception')
        except ValueError:
            # Should throw an exception as it has already been added to the
            # main window
            pass

        try:
            w = Window()
            w.addWindow(subWindow)
            self.assertTrue(False, 'Window.addWindow did not throw the '
                    'expected exception')
        except ValueError:
            # Should throw an exception as it has already been added to the
            # main window
            pass


    def testRemoveSubWindow(self):
        app = TestApp()
        app.init()
        subWindow = Window('Sub window')
        mainWindow = app.getMainWindow()
        mainWindow.addWindow(subWindow)

        # Added to main window so the parent of the sub window should be the
        # main window
        self.assertEquals(subWindow.getParent(), mainWindow)

        # Remove from the wrong window, should result in an exception
        removed = subWindow.removeWindow(subWindow)
        self.assertFalse(removed, 'Window was removed even though it should '
                'not have been')

        # Parent should still be set
        self.assertEquals(subWindow.getParent(), mainWindow)

        # Remove from the main window and assert it has been removed
        removed = mainWindow.removeWindow(subWindow)
        self.assertTrue(removed, 'Window was not removed correctly')
        self.assertEquals(subWindow.getParent(), None)


class TestApp(Application):

    def init(self):
        w = Window('Main window')
        self.setMainWindow(w)
