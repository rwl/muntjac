# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Used by C{Form} to layout fields."""

from muntjac.ui.ordered_layout import OrderedLayout


class FormLayout(OrderedLayout):
    """FormLayout is used by L{Form} to layout fields. It may also be
    used separately without L{Form}.

    FormLayout is a close relative to vertical L{OrderedLayout}, but
    in FormLayout caption is rendered on left side of component. Required
    and validation indicators are between captions and fields.

    FormLayout does not currently support some advanced methods from
    OrderedLayout like setExpandRatio and setComponentAlignment.

    FormLayout by default has component spacing on. Also margin top and
    margin bottom are by default on.
    """

    CLIENT_WIDGET = None #ClientWidget(VFormLayout, LoadStyle.EAGER)

    def __init__(self):
        super(FormLayout, self).__init__()
        self.setSpacing(True)
        self.setMargin(True, False, True, False)
