# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Criterion that wraps another criterion and inverts its return value."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class Not(ClientSideCriterion):
    """Criterion that wraps another criterion and inverts its return value.
    """

    def __init__(self, acceptCriterion):
        self._acceptCriterion = acceptCriterion


    def paintContent(self, target):
        super(Not, self).paintContent(target)
        self._acceptCriterion.paint(target)


    def accept(self, dragEvent):
        return not self._acceptCriterion.accept(dragEvent)


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.Not'
