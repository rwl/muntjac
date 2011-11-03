"""Provides interfaces and classes in Muntjac.

Package Specification
=====================

Interface hierarchy
-------------------

The L{IComponent} interface is the top-level interface which must be
implemented by all user interface components in Muntjac. It defines the
common properties of the components and how the
framework will handle them. Most simple components, such as L{Button},
for example, do not need to implement the lower-level interfaces
described below. Notice that also the classes and interfaces required by
the component event framework are defined in L{IComponent}.

The next level in the component hierarchy are the classes
implementing the L{IComponentContainer} interface. It adds the capacity
to contain other components to L{IComponent} with a simple API.

The third and last level is the L{ILayout}, which adds the concept of
location to the components contained in a L{IComponentContainer}. It can
be used to create containers which contents can be positioned.

Component class hierarchy
-------------------------

At the top level is L{AbstractComponent} which implements the L{IComponent}
interface. As the name suggests it is abstract, but it does include a default
implementation for all methods defined in C{Component} so that a component is
free to override only those functionalities it needs.

As seen in the picture, C{AbstractComponent} serves as
the superclass for several "real" components, but it also has a some
abstract extensions. L{AbstractComponentContainer}
serves as the root class for all components (for example, panels and
windows) who can contain other components. L{AbstractField}, on the other
hand, implements several interfaces to provide a base class for components
that are used for data display and manipulation.
"""
