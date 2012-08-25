# @INVIENT_COPYRIGHT@
# @MUNTJAC_LICENSE@


class IPaint(object):
    """This Paint interface defines how color patterns can be generated
    when drawing the InvientCharts.

    @author: Invient
    @author: Richard Lincoln
    """

    def getString(self):
        """Returns string representation of an object of type Paint.

        @return: Returns string representation of an object of type Paint.
        """
        raise NotImplementedError
