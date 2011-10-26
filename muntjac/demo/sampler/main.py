
from muntjac.util import run_app

from muntjac.application import Application
from muntjac.ui.window import Window

from muntjac.demo.sampler.features.dragndrop.DragDropTreeSortingExample \
    import DragDropTreeSortingExample as Example


class App(Application):

#    def __init__(self):
#        super(App, self).__init__()
#
#        self._currentApplicationTheme = 'sampler-reindeer'


    def init(self):
        main = Window('Muntjac')
        self.setMainWindow(main)

        main.addComponent(Example())


if __name__ == '__main__':
    run_app(App, nogui=True, forever=True, debug=True)
