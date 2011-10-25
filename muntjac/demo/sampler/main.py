
from muntjac.util import run_app

from muntjac.demo.sampler.SamplerApplication import SamplerApplication

from muntjac.application import Application
from muntjac.ui.window import Window
from muntjac.ui.label import Label

from muntjac.demo.sampler.features.buttons.ButtonLinkExample import ButtonLinkExample


class App(Application):

    def init(self):
        main = Window('Muntjac')
        self.setMainWindow(main)

        main.addComponent(ButtonLinkExample())


if __name__ == '__main__':
    run_app(App, nogui=True, forever=True, debug=True)
