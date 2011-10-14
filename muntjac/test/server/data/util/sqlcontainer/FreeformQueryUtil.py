# -*- coding: utf-8 -*-
from com.vaadin.data.util.sqlcontainer.AllTests import (AllTests,)
# from org.junit.Test import (Test,)
DB = AllTests.DB


class FreeformQueryUtil(object):

    def testDummy(self):
        # Added dummy test so JUnit will not complain about "No runnable methods".
        pass

    @classmethod
    def getQueryWithFilters(cls, filters, offset, limit):
        sh = StatementHelper()
        if AllTests.db == DB.MSSQL:
            if limit > 1:
                offset += 1
                limit -= 1
            query = cls.StringBuilder()
            query.append('SELECT * FROM (SELECT row_number() OVER (')
            query.append('ORDER BY \"ID\" ASC')
            query.append(') AS rownum, * FROM \"PEOPLE\"')
            if not filters.isEmpty():
                query.append(QueryBuilder.getWhereStringForFilters(filters, sh))
            query.append(') AS a WHERE a.rownum BETWEEN ').append(offset).append(' AND ').append(str(offset + limit))
            sh.setQueryString(str(query))
            return sh
        elif AllTests.db == DB.ORACLE:
            if limit > 1:
                offset += 1
                limit -= 1
            query = cls.StringBuilder()
            query.append('SELECT * FROM (SELECT x.*, ROWNUM AS ' + '\"rownum\" FROM (SELECT * FROM \"PEOPLE\"')
            if not filters.isEmpty():
                query.append(QueryBuilder.getWhereStringForFilters(filters, sh))
            query.append(') x) WHERE \"rownum\" BETWEEN ? AND ?')
            sh.addParameterValue(offset)
            sh.addParameterValue(offset + limit)
            sh.setQueryString(str(query))
            return sh
        else:
            query = cls.StringBuilder('SELECT * FROM people')
            if not filters.isEmpty():
                query.append(QueryBuilder.getWhereStringForFilters(filters, sh))
            if (limit != 0) or (offset != 0):
                query.append(' LIMIT ? OFFSET ?')
                sh.addParameterValue(limit)
                sh.addParameterValue(offset)
            sh.setQueryString(str(query))
            return sh
