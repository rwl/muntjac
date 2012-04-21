# Copyright (C) 2012 Richard Lincoln
# @MUNTJAC_LICENSE@

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

cwd = abspath(dirname(__file__))
readme = open(join(cwd, "README.rst"))
changelog = open(join(cwd, "CHANGELOG"))
kwds = {"long_description": readme.read() + '\n\n' + changelog.read()}
readme.close()
changelog.close()

setup(name="Muntjac",
      version="@VERSION@",
      description="Web application GUI toolkit",
      author="Richard Lincoln",
      author_email="r.w.lincoln@gmail.com",
      url="http://www.muntiacus.org/",
      install_requires=["Paste", "PasteWebKit", "Babel", "OrderedDict", "Mox"],
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
