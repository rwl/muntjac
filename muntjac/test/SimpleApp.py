
from muntjac.application import Application
from muntjac.ui.window import Window
from muntjac.ui.label import Label

class MyClass(Application):

    def init(self):
        window = Window()
        lbl = Label("Welcome to Muntjac")
        window.addComponent(lbl)
        self.setMainWindow(window)
