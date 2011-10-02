# -*- coding: utf-8 -*-


class VerticalLayoutBasicExample(VerticalLayout):

    def __init__(self):
        # this is a VerticalLayout
        # let's add some components
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 5):
                break
            tf = TextField('Row ' + i + 1)
            tf.setWidth('300px')
            # Add the component to the VerticalLayout
            self.addComponent(tf)
