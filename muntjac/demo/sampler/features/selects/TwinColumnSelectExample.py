# -*- coding: utf-8 -*-
# from com.vaadin.ui.TwinColSelect import (TwinColSelect,)


class TwinColumnSelectExample(VerticalLayout, Property.ValueChangeListener):
    _cities = ['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo', 'Paris', 'Stockholm']

    def __init__(self):
        # Shows a notification when a selection is made.
        self.setSpacing(True)
        l = TwinColSelect()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < len(self._cities)):
                break
            l.addItem(self._cities[i])
        l.setRows(7)
        l.setNullSelectionAllowed(True)
        l.setMultiSelect(True)
        l.setImmediate(True)
        l.addListener(self)
        l.setLeftColumnCaption('Available cities')
        l.setRightColumnCaption('Selected destinations')
        l.setWidth('350px')
        self.addComponent(l)

    def valueChange(self, event):
        if not (str(event.getProperty()) == '[]'):
            self.getWindow().showNotification('Selected cities: ' + event.getProperty())
