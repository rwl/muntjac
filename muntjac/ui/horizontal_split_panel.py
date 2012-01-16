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
horizontally."""

from muntjac.ui.abstract_split_panel import AbstractSplitPanel


class HorizontalSplitPanel(AbstractSplitPanel):
    """A horizontal split panel contains two components and lays them
    horizontally. The first component is on the left side::

         +---------------------++----------------------+
         |                     ||                      |
         | The first component || The second component |
         |                     ||                      |
         +---------------------++----------------------+

                               ^
                               |
                         the splitter

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    CLIENT_WIDGET = None #ClientWidget(VSplitPanelHorizontal, LoadStyle.EAGER)

    def __init__(self):
        super(HorizontalSplitPanel, self).__init__()
        self.setSizeFull()
