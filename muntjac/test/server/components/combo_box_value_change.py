# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
