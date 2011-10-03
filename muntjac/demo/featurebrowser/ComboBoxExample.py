
from random import random

from muntjac.ui import CustomComponent, VerticalLayout, ComboBox
from muntjac.ui.abstract_select import IFiltering


class ComboBoxExample(CustomComponent):

    _firstnames = ['John', 'Mary', 'Joe', 'Sarah', 'Jeff', 'Jane', 'Peter',
            'Marc', 'Robert', 'Paula', 'Lenny', 'Kenny', 'Nathan', 'Nicole',
            'Laura', 'Jos', 'Josie', 'Linus']

    _lastnames = ['Torvalds', 'Smith', 'Adams', 'Black', 'Wilson', 'Richards',
            'Thompson', 'McGoff', 'Halas', 'Jones', 'Beck', 'Sheridan',
            'Picard', 'Hill', 'Fielding', 'Einstein']

    def __init__(self):
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)

        # starts-with filter
        s1 = ComboBox('Select with starts-with filter')
        s1.setFilteringMode(IFiltering.FILTERINGMODE_STARTSWITH)
        s1.setWidth('20em')
        for _ in range(105):
            s1.addItem(
                    (self._firstnames[random() * (len(self._firstnames) - 1)]
                     + ' '
                     + self._lastnames[random() * (len(self._lastnames) - 1)]))
        s1.setImmediate(True)
        main.addComponent(s1)

        # contains filter
        s2 = ComboBox('Select with contains filter')
        s2.setFilteringMode(IFiltering.FILTERINGMODE_CONTAINS)
        s2.setWidth('20em')
        for _ in range(500):
            s2.addItem(
                    (self._firstnames[random() * (len(self._firstnames) - 1)]
                     + ' '
                     + self._lastnames[random() * (len(self._lastnames) - 1)]))
        s2.setImmediate(True)
        main.addComponent(s2)

        # initially empty
        s3 = ComboBox('Initially empty; enter your own')
        s3.setWidth('20em')
        s3.setImmediate(True)
        s3.setNewItemsAllowed(True)
        main.addComponent(s3)
