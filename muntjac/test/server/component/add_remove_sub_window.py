# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
