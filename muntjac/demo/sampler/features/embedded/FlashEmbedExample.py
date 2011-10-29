
from muntjac.api import VerticalLayout, Embedded
from muntjac.terminal.external_resource import ExternalResource


class FlashEmbedExample(VerticalLayout):

    def __init__(self):
        super(FlashEmbedExample, self).__init__()

        e = Embedded(None, ExternalResource('http://www.youtube.com/'
                'v/Qy67XU6xEi8&hl=en_US&fs=1&'))
        e.setMimeType('application/x-shockwave-flash')
        e.setParameter('allowFullScreen', 'true')
        e.setWidth('320px')
        e.setHeight('265px')
        self.addComponent(e)
