
from muntjac.api import VerticalLayout, ListSelect
from muntjac.data.property import IValueChangeListener


class ListSelectMultipleExample(VerticalLayout, IValueChangeListener):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']

    def __init__(self):
        self.setSpacing(True)

        l = ListSelect('Please select some cities')

        for c in self._cities:
            l.addItem(c)

        l.setRows(7)
        l.setNullSelectionAllowed(True)
        l.setMultiSelect(True)
        l.setImmediate(True)
        l.addListener(self)
        self.addComponent(l)

    # Shows a notification when a selection is made.
    def valueChange(self, event):
        self.getWindow().showNotification('Selected cities: '
                + event.getProperty())
