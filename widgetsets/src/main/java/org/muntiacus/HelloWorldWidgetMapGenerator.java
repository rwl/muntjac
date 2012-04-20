package org.muntiacus;

import java.util.Collection;
import java.util.HashSet;

import com.vaadin.terminal.Paintable;
import com.vaadin.terminal.gwt.widgetsetutils.EagerWidgetMapGenerator;
import com.vaadin.ui.Label;
import com.vaadin.ui.VerticalLayout;
import com.vaadin.ui.Window;

public class HelloWorldWidgetMapGenerator extends EagerWidgetMapGenerator {

	@Override
	protected Collection<Class<? extends Paintable>> getUsedPaintables() {

		Collection<Class<? extends Paintable>> paintables =
		new HashSet<Class<? extends Paintable>>();

		paintables.add(Label.class);
		paintables.add(Window.class);
		paintables.add(VerticalLayout.class);

 		return paintables;
	}

}
