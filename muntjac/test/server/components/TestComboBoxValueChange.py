# -*- coding: utf-8 -*-
from com.vaadin.tests.server.components.AbstractTestFieldValueChange import (AbstractTestFieldValueChange,)
# from com.vaadin.ui.ComboBox import (ComboBox,)


class TestComboBoxValueChange(AbstractTestFieldValueChange):
    """Check that the value change listener for a combo box is triggered exactly
    once when setting the value, at the correct time.

    See <a href="http://dev.vaadin.com/ticket/4394">Ticket 4394</a>.
    """

    def setUp(self):
        combo = ComboBox()
        combo.addItem('myvalue')
        super(TestComboBoxValueChange, self).setUp(combo)

    def setValue(self, field):
        variables = dict()
        variables.put('selected', ['myvalue'])
        field.changeVariables(field, variables)
