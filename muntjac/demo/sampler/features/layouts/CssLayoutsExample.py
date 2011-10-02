# -*- coding: utf-8 -*-
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.CssLayout import (CssLayout,)
# from com.vaadin.ui.Panel import (Panel,)


class CssLayoutsExample(VerticalLayout):

    def __init__(self):
        self.setMargin(True)
        # Note, that this code example may not be self explanatory without
        # checking out the related CSS file in the sampler theme.

        panel = Panel('Panel')
        panel.setStyleName('floatedpanel')
        panel.setWidth('30%')
        panel.setHeight('370px')
        panel.addComponent(ALabel('This panel is 30% wide ' + 'and 370px high (defined on the server side) ' + 'and floated right (with custom css). ' + 'Try resizing the browser window to see ' + 'how the black boxes (floated left) ' + 'behave. Every third of them has colored text ' + 'to demonstrate the dynamic css injection.'))
        bottomCenter = ALabel('I\'m a 3 inches wide footer at the bottom of the layout')
        bottomCenter.setSizeUndefined()
        # disable 100% default width
        bottomCenter.setStyleName('footer')

        class cssLayout(CssLayout):
            _brickCounter = 0

            def getCss(self, c):
                # colorize every third rendered brick
                if isinstance(c, CssLayoutsExample_this.Brick):
                    self._brickCounter += 1
                    if self._brickCounter % 3 == 0:
                        # make every third brick colored and italic
                        return 'color: #ff6611; font-style: italic;'
                return None

        cssLayout.setWidth('100%')
        cssLayout.addComponent(panel)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 15):
                break
            # add black labels that float left
            cssLayout.addComponent(self.Brick())
        cssLayout.addComponent(bottomCenter)
        self.addComponent(cssLayout)

    class Brick(ALabel):
        """A simple label containing text "Brick" and themed black square."""

        def __init__(self):
            super(Brick, self)('Brick')
            # disable 100% width that label has by default
            self.setSizeUndefined()
            self.setStyleName('brick')
