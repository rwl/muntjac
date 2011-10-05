
from muntjac.ui import VerticalLayout, ComboBox
from muntjac.data.property import IValueChangeListener
from muntjac.ui.abstract_select import IFiltering


class ComboBoxPlainExample(VerticalLayout, IValueChangeListener):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']

    def __init__(self):
        # Shows a notification when a selection is made.
        self.setSpacing(True)
        l = ComboBox('Please select a city')

        for c in self._cities:
            l.addItem(c)

        l.setFilteringMode(IFiltering.FILTERINGMODE_OFF)
        l.setImmediate(True)
        l.addListener(self)
        self.addComponent(l)


    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: '
                + event.getProperty())
