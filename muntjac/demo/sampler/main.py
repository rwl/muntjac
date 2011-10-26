
from muntjac.util import run_app

from muntjac.application import Application
from muntjac.ui.window import Window

from muntjac.demo.sampler.features.layouts.LayoutMarginExample \
    import LayoutMarginExample as Example


class App(Application):

    def init(self):
        main = Window('Muntjac')
#        main.setTheme('sampler-reindeer')
        self.setMainWindow(main)

        main.addComponent(Example())


if __name__ == '__main__':
    run_app(App, nogui=True, forever=True, debug=True)
