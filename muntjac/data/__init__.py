# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
