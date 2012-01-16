# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Parent class for criteria that can be completely validated on client
side."""

from muntjac.event.dd.acceptcriteria.accept_criterion import IAcceptCriterion
from muntjac.util import clsname


class ClientSideCriterion(IAcceptCriterion):
    """Parent class for criteria that can be completely validated on client
    side. All classes that provide criteria that can be completely validated
    on client side should extend this class.

    It is recommended that subclasses of ClientSideCriterion re-validate the
    condition on the server side in L{IAcceptCriterion.accept} after
    the client side validation has accepted a transfer.
    """

    def isClientSideVerifiable(self):
        return True


    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')


    def paintContent(self, target):
        pass


    def getIdentifier(self):
        return clsname(self.__class__)  # FIXME: Python client-side


    def paintResponse(self, target):
        # NOP, nothing to do as this is client side verified criterion
        pass
