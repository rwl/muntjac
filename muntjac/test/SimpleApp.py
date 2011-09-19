
from muntjac.Application import Application
from muntjac.ui.Window import Window
from muntjac.ui.Label import Label

class MyClass(Application):

    def init(self):
        window = Window()
        lbl = Label("Welcome to Muntjac")
        window.addComponent(lbl)
        self.setMainWindow(window)
