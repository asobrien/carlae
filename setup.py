#!/usr/bin/env python
#----------------------------------------------------------------------
# Setup script for carlae package
import sys
import subprocess
from setuptools import setup, find_packages
import os

# from distutils.core import setup
# from pip.req import parse_requirements


# Get requirements from file
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()


VERSION = subprocess.check_output(["git", "describe"]).strip().lstrip('v')


### GET REQUIREMENTS FROM FILE
# parse_requirements() returns generator of pip.req.InstallRequirement objects
# install_reqs = parse_requirements('./src/requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
# reqs = [str(ir.req) for ir in install_reqs]


# Check for required Python packages
# from: http://www.pytables.org/trac-bck/browser/trunk/db.py?rev=4149
def check_import(pkgname, pkgver):
    try:
        mod = __import__(pkgname)
    except ImportError:
        exit_with_error(
            "Can't find a local %s Python installation." % pkgname,
            "Please read carefully the ``README`` file "
            "and remember that PyTables needs the %s package "
            "to compile and run." % pkgname )
    else:
        if mod.__version__ < pkgver:
            exit_with_error(
                "You need %(pkgname)s %(pkgver)s or greater to run PyTables!"
                % {'pkgname': pkgname, 'pkgver': pkgver} )

    print ( "* Found %(pkgname)s %(pkgver)s package installed."
            % {'pkgname': pkgname, 'pkgver': mod.__version__} )
    globals()[pkgname] = mod


#Having the Python version included in the package name makes managing a
#system with multiple versions of Python much easier.

def find_name(base='carlae'):
    '''If "--name-with-python-version" is on the command line then
    append "-pyX.Y" to the base name'''
    name = base
    if '--name-with-python-version' in sys.argv:
        name += '-py%i.%i'%(sys.version_info[0],sys.version_info[1])
        sys.argv.remove('--name-with-python-version')
    return name


NAME = find_name()
#----------------------------------------------------------------------

setup(name=NAME,
      version=VERSION,
      description='A simple URL shortener for your domain',
      author="Anthony O'Brien",
      author_email='anthony@bearonis.com',
      url='https://github.com/asobrien/carlae',
      license='MIT',
      install_requires=required_packages,
      include_package_data=True,
      zip_safe=False,
      # package_dir={'carlae': 'src'},
      # packages=['carlae']
      packages=find_packages()

     )