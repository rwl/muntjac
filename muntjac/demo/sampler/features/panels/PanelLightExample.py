
from muntjac.api import VerticalLayout, Panel, Label, Button

from muntjac.ui.button import IClickListener
from muntjac.ui.themes import Reindeer


class PanelLightExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(PanelLightExample, self).__init__()

        self.setSpacing(True)
        self.setSpacing(True)

        # Panel 1 - with caption
        self._panel = Panel('This is a light Panel')
        self._panel.setStyleName(Reindeer.PANEL_LIGHT)
        self._panel.setHeight('200px')  # we want scrollbars
        # let's adjust the panels default layout (a VerticalLayout)
        layout = self._panel.getContent()
        layout.setMargin(True)  # we want a margin
        layout.setSpacing(True)
        # and spacing between components
        self.addComponent(self._panel)

        # Let's add a few rows to provoke scrollbars:
        for _ in range(20):
            l = Label('The quick brown fox jumps over the lazy dog.')
            self._panel.addComponent(l)

        # Caption toggle:
        b = Button('Toggle caption')
        b.addListener(self, IClickListener)
        self.addComponent(b)


    def buttonClick(self, event):
        if self._panel.getCaption() is None:
            self._panel.setCaption('This is a light Panel')
        else:
            self._panel.setCaption(None)
