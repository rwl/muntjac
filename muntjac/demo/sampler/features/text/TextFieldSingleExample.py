# -*- coding: utf-8 -*-


class TextFieldSingleExample(VerticalLayout, Property.ValueChangeListener):
    _editor = TextField('Echo this:')

    def __init__(self):
        # Catch the valuechange event of the textfield and update the value of the
        # label component

        self.setSpacing(True)
        self._editor.addListener(self)
        self._editor.setImmediate(True)
        # editor.setColumns(5); // guarantees that at least 5 chars fit
        self.addComponent(self._editor)

    def valueChange(self, event):
        # Show the new value we received
        self.getWindow().showNotification(self._editor.getValue())
