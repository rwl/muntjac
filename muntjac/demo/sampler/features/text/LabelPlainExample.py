# -*- coding: utf-8 -*-


class LabelPlainExample(VerticalLayout):

    def __init__(self):
        self.setSpacing(True)
        plainText = ALabel('This is an example of a Label' + ' component. The content mode of this label is set' + ' to CONTENT_TEXT. This means that it will display' + ' the content text as is. HTML and XML special characters' + ' (<,>,&) are escaped properly to allow displaying them.')
        plainText.setContentMode(ALabel.CONTENT_TEXT)
        self.addComponent(plainText)
