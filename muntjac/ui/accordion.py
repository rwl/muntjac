# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Defines a component similar to a TabSheet, but with a vertical orientation.
"""

from muntjac.ui.tab_sheet import TabSheet


class Accordion(TabSheet):
    """An accordion is a component similar to a L{TabSheet}, but
    with a vertical orientation and the selected component presented
    between tabs.

    Closable tabs are not supported by the accordion.

    The L{Accordion} can be styled with the .v-accordion, .v-accordion-item,
    .v-accordion-item-first and .v-accordion-item-caption styles.

    @see: L{TabSheet}
    """

    CLIENT_WIDGET = None #ClientWidget(VAccordion)
