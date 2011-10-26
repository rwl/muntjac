
from muntjac.api import HorizontalLayout, TextField, Label, Alignment


class HorizontalLayoutBasicExample(HorizontalLayout):

    # this is a HorizontalLayout

    def __init__(self):
        super(HorizontalLayoutBasicExample, self).__init__()

        # First TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)

        # A dash
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)

        # Second TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)

        # Another dash
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)

        # Third TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)

        # Yet another dash
        dash = Label('-')
        self.addComponent(dash)
        self.setComponentAlignment(dash, Alignment.MIDDLE_LEFT)

        # Forth and last TextField
        tf = TextField()
        tf.setWidth('70px')
        self.addComponent(tf)
