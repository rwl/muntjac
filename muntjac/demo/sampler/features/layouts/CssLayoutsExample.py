
from muntjac.ui import VerticalLayout, Panel, Label, CssLayout


class CssLayoutsExample(VerticalLayout):

    def __init__(self):
        self.setMargin(True)

        # Note, that this code example may not be self explanatory without
        # checking out the related CSS file in the sampler theme.

        panel = Panel('Panel')
        panel.setStyleName('floatedpanel')
        panel.setWidth('30%')
        panel.setHeight('370px')
        panel.addComponent(Label('This panel is 30% wide '
                + 'and 370px high (defined on the server side) '
                + 'and floated right (with custom css). '
                + 'Try resizing the browser window to see '
                + 'how the black boxes (floated left) '
                + 'behave. Every third of them has colored text '
                + 'to demonstrate the dynamic css injection.'))

        bottomCenter = Label(
                'I\'m a 3 inches wide footer at the bottom of the layout')
        bottomCenter.setSizeUndefined()  # disable 100% default width
        bottomCenter.setStyleName('footer')


        class cssLayout(CssLayout):

            def __init__(self):
                self._brickCounter = 0

            def getCss(self, c):
                # colorize every third rendered brick
                if isinstance(c, Brick):
                    self._brickCounter += 1
                    if self._brickCounter % 3 == 0:
                        # make every third brick colored and italic
                        return 'color: #ff6611; font-style: italic;'
                return None


        cssLayout.setWidth('100%')

        cssLayout.addComponent(panel)
        for _ in range(15):
            # add black labels that float left
            cssLayout.addComponent(Brick())

        cssLayout.addComponent(bottomCenter)

        self.addComponent(cssLayout)


class Brick(Label):
    """A simple label containing text "Brick" and themed black square."""

    def __init__(self):
        super(Brick, self).__init__('Brick')
        # disable 100% width that label has by default
        self.setSizeUndefined()
        self.setStyleName('brick')
