# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Criterion that accepts all drops anywhere on the component."""

from muntjac.event.dd.acceptcriteria.client_side_criterion import \
    ClientSideCriterion


class AcceptAll(ClientSideCriterion):
    """Criterion that accepts all drops anywhere on the component.

    Note! Class is singleton, use L{get} method to get the instance.
    """

    _singleton = None

    def __init__(self):
        pass

    @classmethod
    def get(cls):
        return cls._singleton


    def accept(self, dragEvent):
        return True


    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.AcceptAll'

AcceptAll._singleton = AcceptAll()
