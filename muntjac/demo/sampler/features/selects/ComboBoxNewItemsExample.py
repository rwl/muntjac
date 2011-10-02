# -*- coding: utf-8 -*-
# from com.vaadin.data.Property.ValueChangeEvent import (ValueChangeEvent,)
# from com.vaadin.ui.AbstractSelect import (AbstractSelect,)


class ComboBoxNewItemsExample(VerticalLayout, Property.ValueChangeListener, AbstractSelect.NewItemHandler):
    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo', 'Paris', 'Stockholm']
    _l = None
    _lastAdded = False

    def __init__(self):
        # Shows a notification when a selection is made.
        self.setSpacing(True)
        self._l = ComboBox('Please select a city')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._cities)):
                break
            self._l.addItem(self._cities[i])
        self._l.setNewItemsAllowed(True)
        self._l.setNewItemHandler(self)
        self._l.setImmediate(True)
        self._l.addListener(self)
        self.addComponent(self._l)

    def valueChange(self, event):
        if not self._lastAdded:
            self.getWindow().showNotification('Selected city: ' + event.getProperty())
        self._lastAdded = False

    def addNewItem(self, newItemCaption):
        if not self._l.containsId(newItemCaption):
            self.getWindow().showNotification('Added city: ' + newItemCaption)
            self._lastAdded = True
            self._l.addItem(newItemCaption)
            self._l.setValue(newItemCaption)
