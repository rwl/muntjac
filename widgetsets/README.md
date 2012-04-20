Muntjac Widgetsets
==================

Compiles the default widgetset with eager loading by default. Widgetsets are
copied to ${project.basedir}/../muntjac/public/VAADIN/widgetsets.

    $ mvn gwt:compile


To compile one of the other widgetsets:

    $ mvn gwt:compile -Dgwt.module=org.muntiacus.LazyWidgetset


There are widgetsets for each Muntjac add-on. Others widgetsets include:

 * DemoWidgetset, combines all add-on widgetsets using lazy loading,
 * LazyWidgetset, the default widgetset with lazy loading,
 * DeferredWidgetset, the default widgetset with deferred loading and
 * HelloWorldWidgetset, a small widgetset for HelloWorld demo.
