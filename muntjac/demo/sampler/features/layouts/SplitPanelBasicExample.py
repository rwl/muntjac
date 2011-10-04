# -*- coding: utf-8 -*-


class SplitPanelBasicExample(VerticalLayout):
    brownFox = 'The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. '

    def __init__(self):
        # First a vertical SplitPanel
        vert = VerticalSplitPanel()
        vert.setHeight('450px')
        vert.setWidth('100%')
        vert.setSplitPosition(150, Sizeable.UNITS_PIXELS)
        self.addComponent(vert)
        # add a label to the upper area
        vert.addComponent(Label(self.brownFox))
        # Add a horizontal SplitPanel to the lower area
        horiz = HorizontalSplitPanel()
        horiz.setSplitPosition(50)
        # percent
        vert.addComponent(horiz)
        # left component:
        horiz.addComponent(Label(self.brownFox))
        # right component:
        horiz.addComponent(Label(self.brownFox))
        # Lock toggle button

        class _0_(Button.ClickListener):

            def buttonClick(self, event):
                self.vert.setLocked(event.getButton().booleanValue())
                self.horiz.setLocked(event.getButton().booleanValue())

        _0_ = _0_()
        toggleLocked = CheckBox('Splits locked', _0_)
        toggleLocked.setImmediate(True)
        self.addComponent(toggleLocked)
