
from muntjac.application import Application
from muntjac.ui.window import Window
from muntjac.ui.label import Label


class HelloWorld(Application):

    def init(self):
        """Init is invoked on application load (when a user accesses
        the application for the first time).
        """
        # Main window is the primary browser window
        main = Window('Hello window')
        self.setMainWindow(main)

        # "Hello world" text is added to window as a Label component
        main.addComponent(Label('Hello World!'))


if __name__ == '__main__':
    from muntjac.util import run_app
    run_app(HelloWorld, nogui=True, forever=False, debug=True)
