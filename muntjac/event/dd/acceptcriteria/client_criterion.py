# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class ClientCriterion(object):
    """An annotation type used to point the client side counterpart for server
    side a L{AcceptCriterion} class. Usage is pretty similar to L{ClientWidget}
    which is used with Muntjac components that have a specialized client side
    counterpart.

    Annotations are used at GWT compilation phase, so remember to rebuild your
    widgetset if you do changes for L{ClientCriterion} mappings.
    """

    # the client side counterpart for the annotated criterion
    value = None
