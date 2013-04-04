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

"""Contains interfaces for the data layer, mainly for binding typed
data and data collections to components, and for validating data.

Data binding
============

The package contains a three-tiered structure for typed data
objects and collections of them:

    - A L{IProperty} represents a single, typed data value.

    - An L{IItem} embodies a set of I{Properties}.
      A locally unique (inside the L{IItem})
      Property identifier corresponds to each Property inside the Item.
    - A L{IContainer} contains a set of Items, each corresponding to a
      locally unique Item identifier. Note that Container imposes a few
      restrictions on the data stored in it, see L{IContainer} for further
      information.

Buffering
=========

A L{IBuffered} implementor is able to track and buffer changes and commit
or discard them later.

Validation
==========

L{IValidator} implementations are used to validate data, typically the value
of a L{IField}. One or more L{IValidator} can be added to a L{IValidatable}
implementor and then used to validate the value of the Validatable.
"""
