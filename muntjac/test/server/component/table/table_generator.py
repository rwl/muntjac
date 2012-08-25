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

from unittest import TestCase
from muntjac.ui.table import Table


class TableGenerator(TestCase):

    @classmethod
    def createTableWithDefaultContainer(cls, properties, items):
        t = Table()

        for i in range(properties):
            t.addContainerProperty('Property %d' % i, str, None)

        for j in range(items):
            item = t.addItem('Item %d' % j)
            for i in range(properties):
                v = 'Item %d/Property %d' % (j, i)
                item.getItemProperty('Property %d' % i).setValue(v)

        return t


    def testTableGenerator(self):
        t = self.createTableWithDefaultContainer(1, 1)
        self.assertEquals(len(t), 1)
        self.assertEquals(len(t.getContainerPropertyIds()), 1)

        t = self.createTableWithDefaultContainer(100, 50)
        self.assertEquals(len(t), 50)
        self.assertEquals(len(t.getContainerPropertyIds()), 100)
