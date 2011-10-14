# -*- coding: utf-8 -*-
# from com.vaadin.Application import (Application,)
# from org.junit.Assert.assertEquals import (assertEquals,)
# from org.junit.Assert.assertFalse import (assertFalse,)
# from org.junit.Assert.assertNull import (assertNull,)
# from org.junit.Assert.assertTrue import (assertTrue,)
# from org.junit.Test import (Test,)


class AddRemoveSubWindow(object):

    class TestApp(Application):

        def init(self):
            w = Window('Main window')
            self.setMainWindow(w)

    def addSubWindow(self):
        app = self.TestApp()
        app.init()
        subWindow = Window('Sub window')
        mainWindow = app.getMainWindow()
        mainWindow.addWindow(subWindow)
        # Added to main window so the parent of the sub window should be the
        # main window
        assertEquals(subWindow.getParent(), mainWindow)
        # Should throw an exception as it has already been added to the
        # main window
        # Try to add the same sub window to another window
        try:
            mainWindow.addWindow(subWindow)
            assertTrue('Window.addWindow did not throw the expected exception', False)
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]
        # Should throw an exception as it has already been added to the
        # main window
        try:
            w = Window()
            w.addWindow(subWindow)
            assertTrue('Window.addWindow did not throw the expected exception', False)
        except self.IllegalArgumentException, e:
            pass # astStmt: [Stmt([]), None]

    def removeSubWindow(self):
        app = self.TestApp()
        app.init()
        subWindow = Window('Sub window')
        mainWindow = app.getMainWindow()
        mainWindow.addWindow(subWindow)
        # Added to main window so the parent of the sub window should be the
        # main window
        assertEquals(subWindow.getParent(), mainWindow)
        # Remove from the wrong window, should result in an exception
        removed = subWindow.removeWindow(subWindow)
        assertFalse('Window was removed even though it should not have been', removed)
        # Parent should still be set
        assertEquals(subWindow.getParent(), mainWindow)
        # Remove from the main window and assert it has been removed
        removed = mainWindow.removeWindow(subWindow)
        assertTrue('Window was not removed correctly', removed)
        assertNull(subWindow.getParent())
