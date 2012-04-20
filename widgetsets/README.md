Muntjac Widgetsets
==================

The default widgetset with eager loading is compiled by default.

    $ mvn gwt:compile


To compile one of the other widgetsets:

    $ mvn gwt:compile -Dwidgetset=LazyWidgetset


To compile multiple widgetsets uncomment the `modules` section of the
gwt-maven-plugin configuration in the pom.xml file. The default output
directory for generated widgetsets is:

    ${project.basedir}/../muntjac/public/VAADIN/widgetsets


Besides the DefaultWidgetset, there are widgetsets for each Muntjac add-on:

 * CanvasWidgetset
 * CodeMirror2Widgetset
 * GoogleMapsWidgetset
 * RefresherWidgetset
 * ColorPickerWidgetset
 * StepperWidgetset
 * CSSToolsWidgetset
 * InvientChartsWidgetset
 * SVGComponentWidgetset
 * WeeLayoutWidgetset


Others widgetsets include:

 * DemoWidgetset, combines all add-on widgetsets using lazy loading,
 * LazyWidgetset, the default widgetset with lazy loading,
 * DeferredWidgetset, the default widgetset with deferred loading,
 * LiteWidgetset, the default widgetset without the Table, RichTextArea
 or Tree components,
 * HelloWorldWidgetset, a small widgetset for HelloWorld demo
 * CalcWidgetMapGenerator, a small widgetset for Calc demo.
