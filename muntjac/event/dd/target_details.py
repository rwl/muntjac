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

"""wraps drop target related information about DragAndDropEvent."""


class ITargetDetails(object):
    """ITargetDetails wraps drop target related information about
    L{DragAndDropEvent}.

    When a ITargetDetails object is used in L{DropHandler} it is often
    preferable to cast the ITargetDetails to an implementation provided by
    DropTarget like L{TreeTargetDetails}. They often provide a better typed,
    drop target specific API.
    """

    def getData(self, key):
        """Gets target data associated with the given string key

        @return: The data associated with the key
        """
        raise NotImplementedError


    def getTarget(self):
        """@return: the drop target on which the L{DragAndDropEvent}
        happened."""
        raise NotImplementedError
