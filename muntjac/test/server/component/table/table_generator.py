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
