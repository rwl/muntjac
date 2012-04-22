# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.components import abstract_test_field_value_change

from muntjac.ui.combo_box import ComboBox


class TestComboBoxValueChange(
            abstract_test_field_value_change.AbstractTestFieldValueChange):
    """Check that the value change listener for a combo box is triggered
    exactly once when setting the value, at the correct time.
    """

    def setUp(self):
        combo = ComboBox()
        combo.addItem('myvalue')
        super(TestComboBoxValueChange, self).setUp(combo)


    def setValue(self, field):
        variables = dict()
        variables['selected'] = ['myvalue']
        field.changeVariables(field, variables)
