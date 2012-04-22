# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""A IComponent that builds a ITransferable for a drag and drop operation."""

from muntjac.ui.component import IComponent


class IDragSource(IComponent):
    """IDragSource is a L{IComponent} that builds a L{Transferable} for a
    drag and drop operation.

    In Muntjac the drag and drop operation practically starts from client side
    component. The client side component initially defines the data that will
    be present in L{Transferable} object on server side. If the server side
    counterpart of the component implements this interface, terminal
    implementation lets it create the L{Transferable} instance from the raw
    client side "seed data". This way server side implementation may translate
    or extend the data that will be available for L{DropHandler}.
    """

    def getTransferable(self, rawVariables):
        """IDragSource may convert data added by client side component to
        meaningful values for server side developer or add other data based
        on it.

        For example Tree converts item identifiers to generated string keys for
        the client side. Muntjac developer don't and can't know anything about
        these generated keys, only about item identifiers. When tree node is
        dragged client puts that key to L{Transferable}s client side
        counterpart. In L{Tree.getTransferable} the key is converted
        back to item identifier that the server side developer can use.

        @param rawVariables:
                   the data that client side initially included in
                   L{Transferable}s client side counterpart.
        @return: the L{Transferable} instance that will be passed to
                L{DropHandler} (and/or L{AcceptCriterion})
        """
        raise NotImplementedError
