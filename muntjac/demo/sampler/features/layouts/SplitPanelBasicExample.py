
from muntjac.ui import \
    (VerticalLayout, VerticalSplitPanel, Label, HorizontalSplitPanel,
     button, CheckBox)

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

        class LockListener(button.IClickListener):

            def __init__(self, vert, horiz):
                self._vert = vert
                self._horiz = horiz

            def buttonClick(self, event):
                self._vert.setLocked( bool(event.getButton()) )
                self._horiz.setLocked( bool(event.getButton()) )

        # Lock toggle button
        toggleLocked = CheckBox('Splits locked', LockListener(vert, horiz))
        toggleLocked.setImmediate(True)
        self.addComponent(toggleLocked)
