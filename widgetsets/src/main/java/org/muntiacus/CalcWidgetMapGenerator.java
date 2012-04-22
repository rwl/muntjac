package org.muntiacus;

import java.util.Collection;
import com.vaadin.terminal.Paintable;
import com.vaadin.ui.Button;
import com.vaadin.ui.GridLayout;

public class CalcWidgetMapGenerator extends HelloWorldWidgetMapGenerator {

	@Override
	protected Collection<Class<? extends Paintable>> getUsedPaintables() {

		Collection<Class<? extends Paintable>> paintables = super.getUsedPaintables();

		paintables.add(Button.class);
		paintables.add(GridLayout.class);

 		return paintables;
	}

}
