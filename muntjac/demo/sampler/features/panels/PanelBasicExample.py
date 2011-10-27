
from muntjac.api import VerticalLayout, Panel, Label, Button
from muntjac.ui.button import IClickListener


class PanelBasicExample(VerticalLayout, IClickListener):

    def __init__(self):
        super(PanelBasicExample, self).__init__()

        self.setSpacing(True)

        # Panel 1 - with caption
        self._panel = Panel('This is a standard Panel')
        self._panel.setHeight('200px')  # we want scrollbars
        # let's adjust the panels default layout (a VerticalLayout)
        layout = self._panel.getContent()
        layout.setMargin(True)  # we want a margin
        layout.setSpacing(True)  # and spacing between components
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
        if self._panel.getCaption() == '':
            self._panel.setCaption('This is a standard Panel')
        else:
            self._panel.setCaption('')
