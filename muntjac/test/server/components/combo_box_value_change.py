# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

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
