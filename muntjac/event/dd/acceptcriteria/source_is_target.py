# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""A criterion that ensures the drag source is the same as drop target."""

from muntjac.event.transferable_impl import TransferableImpl

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class SourceIsTarget(ClientSideCriterion):
    """A criterion that ensures the drag source is the same as drop target.
    Eg. L{Tree} or L{Table} could support only re-ordering of items,
    but no L{Transferable}s coming outside.

    Note! Class is singleton, use L{get} method to get the instance.
    """

    _instance = None

    def __init__(self):
        pass


    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            target = dragEvent.getTargetDetails().getTarget()
            return sourceComponent == target
        return False


    @classmethod
    def get(cls):
        return cls._instance


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIsTarget'


SourceIsTarget._instance = SourceIsTarget()
