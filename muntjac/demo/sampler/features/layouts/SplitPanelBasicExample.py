
from muntjac.api import \
    (VerticalLayout, VerticalSplitPanel, Label, HorizontalSplitPanel,
     CheckBox)

from muntjac.ui.button import IClickListener

from muntjac.terminal.sizeable import ISizeable


class SplitPanelBasicExample(VerticalLayout):

    brownFox = ('The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. '
            'The quick brown fox jumps over the lazy dog. ')

    def __init__(self):
        super(SplitPanelBasicExample, self).__init__()

        # First a vertical SplitPanel
        vert = VerticalSplitPanel()
        vert.setHeight('450px')
        vert.setWidth('100%')
        vert.setSplitPosition(150, ISizeable.UNITS_PIXELS)
        self.addComponent(vert)

        # add a label to the upper area
        vert.addComponent(Label(self.brownFox))

        # Add a horizontal SplitPanel to the lower area
        horiz = HorizontalSplitPanel()
        horiz.setSplitPosition(50)  # percent
        vert.addComponent(horiz)

        # left component:
        horiz.addComponent(Label(self.brownFox))

        # right component:
        horiz.addComponent(Label(self.brownFox))

        # Lock toggle button
        toggleLocked = CheckBox('Splits locked', LockListener(vert, horiz))
        toggleLocked.setImmediate(True)
        self.addComponent(toggleLocked)


class LockListener(IClickListener):

    def __init__(self, vert, horiz):
        self._vert = vert
        self._horiz = horiz

    def buttonClick(self, event):  # FIXME: only works once
        self._vert.setLocked( event.getButton().booleanValue() )
        self._horiz.setLocked( event.getButton().booleanValue() )
