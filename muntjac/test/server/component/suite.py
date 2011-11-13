
import unittest

from abstract_component_container_listeners \
    import TestAbstractComponentContainerListeners

from abstract_component_style_names \
    import TestAbstractComponentStyleNames

from abstract_ordered_layout_listeners \
    import TestAbstractOrderedLayoutListeners

from absolute_layout_listeners import AbsoluteLayoutListeners
from abstract_field_listeners import TestAbstractFieldListeners
from abstract_select_listeners import TestAbstractSelectListeners
from abstract_split_panel_listeners import TestAbstractSplitPanelListeners
from abstract_text_field_listeners import TestAbstractTextFieldListeners
from add_remove_sub_window import AddRemoveSubWindow
from button_listeners import ButtonListeners
from component_position import ComponentPosition
from css_layout_listeners import CssLayoutListeners
from date_field_listeners import DateFieldListeners
from embedded_listeners import EmbeddedListeners
from empty_tree_table import EmptyTreeTable
from grid_layout_listeners import GridLayoutListeners
from label_listeners import LabelListeners
from login_form_listeners import LoginFormListeners
from menu_bar_ids import MenuBarIds
from option_group_listeners import OptionGroupListeners
from ordered_layout import TestOrderedLayout
from panel_listeners import PanelListeners
from popup_view_listeners import PopupViewListeners
from select_listeners import SelectListeners
from tab_sheet_listeners import TabSheetListeners
from test_tab_sheet import TestTabSheet
from test_tree_listeners import TestTreeListeners
from tree_listeners import TreeListeners
from upload_listeners import UploadListeners
from uri_fragment_utility_listeners import UriFragmentUtilityListeners
from window_listeners import WindowListeners

from table.table_column_alignments import TableColumnAlignments
from table.table_generator import TableGenerator
from table.table_listeners import TableListeners
from table.table_visible_columns import TableVisibleColumns
from table.test_footer import TestFooter
from table.test_multiple_selection import TestMultipleSelection


def suite():

    suite = unittest.TestSuite()

    suite.addTest( unittest.makeSuite(TestAbstractComponentContainerListeners) )
    suite.addTest( unittest.makeSuite(TestAbstractComponentStyleNames) )
    suite.addTest( unittest.makeSuite(TestAbstractOrderedLayoutListeners) )
    suite.addTest( unittest.makeSuite(AbsoluteLayoutListeners) )
    suite.addTest( unittest.makeSuite(TestAbstractFieldListeners) )
    suite.addTest( unittest.makeSuite(TestAbstractSelectListeners) )
    suite.addTest( unittest.makeSuite(TestAbstractSplitPanelListeners) )
    suite.addTest( unittest.makeSuite(TestAbstractTextFieldListeners) )
    suite.addTest( unittest.makeSuite(AddRemoveSubWindow) )
    suite.addTest( unittest.makeSuite(ButtonListeners) )
    suite.addTest( unittest.makeSuite(ComponentPosition) )
    suite.addTest( unittest.makeSuite(CssLayoutListeners) )
    suite.addTest( unittest.makeSuite(DateFieldListeners) )
    suite.addTest( unittest.makeSuite(EmbeddedListeners) )
    suite.addTest( unittest.makeSuite(EmptyTreeTable) )
    suite.addTest( unittest.makeSuite(GridLayoutListeners) )
    suite.addTest( unittest.makeSuite(LabelListeners) )
    suite.addTest( unittest.makeSuite(LoginFormListeners) )
    suite.addTest( unittest.makeSuite(MenuBarIds) )
    suite.addTest( unittest.makeSuite(OptionGroupListeners) )
    suite.addTest( unittest.makeSuite(TestOrderedLayout) )
    suite.addTest( unittest.makeSuite(PanelListeners) )
    suite.addTest( unittest.makeSuite(PopupViewListeners) )
    suite.addTest( unittest.makeSuite(SelectListeners) )
    suite.addTest( unittest.makeSuite(TabSheetListeners) )
    suite.addTest( unittest.makeSuite(TestTabSheet) )
    suite.addTest( unittest.makeSuite(TestTreeListeners) )
    suite.addTest( unittest.makeSuite(TreeListeners) )
    suite.addTest( unittest.makeSuite(UploadListeners) )
    suite.addTest( unittest.makeSuite(UriFragmentUtilityListeners) )
    suite.addTest( unittest.makeSuite(WindowListeners) )

    suite.addTest( unittest.makeSuite(TableColumnAlignments) )
    suite.addTest( unittest.makeSuite(TableGenerator) )
    suite.addTest( unittest.makeSuite(TableListeners) )
    suite.addTest( unittest.makeSuite(TableVisibleColumns) )
    suite.addTest( unittest.makeSuite(TestFooter) )
    suite.addTest( unittest.makeSuite(TestMultipleSelection) )

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )
