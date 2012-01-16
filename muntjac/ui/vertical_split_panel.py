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

"""Defines a panel that contains two components and lays them out
vertically."""

from muntjac.ui.abstract_split_panel import AbstractSplitPanel


class VerticalSplitPanel(AbstractSplitPanel):
    """A vertical split panel contains two components and lays them
    vertically. The first component is above the second component::

         +--------------------------+
         |                          |
         |  The first component     |
         |                          |
         +==========================+  <-- splitter
         |                          |
         |  The second component    |
         |                          |
         +--------------------------+
    """

    CLIENT_WIDGET = None #ClientWidget(VSplitPanelVertical, LoadStyle.EAGER)

    def __init__(self):
        super(VerticalSplitPanel, self).__init__()
        self.setSizeFull()
