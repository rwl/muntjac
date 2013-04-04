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

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.window import \
    Window, ResizeEvent, IResizeListener, CloseEvent, ICloseListener

from muntjac.event.field_events import \
    FocusEvent, IFocusListener, BlurEvent, IBlurListener


class WindowListeners(AbstractListenerMethodsTest):

    def testFocusListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, FocusEvent, IFocusListener)


    def testBlurListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, BlurEvent, IBlurListener)


    def testResizeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, ResizeEvent, IResizeListener)


    def testCloseListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Window, CloseEvent, ICloseListener)
