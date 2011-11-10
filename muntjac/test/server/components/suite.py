
import unittest

from component_attach_detach_listener_test \
    import ComponentAttachDetachListenerTest

from combo_box_value_change import TestComboBoxValueChange
from grid_layout_last_row_removal import TestGridLayoutLastRowRemoval
from text_field_value_change import TestTextFieldValueChange
from window import TestWindow


def suite():

    suite = unittest.TestSuite()

    suite.addTest( unittest.makeSuite(ComponentAttachDetachListenerTest) )
    suite.addTest( unittest.makeSuite(TestComboBoxValueChange) )
    suite.addTest( unittest.makeSuite(TestGridLayoutLastRowRemoval) )
    suite.addTest( unittest.makeSuite(TestTextFieldValueChange) )
    suite.addTest( unittest.makeSuite(TestWindow) )

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )