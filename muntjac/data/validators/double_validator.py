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

"""String validator for a double precision floating point number."""

from muntjac.data.validators.abstract_string_validator import \
    AbstractStringValidator


class DoubleValidator(AbstractStringValidator):
    """String validator for a double precision floating point number. See
    L{AbstractStringValidator} for more information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string can be parsed as an
        double.

        @param errorMessage:
                   the message to display in case the value does not validate.
        """
        super(DoubleValidator, self).__init__(errorMessage)


    def isValidString(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
