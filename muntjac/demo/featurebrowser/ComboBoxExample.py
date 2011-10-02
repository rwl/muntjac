# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.ui.AbstractSelect.Filtering import (Filtering,)


class ComboBoxExample(CustomComponent):
    _firstnames = ['John', 'Mary', 'Joe', 'Sarah', 'Jeff', 'Jane', 'Peter', 'Marc', 'Robert', 'Paula', 'Lenny', 'Kenny', 'Nathan', 'Nicole', 'Laura', 'Jos', 'Josie', 'Linus']
    _lastnames = ['Torvalds', 'Smith', 'Adams', 'Black', 'Wilson', 'Richards', 'Thompson', 'McGoff', 'Halas', 'Jones', 'Beck', 'Sheridan', 'Picard', 'Hill', 'Fielding', 'Einstein']

    def __init__(self):
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)
        # starts-with filter
        s1 = ComboBox('Select with starts-with filter')
        s1.setFilteringMode(Filtering.FILTERINGMODE_STARTSWITH)
        s1.setWidth('20em')
        r = Random(5)
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < 105):
                break
            s1.addItem(self._firstnames[r.nextDouble() * (len(self._firstnames) - 1)] + ' ' + self._lastnames[r.nextDouble() * (len(self._lastnames) - 1)])
        s1.setImmediate(True)
        main.addComponent(s1)
        # contains filter
        s2 = ComboBox('Select with contains filter')
        s2.setFilteringMode(Filtering.FILTERINGMODE_CONTAINS)
        s2.setWidth('20em')
        _1 = True
        i = 0
        while True:
            if _1 is True:
                _1 = False
            else:
                i += 1
            if not (i < 500):
                break
            s2.addItem(self._firstnames[r.nextDouble() * (len(self._firstnames) - 1)] + ' ' + self._lastnames[r.nextDouble() * (len(self._lastnames) - 1)])
        s2.setImmediate(True)
        main.addComponent(s2)
        # initially empty
        s3 = ComboBox('Initially empty; enter your own')
        s3.setWidth('20em')
        s3.setImmediate(True)
        s3.setNewItemsAllowed(True)
        main.addComponent(s3)
