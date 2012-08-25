package org.muntiacus;

import com.vaadin.terminal.Paintable;
import com.vaadin.terminal.gwt.widgetsetutils.EagerWidgetMapGenerator;
import com.vaadin.ui.ClientWidget.LoadStyle;

public class DeferredWidgetMapGenerator extends EagerWidgetMapGenerator {
    @Override
    protected LoadStyle getLoadStyle(Class<? extends Paintable> paintableType) {
        return LoadStyle.DEFERRED;
    }
}
