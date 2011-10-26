
from muntjac.api import AbsoluteLayout, Button


class AbsoluteLayoutBasicExample(AbsoluteLayout):

    def __init__(self):
        super(AbsoluteLayoutBasicExample, self).__init__()

        self.setMargin(True)

        # Add a border to the layout with CSS to indicate its boundaries
        self.addStyleName('border')

        # allow border to show (100% would clip the right side border)
        self.setWidth('99%')
        self.setHeight('300px')
        self.addComponent(Button('Top: 10px, left: 10px'),
                'top:10px; left:10px')
        self.addComponent(Button('Top: 10px, right: 40px'),
                'top:10px; right:40px')
        self.addComponent(Button('Bottom: 0, left: 50%'),
                'bottom:0; left:50%')
        self.addComponent(Button('Top: 50%, right: 50%'),
                'top:50%; right:50%')

        # Components can overflow out of the container, but they will be
        # clipped. Negative values do not work currently (see issue #4479)
        self.addComponent(Button('Top: 50%, right: 50%'), 'top:50%; right:50%')
