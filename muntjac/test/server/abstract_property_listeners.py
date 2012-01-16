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

from muntjac.data.util.abstract_property import AbstractProperty

from muntjac.data.property import \
    ValueChangeEvent, IValueChangeListener, IReadOnlyStatusChangeEvent, \
    IReadOnlyStatusChangeListener

from muntjac.data.util.object_property import ObjectProperty

from muntjac.test.server.component import abstract_listener_methods_test


class TestAbstractPropertyListeners(
            abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testValueChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(AbstractProperty,
                ValueChangeEvent, IValueChangeListener, ObjectProperty(''))


    def testReadOnlyStatusChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(AbstractProperty,
                IReadOnlyStatusChangeEvent, IReadOnlyStatusChangeListener,
                ObjectProperty(''))
