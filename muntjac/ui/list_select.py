# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Defines a simple list."""

from muntjac.ui.abstract_select import AbstractSelect


class ListSelect(AbstractSelect):
    """This is a simple list select without, for instance, support for
    new items, lazyloading, and other advanced features.
    """

    CLIENT_WIDGET = None #ClientWidget(VListSelect)

    def __init__(self, *args):
        self._columns = 0
        self._rows = 0

        super(ListSelect, self).__init__(*args)


    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns
        is set 0, the actual number of displayed columns is determined
        implicitly by the adapter.

        @param columns:
                   the number of columns to set.
        """
        if columns < 0:
            columns = 0

        if self._columns != columns:
            self._columns = columns
            self.requestRepaint()


    def getColumns(self):
        return self._columns


    def getRows(self):
        return self._rows


    def setRows(self, rows):
        """Sets the number of rows in the editor. If the number of rows is
        set 0, the actual number of displayed rows is determined implicitly
        by the adapter.

        @param rows:
                   the number of rows to set.
        """
        if rows < 0:
            rows = 0

        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()


    def paintContent(self, target):
        target.addAttribute('type', 'list')

        # Adds the number of columns
        if self._columns != 0:
            target.addAttribute('cols', self._columns)

        # Adds the number of rows
        if self._rows != 0:
            target.addAttribute('rows', self._rows)

        super(ListSelect, self).paintContent(target)
