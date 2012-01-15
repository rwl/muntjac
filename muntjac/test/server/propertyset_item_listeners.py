# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component import abstract_listener_methods_test

from muntjac.data.util.propertyset_item import PropertysetItem

from muntjac.data.item import \
    IPropertySetChangeEvent, IPropertySetChangeListener


class PropertysetItemListeners(
            abstract_listener_methods_test.AbstractListenerMethodsTest):

    def testPropertySetChangeListenerAddGetRemove(self):
        self._testListenerAddGetRemove(PropertysetItem,
                IPropertySetChangeEvent, IPropertySetChangeListener)
