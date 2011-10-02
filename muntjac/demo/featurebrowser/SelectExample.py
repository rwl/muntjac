# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
# from com.vaadin.ui.ComboBox import (ComboBox,)
# from com.vaadin.ui.ListSelect import (ListSelect,)
# from com.vaadin.ui.NativeSelect import (NativeSelect,)
# from com.vaadin.ui.OptionGroup import (OptionGroup,)
# from com.vaadin.ui.TwinColSelect import (TwinColSelect,)


class SelectExample(CustomComponent):
    """Shows some basic fields for value input; TextField, DateField, Slider...

    @author IT Mill Ltd.
    """
    # listener that shows a value change notification

    class listener(Field.ValueChangeListener):

        def valueChange(self, event):
            self.getWindow().showNotification('' + event.getProperty().getValue())

    def __init__(self):
        # Initialize select with some values, make immediate and add listener.
        main = VerticalLayout()
        main.setMargin(True)
        self.setCompositionRoot(main)
        horiz = HorizontalLayout()
        horiz.setWidth('100%')
        main.addComponent(horiz)
        single = Panel('Single selects')
        single.setStyleName(Reindeer.PANEL_LIGHT)
        horiz.addComponent(single)
        multi = Panel('Multi selects')
        multi.setStyleName(Reindeer.PANEL_LIGHT)
        horiz.addComponent(multi)
        # radio button group
        sel = OptionGroup('OptionGroup')
        self.initSelect(sel)
        single.addComponent(sel)
        # checkbox group
        sel = OptionGroup('OptionGroup')
        sel.setMultiSelect(True)
        # TODO: throws if set after listener - why?
        self.initSelect(sel)
        multi.addComponent(sel)
        # single-select list
        sel = ListSelect('ListSelect')
        sel.setColumns(15)
        self.initSelect(sel)
        single.addComponent(sel)
        # multi-select list
        sel = ListSelect('ListSelect')
        sel.setColumns(15)
        sel.setMultiSelect(True)
        self.initSelect(sel)
        multi.addComponent(sel)
        # native-style dropdows
        sel = NativeSelect('NativeSelect')
        sel.setColumns(15)
        self.initSelect(sel)
        single.addComponent(sel)
        # combobox
        sel = ComboBox('ComboBox')
        sel.setWidth('15em')
        self.initSelect(sel)
        single.addComponent(sel)
        # "twin column" select
        sel = TwinColSelect('TwinColSelect')
        sel.setWidth('100%')
        sel.setColumns(15)
        self.initSelect(sel)
        multi.addComponent(sel)

    def initSelect(self, sel):
        _0 = True
        i = 1
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i <= 5):
                break
            sel.addItem('Item ' + i)
        # select one item
        sel.select('Item 1')
        # make immediate, add listener
        sel.setImmediate(True)
        sel.addListener(self.listener)
