
from muntjac.main import muntjac

from muntjac.application import Application
from muntjac.ui.window import Window

from muntjac.demo.sampler.features.dragndrop.DragDropServerValidationExample \
    import DragDropServerValidationExample as Example


class App(Application):

    def init(self):
        main = Window('Muntjac')
        main.setTheme('sampler-reindeer')
        self.setMainWindow(main)

        main.addComponent(Example())


if __name__ == '__main__':
    muntjac(App, nogui=True, forever=True, debug=True)
