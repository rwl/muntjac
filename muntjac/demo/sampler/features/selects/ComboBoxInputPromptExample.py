
from muntjac.ui import VerticalLayout, ComboBox
from muntjac.data.property import IValueChangeListener


class ComboBoxInputPromptExample(VerticalLayout, IValueChangeListener):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']

    def __init__(self):
        self.setMargin(True, False, False, False)  # for looks: more 'air'

        # Create & set input prompt
        l = ComboBox()
        l.setInputPrompt('Please select a city')

        # configure & load content
        l.setImmediate(True)
        l.addListener(self)
        for c in self._cities:
            l.addItem(c)

        # add to the layout
        self.addComponent(l)

    # Shows a notification when a selection is made.
    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: '
                + event.getProperty())
