
from muntjac.ui import Label


class CodeLabel(Label):

    def __init__(self, content=None):

        if content is None:
            self.setContentMode(self.CONTENT_PREFORMATTED)
        else:
            super(CodeLabel, self)(content, self.CONTENT_PREFORMATTED)


    def setContentMode(self, contentMode):
        if contentMode != self.CONTENT_PREFORMATTED:
            raise NotImplementedError, 'Only preformatted content supported'

        super(CodeLabel, self).setContentMode(self.CONTENT_PREFORMATTED)
