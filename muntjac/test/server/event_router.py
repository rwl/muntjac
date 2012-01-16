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
