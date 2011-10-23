
from muntjac.api import VerticalLayout, TwinColSelect
from muntjac.data.property import IValueChangeListener


class TwinColumnSelectExample(VerticalLayout, IValueChangeListener):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']

    def __init__(self):
        self.setSpacing(True)

        l = TwinColSelect()

        for c in self._cities:
            l.addItem(c)

        l.setRows(7)
        l.setNullSelectionAllowed(True)
        l.setMultiSelect(True)
        l.setImmediate(True)
        l.addListener(self)
        l.setLeftColumnCaption('Available cities')
        l.setRightColumnCaption('Selected destinations')
        l.setWidth('350px')
        self.addComponent(l)

    # Shows a notification when a selection is made.
    def valueChange(self, event):
        if not (str(event.getProperty()) == '[]'):
            self.getWindow().showNotification('Selected cities: '
                    + event.getProperty())
