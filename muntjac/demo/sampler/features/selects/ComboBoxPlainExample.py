
from muntjac.api import VerticalLayout, ComboBox
from muntjac.data.property import IValueChangeListener
from muntjac.ui.abstract_select import IFiltering


class ComboBoxPlainExample(VerticalLayout, IValueChangeListener):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']

    def __init__(self):
        super(ComboBoxPlainExample, self).__init__()

        self.setSpacing(True)
        l = ComboBox('Please select a city')

        for c in self._cities:
            l.addItem(c)

        l.setFilteringMode(IFiltering.FILTERINGMODE_OFF)
        l.setImmediate(True)
        l.addListener(self, IValueChangeListener)
        self.addComponent(l)

    # Shows a notification when a selection is made.
    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: '
                + str(event.getProperty()))
