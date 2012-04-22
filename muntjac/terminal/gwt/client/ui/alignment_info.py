# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@


class AlignmentInfo(object):

    LEFT = None
    RIGHT = None
    TOP = None
    BOTTOM = None
    CENTER = None
    MIDDLE = None
    TOP_LEFT = None

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 1:
            bitMask, = args
            self._bitMask = bitMask
        elif nargs == 2:
            horizontal, vertical = args
            self.__init__(horizontal.getBitMask() + vertical.getBitMask())
        else:
            raise ValueError


    def getBitMask(self):
        return self._bitMask


    def isTop(self):
        return self._bitMask & Bits.ALIGNMENT_TOP == Bits.ALIGNMENT_TOP


    def isBottom(self):
        return self._bitMask & Bits.ALIGNMENT_BOTTOM == Bits.ALIGNMENT_BOTTOM


    def isLeft(self):
        return self._bitMask & Bits.ALIGNMENT_LEFT == Bits.ALIGNMENT_LEFT


    def isRight(self):
        return self._bitMask & Bits.ALIGNMENT_RIGHT == Bits.ALIGNMENT_RIGHT


    def isVerticalCenter(self):
        return self._bitMask & Bits.ALIGNMENT_VERTICAL_CENTER == Bits.ALIGNMENT_VERTICAL_CENTER


    def isHorizontalCenter(self):
        return self._bitMask & Bits.ALIGNMENT_HORIZONTAL_CENTER == Bits.ALIGNMENT_HORIZONTAL_CENTER


    def getVerticalAlignment(self):
        if self.isBottom():
            return 'bottom'
        elif self.isVerticalCenter():
            return 'middle'
        return 'top'


    def getHorizontalAlignment(self):
        if self.isRight():
            return 'right'
        elif self.isHorizontalCenter():
            return 'center'
        return 'left'


class Bits(object):
    """Bitmask values for client server communication"""

    ALIGNMENT_LEFT = 1
    ALIGNMENT_RIGHT = 2
    ALIGNMENT_TOP = 4
    ALIGNMENT_BOTTOM = 8
    ALIGNMENT_HORIZONTAL_CENTER = 16
    ALIGNMENT_VERTICAL_CENTER = 32


AlignmentInfo.LEFT = AlignmentInfo(Bits.ALIGNMENT_LEFT)
AlignmentInfo.RIGHT = AlignmentInfo(Bits.ALIGNMENT_RIGHT)
AlignmentInfo.TOP = AlignmentInfo(Bits.ALIGNMENT_TOP)
AlignmentInfo.BOTTOM = AlignmentInfo(Bits.ALIGNMENT_BOTTOM)
AlignmentInfo.CENTER = AlignmentInfo(Bits.ALIGNMENT_HORIZONTAL_CENTER)
AlignmentInfo.MIDDLE = AlignmentInfo(Bits.ALIGNMENT_VERTICAL_CENTER)
AlignmentInfo.TOP_LEFT = AlignmentInfo(Bits.ALIGNMENT_TOP + Bits.ALIGNMENT_LEFT)
