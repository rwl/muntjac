
import unittest

from abstract_in_memory_container_listeners \
    import TestAbstractInMemoryContainerListeners

from abstract_container_listeners import TestAbstractContainerListeners
from abstract_property_listeners import TestAbstractPropertyListeners
from event_router import TestEventRouter
from file_type_resolver import TestFileTypeResolver
from indexed_container_listeners import IndexedContainerListeners
from key_mapper import TestKeyMapper
from license_in_python_files import LicenseInPythonFiles
from mime_types import TestMimeTypes
from propertyset_item_listeners import PropertysetItemListeners

from terminal.gwt.server.test_static_files_location \
    import TestStaticFilesLocation

from componentcontainer.add_remove_component_test import AddRemoveComponentTest

from validation.test_read_only_validation import TestReadOnlyValidation


def suite():

    suite = unittest.TestSuite()

    suite.addTest( unittest.makeSuite(TestAbstractInMemoryContainerListeners) )
    suite.addTest( unittest.makeSuite(TestAbstractContainerListeners) )
    suite.addTest( unittest.makeSuite(TestAbstractPropertyListeners) )
    suite.addTest( unittest.makeSuite(TestEventRouter) )
    suite.addTest( unittest.makeSuite(TestFileTypeResolver) )
    suite.addTest( unittest.makeSuite(IndexedContainerListeners) )
    suite.addTest( unittest.makeSuite(TestKeyMapper) )
    suite.addTest( unittest.makeSuite(LicenseInPythonFiles) )
    suite.addTest( unittest.makeSuite(TestMimeTypes) )
    suite.addTest( unittest.makeSuite(PropertysetItemListeners) )

#    suite.addTest( unittest.makeSuite(TestStaticFilesLocation) )

    suite.addTest( unittest.makeSuite(AddRemoveComponentTest) )

    suite.addTest( unittest.makeSuite(TestReadOnlyValidation) )

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )
