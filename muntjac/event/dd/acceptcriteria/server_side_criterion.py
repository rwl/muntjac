# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Parent class for criteria which are verified on the server side."""

from muntjac.event.dd.acceptcriteria.accept_criterion import IAcceptCriterion


class ServerSideCriterion(IAcceptCriterion):
    """Parent class for criteria which are verified on the server side
    during a drag operation to accept/discard dragged content (presented
    by L{Transferable}).

    Subclasses should implement the L{IAcceptCriterion.accept} method.

    As all server side state can be used to make a decision, this is more
    flexible than L{ClientSideCriterion}. However, this does require
    additional requests from the browser to the server during a drag operation.

    @see: IAcceptCriterion
    @see: ClientSideCriterion
    """

    def isClientSideVerifiable(self):
        return False


    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')


    def paintContent(self, target):
        pass


    def paintResponse(self, target):
        pass


    def getIdentifier(self):
        #return clsname(ServerSideCriterion)  # FIXME: Python client side
        return 'com.vaadin.event.dd.acceptcriteria.ServerSideCriterion'
