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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from unittest import TestCase
from muntjac.ui.text_field import TextField
from muntjac.data.property import IValueChangeListener


class TestEventRouter(TestCase):

    def setUp(self):
        TestCase.setUp(self)

        self._innerListenerCalls = 0


    def testAddInEventListener(self):
        tf = TextField()

        class Outer(IValueChangeListener):

            def __init__(self, test, tf):
                self._test = test
                self._tf = tf

            def valueChange(self, event):

                class Inner(IValueChangeListener):

                    def __init__(self, test):
                        self._test = test

                    def valueChange(self, event):
                        self._test._innerListenerCalls += 1
                        print 'The inner listener was called'

                self._tf.addListener(Inner(self._test), IValueChangeListener)

        tf.addListener(Outer(self, tf), IValueChangeListener)
        tf.setValue('abc')  # No inner listener calls, adds one inner
        tf.setValue('def')  # One inner listener call, adds one inner
        tf.setValue('ghi')  # Two inner listener calls, adds one inner

        self.assertEqual(self._innerListenerCalls, 3)
