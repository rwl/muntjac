
from muntjac.ui import VerticalLayout, Embedded
from muntjac.terminal.external_resource import ExternalResource


class WebEmbedExample(VerticalLayout):

    def __init__(self):
        e = Embedded('Google Search',
                ExternalResource('http://www.google.com'))
        e.setType(Embedded.TYPE_BROWSER)
        e.setWidth('100%')
        e.setHeight('400px')
        self.addComponent(e)
