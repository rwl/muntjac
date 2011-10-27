
from muntjac.api import TextField, VerticalLayout


class VerticalLayoutBasicExample(VerticalLayout):

    def __init__(self):
        # this is a VerticalLayout
        super(VerticalLayoutBasicExample, self).__init__()

        # let's add some components
        for i in range(5):
            tf = TextField('Row %d' % (i + 1))
            tf.setWidth('300px')
            # Add the component to the VerticalLayout
            self.addComponent(tf)
