# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.uri_fragment_utility import \
    UriFragmentUtility, FragmentChangedEvent, IFragmentChangedListener


class UriFragmentUtilityListeners(AbstractListenerMethodsTest):

    def testFragmentChangedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(UriFragmentUtility, FragmentChangedEvent,
                IFragmentChangedListener)
