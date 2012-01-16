# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""A compound criterion that accepts the drag if all of its criteria
accepts the drag."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class And(ClientSideCriterion):
    """A compound criterion that accepts the drag if all of its criteria
    accepts the drag.

    @see: L{Or}
    """

    def __init__(self, *criteria):
        """@param criteria:
                   criteria of which the And criterion will be composed
        """
        self.criteria = criteria


    def paintContent(self, target):
        super(And, self).paintContent(target)
        for crit in self.criteria:
            crit.paint(target)


    def accept(self, dragEvent):
        for crit in self.criteria:
            if not crit.accept(dragEvent):
                return False
        return True


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.And'
