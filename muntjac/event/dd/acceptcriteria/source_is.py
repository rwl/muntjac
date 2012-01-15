# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Client side criteria that checks if the drag source is one of the given
components."""

from muntjac.event.transferable_impl import TransferableImpl

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class SourceIs(ClientSideCriterion):
    """Client side criteria that checks if the drag source is one of the given
    components.
    """

    def __init__(self, *component):
        self._component = component


    def paintContent(self, target):
        super(SourceIs, self).paintContent(target)
        target.addAttribute('c', len(self._component))
        for i, c in enumerate(self._component):
            target.addAttribute('component' + i, c)


    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            for c in self._component:
                if c == sourceComponent:
                    return True
        return False


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIs'
