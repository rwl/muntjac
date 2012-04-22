# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Criterion that can be used create policy to accept/discard dragged
content."""


class IAcceptCriterion(object):
    """Criterion that can be used create policy to accept/discard dragged
    content (presented by L{Transferable}).

    The drag and drop mechanism will verify the criteria returned by
    L{DropHandler.getAcceptCriterion} before calling L{DropHandler.drop}.

    The criteria can be evaluated either on the client (browser - see
    L{ClientSideCriterion}) or on the server (see L{ServerSideCriterion}).
    If no constraints are needed, an L{AcceptAll} can be used.

    In addition to accepting or rejecting a possible drop, criteria can provide
    additional hints for client side painting.

    @see: L{DropHandler}
    @see: L{ClientSideCriterion}
    @see: L{ServerSideCriterion}
    """

    def isClientSideVerifiable(self):
        """Returns whether the criteria can be checked on the client or whether
        a server request is needed to check the criteria.

        This requirement may depend on the state of the criterion (e.g. logical
        operations between criteria), so this cannot be based on a marker
        interface.
        """
        raise NotImplementedError


    def paint(self, target):
        raise NotImplementedError


    def paintResponse(self, target):
        """This needs to be implemented iff criterion does some lazy server
        side initialization. The UIDL painted in this method will be passed to
        client side drop handler implementation. Implementation can assume that
        L{accept} is called before this method.
        """
        raise NotImplementedError


    def accept(self, dragEvent):
        """Validates the data in event to be appropriate for the
        L{DropHandler.drop} method.

        Note that even if your criterion is validated on client side, you
        should always validate the data on server side too.
        """
        raise NotImplementedError
