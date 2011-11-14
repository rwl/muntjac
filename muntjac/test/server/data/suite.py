
import unittest


from util.container_hierarchical_wrapper \
    import TestContainerHierarchicalWrapper

from util.performance_test_indexed_container \
    import PerformanceTestIndexedContainer

from util.container_sorting import TestContainerSorting
from util.hierarchical_container import TestHierarchicalContainer
from util.indexed_container import TestIndexedContainer
from util.object_property_test import ObjectPropertyTest

from util.filter.simple_string_filter_test import SimpleStringFilterTest


def suite():

    suite = unittest.TestSuite()

    suite.addTest( unittest.makeSuite(TestContainerHierarchicalWrapper) )
    suite.addTest( unittest.makeSuite(PerformanceTestIndexedContainer) )
    suite.addTest( unittest.makeSuite(TestContainerSorting) )
    suite.addTest( unittest.makeSuite(TestHierarchicalContainer) )
    suite.addTest( unittest.makeSuite(TestIndexedContainer) )
    suite.addTest( unittest.makeSuite(ObjectPropertyTest) )

    suite.addTest( unittest.makeSuite(SimpleStringFilterTest) )

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )
