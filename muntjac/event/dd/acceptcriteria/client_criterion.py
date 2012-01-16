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


class ClientCriterion(object):
    """An annotation type used to point the client side counterpart for server
    side a L{AcceptCriterion} class. Usage is pretty similar to L{ClientWidget}
    which is used with Muntjac components that have a specialized client side
    counterpart.

    Annotations are used at GWT compilation phase, so remember to rebuild your
    widgetset if you do changes for L{ClientCriterion} mappings.
    """

    # the client side counterpart for the annotated criterion
    value = None
