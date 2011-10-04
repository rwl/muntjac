# -*- coding: utf-8 -*-
# from com.vaadin.ui.Label import (Label,)
# from com.vaadin.ui.Button.ClickListener import (ClickListener,)


class PanelBasicExample(VerticalLayout, ClickListener):
    _panel = None

    def __init__(self):
        self.setSpacing(True)
        # Panel 1 - with caption
        self._panel = Panel('This is a standard Panel')
        self._panel.setHeight('200px')
        # we want scrollbars
        # let's adjust the panels default layout (a VerticalLayout)
        layout = self._panel.getContent()
        layout.setMargin(True)
        # we want a margin
        layout.setSpacing(True)
        # and spacing between components
        self.addComponent(self._panel)
        # Let's add a few rows to provoke scrollbars:
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 20):
                break
            self._panel.addComponent(Label('The quick brown fox jumps over the lazy dog.'))
        # Caption toggle:
        b = Button('Toggle caption')
        b.addListener(self)
        self.addComponent(b)

    def buttonClick(self, event):
        if self._panel.getCaption() == '':
            self._panel.setCaption('This is a standard Panel')
        else:
            self._panel.setCaption('')
