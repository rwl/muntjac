
from muntjac.api import VerticalLayout, abstract_select, ComboBox
from muntjac.data.property import IValueChangeListener


class ComboBoxNewItemsExample(VerticalLayout, IValueChangeListener,
            abstract_select.INewItemHandler):

    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo',
            'Paris', 'Stockholm']


    def __init__(self):
        self._lastAdded = False

        self.setSpacing(True)
        self._l = ComboBox('Please select a city')
        for c in self._citie:
            self._l.addItem(c)

        self._l.setNewItemsAllowed(True)
        self._l.setNewItemHandler(self)
        self._l.setImmediate(True)
        self._l.addListener(self)
        self.addComponent(self._l)

    # Shows a notification when a selection is made.
    def valueChange(self, event):
        if not self._lastAdded:
            self.getWindow().showNotification('Selected city: '
                    + event.getProperty())
        self._lastAdded = False


    def addNewItem(self, newItemCaption):
        if not self._l.containsId(newItemCaption):
            self.getWindow().showNotification('Added city: '
                    + newItemCaption)
            self._lastAdded = True
            self._l.addItem(newItemCaption)
            self._l.setValue(newItemCaption)
