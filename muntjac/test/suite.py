
import unittest

import muntjac.test.server.suite
import muntjac.test.server.component.suite
import muntjac.test.server.components.suite
import muntjac.test.server.data.suite


def suite():
    suite = unittest.TestSuite([
        muntjac.test.server.suite.suite(),
        muntjac.test.server.component.suite.suite(),
        muntjac.test.server.components.suite.suite(),
        muntjac.test.server.data.suite.suite()
    ])
    return suite


def main():
    unittest.TextTestRunner(verbosity=2).run( suite() )


if __name__ == '__main__':
    main()
