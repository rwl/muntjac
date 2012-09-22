from muntjac.api import TabSheet

from muntjac.ui.themes import Runo

class StackedSheet(TabSheet):
    def __init__(self):
        super(StackedSheet, self).__init__()
        self.hideTabs(True)
        self.addStyleName(Runo.TABSHEET_SMALL)
