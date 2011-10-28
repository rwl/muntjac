
from muntjac.api import VerticalLayout, Label


class LabelPlainExample(VerticalLayout):

    def __init__(self):
        super(LabelPlainExample, self).__init__()

        self.setSpacing(True)

        plainText = Label('This is an example of a Label'
                ' component. The content mode of this label is set'
                ' to CONTENT_TEXT. This means that it will display'
                ' the content text as is. HTML and XML special characters'
                ' (<,>,&) are escaped properly to allow displaying them.')
        plainText.setContentMode(Label.CONTENT_TEXT)
        self.addComponent(plainText)
