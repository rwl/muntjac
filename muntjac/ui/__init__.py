"""Provides interfaces and classes in Vaadin.

Package Specification
=====================

Interface hierarchy
-------------------

The {@link com.vaadin.ui.Component} interface is the top-level
interface which must be implemented by all user interface components in
Vaadin. It defines the common properties of the components and how the
framework will handle them. Most simple components, such as {@link
com.vaadin.ui.Button}, for example, do not need to implement the
lower-level interfaces described below. Notice that also the classes and
interfaces required by the component event framework are defined in
{@link com.vaadin.ui.Component}.

The next level in the component hierarchy are the classes
implementing the {@link com.vaadin.ui.ComponentContainer} interface. It
adds the capacity to contain other components to {@link
com.vaadin.ui.Component} with a simple API.

The third and last level is the {@link com.vaadin.ui.Layout},
which adds the concept of location to the components contained in a
{@link com.vaadin.ui.ComponentContainer}. It can be used to create
containers which contents can be positioned.

Component class hierarchy
-------------------------

At the top level is {@link com.vaadin.ui.AbstractComponent} which
implements the {@link com.vaadin.ui.Component} interface. As the name
suggests it is abstract, but it does include a default implementation
for all methods defined in <code>Component</code> so that a component is
free to override only those functionalities it needs.

As seen in the picture, <code>AbstractComponent</code> serves as
the superclass for several "real" components, but it also has a some
abstract extensions. {@link com.vaadin.ui.AbstractComponentContainer}
serves as the root class for all components (for example, panels and
windows) who can contain other components. {@link
com.vaadin.ui.AbstractField}, on the other hand, implements several
interfaces to provide a base class for components that are used for data
display and manipulation.
"""