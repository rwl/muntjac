# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

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
