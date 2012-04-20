package org.muntiacus;

import java.util.Collection;
import com.vaadin.terminal.Paintable;
import com.vaadin.terminal.gwt.widgetsetutils.EagerWidgetMapGenerator;
import com.vaadin.ui.RichTextArea;
import com.vaadin.ui.Table;
import com.vaadin.ui.Tree;


public class LiteWidgetMapGenerator extends EagerWidgetMapGenerator {

	@Override
	protected Collection<Class<? extends Paintable>> getUsedPaintables() {

	    	Collection<Class<? extends Paintable>> minimalPaintables = super.getUsedPaintables();

	    	minimalPaintables.remove(Table.class);
	    	minimalPaintables.remove(RichTextArea.class);
	    	minimalPaintables.remove(Tree.class);

	    	return minimalPaintables;
	}

}
