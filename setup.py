# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

cwd = abspath(dirname(__file__))
readme = open(join(cwd, "README"))
changelog = open(join(cwd, "CHANGELOG"))
kwds = {"long_description": readme.read() + '\n\n' + changelog.read()}
readme.close()
changelog.close()

setup(name="Muntjac",
      version="1.1.0",
      description="Web application GUI toolkit",
      author="Richard Lincoln",
      author_email="r.w.lincoln@gmail.com",
      url="http://www.muntiacus.org/",
      install_requires=["Paste", "PasteWebKit", "Babel"],
      classifiers=['Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'],
      entry_points={"console_scripts": ['muntjac = muntjac.main:main']},
      include_package_data=True,
      packages=find_packages(exclude=['babel*', 'paste*', 'gaesessions*']),
      tests_require=["Mox"],
      test_suite="muntjac.test.suite.main",
      zip_safe=False,
      **kwds)

# python setup.py sdist bdist_egg bdist_wininst bdist_msi upload