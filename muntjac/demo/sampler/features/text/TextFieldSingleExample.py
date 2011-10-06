
from muntjac.ui import VerticalLayout, TextField
from muntjac.data.property import IValueChangeListener


class TextFieldSingleExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        self.setSpacing(True)

        self._editor = TextField('Echo this:')
        self._editor.addListener(self)
        self._editor.setImmediate(True)
        # editor.setColumns(5)  # guarantees that at least 5 chars fit
        self.addComponent(self._editor)

    # Catch the valuechange event of the textfield and update the value of the
    # label component
    def valueChange(self, event):
        # Show the new value we received
        self.getWindow().showNotification(self._editor.getValue())
