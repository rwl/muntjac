# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

cwd = abspath(dirname(__file__))
f = open(join(cwd, "README"))
kwds = {"long_description": f.read()}
f.close()

setup(name="muntjac",
      version="1.0a1",
      description="Web application GUI toolkit",
      author="Richard Lincoln",
      author_email="r.w.lincoln@gmail.com",
      url="http://pypi.python.org/pypi/muntjac",
      install_requires=["Paste", "PasteWebKit", "Babel"],
      classifiers=['Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'License :: Other/Proprietary License',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'],
      include_package_data=True,
      packages=find_packages(),
      tests_require=["Mox"],
      test_suite="muntjac.test.suite.main",
      zip_safe=True,
      **kwds)

# python setup.py sdist bdist_egg bdist_wininst bdist_msi upload