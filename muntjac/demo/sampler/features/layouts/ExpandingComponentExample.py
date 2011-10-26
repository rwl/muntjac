
from muntjac.api import VerticalLayout, HorizontalLayout, Button


class ExpandingComponentExample(VerticalLayout):

    def __init__(self):
        super(ExpandingComponentExample, self).__init__()

        self.setSpacing(True)

        # Basic scenario: single expanded component
        layout = HorizontalLayout()
        layout.setWidth('100%')  # make the layout grow with the window size
        self.addComponent(layout)

        naturalButton = Button('Natural')
        naturalButton.setDescription('This button does not have an explicit '
                'size - instead, its size depends on it\'s content - a.k.a '
                '<i>natural size.</i>')
        layout.addComponent(naturalButton)

        expandedButton = Button('Expanded')
        expandedButton.setWidth('100%')
        expandedButton.setDescription('The width of this button is set to '
                '100% and expanded, and will thus occupy the space left over '
                'by the other components.')
        layout.addComponent(expandedButton)
        layout.setExpandRatio(expandedButton, 1.0)

        sizedButton = Button('Explicit')
        sizedButton.setWidth('150px')
        sizedButton.setDescription('This button is explicitly set to be '
                '150 pixels wide.')
        layout.addComponent(sizedButton)


        # Ratio example
        layout = HorizontalLayout()
        layout.setWidth('100%')  # make the layout grow with the window size
        self.addComponent(layout)

        naturalButton = Button('Natural')
        naturalButton.setDescription('This button does not have an explicit '
                'size - instead, its size depends on it\'s content - a.k.a '
                '<i>natural size.</i>')
        layout.addComponent(naturalButton)

        expandedButton1 = Button('Ratio 1.0')
        expandedButton1.setWidth('100%')
        expandedButton1.setDescription('The width of this button is set to '
                '100% and expanded with a ratio of 1.0, and will in this '
                'example occupy 1:3 of the leftover space.')
        layout.addComponent(expandedButton1)
        layout.setExpandRatio(expandedButton1, 1.0)

        expandedButton2 = Button('Ratio 2.0')
        expandedButton2.setWidth('100%')
        expandedButton2.setDescription('The width of this button is set to '
                '100% and expanded with a ratio of 2.0, and will in this '
                'example occupy 2:3 of the leftover space.')
        layout.addComponent(expandedButton2)
        layout.setExpandRatio(expandedButton2, 2.0)
