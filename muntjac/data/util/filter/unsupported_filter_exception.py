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

"""Exception for cases where a container does not support a specific
type of filters."""

class UnsupportedFilterException(RuntimeError):
    """Exception for cases where a container does not support a specific
    type of filters.

    If possible, this should be thrown already when adding a filter to a
    container. If a problem is not detected at that point, an
    L{NotImplementedError} can be thrown when attempting to perform filtering.
    """

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 0:
            pass
        elif nargs == 1:
            if isinstance(args[0], Exception):
                cause, = args
                super(UnsupportedFilterException, self).__init__(cause)
            else:
                message, = args
                super(UnsupportedFilterException, self).__init__(message)
        elif nargs == 2:
            message, cause = args
            super(UnsupportedFilterException, self).__init__(message, cause)
        else:
            raise ValueError
