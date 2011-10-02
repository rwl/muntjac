# -*- coding: utf-8 -*-
# from com.vaadin.ui.ListSelect import (ListSelect,)
# from java.util.Arrays import (Arrays,)
# from java.util.List import (List,)


class ListSelectSingleExample(VerticalLayout, Property.ValueChangeListener):
    _cities = Arrays.asList(['Berlin', 'Brussels', 'Helsinki', 'Madrid', 'Oslo', 'Paris', 'Stockholm'])

    def __init__(self):
        # Shows a notification when a selection is made. The listener will be
        # called whenever the value of the component changes, i.e when the user
        # makes a new selection.

        self.setSpacing(True)
        # 'Shorthand' constructor - also supports data binding using Containers
        citySelect = ListSelect('Please select a city', self._cities)
        citySelect.setRows(7)
        # perfect length in out case
        citySelect.setNullSelectionAllowed(False)
        # user can not 'unselect'
        citySelect.select('Berlin')
        # select this by default
        citySelect.setImmediate(True)
        # send the change to the server at once
        citySelect.addListener(self)
        # react when the user selects something
        self.addComponent(citySelect)

    def valueChange(self, event):
        self.getWindow().showNotification('Selected city: ' + event.getProperty())
