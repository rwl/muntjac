
from muntjac.api import Label


class CodeLabel(Label):

    CLIENT_WIDGET = None #ClientWidget(VCodeLabel)

    def __init__(self, content=None):

        if content is None:
            self.setContentMode(self.CONTENT_PREFORMATTED)
            super(CodeLabel, self).__init__()
        else:
            super(CodeLabel, self).__init__(content, self.CONTENT_PREFORMATTED)


    def setContentMode(self, contentMode):
        if contentMode != self.CONTENT_PREFORMATTED:
            raise NotImplementedError, 'Only preformatted content supported'

        super(CodeLabel, self).setContentMode(self.CONTENT_PREFORMATTED)
