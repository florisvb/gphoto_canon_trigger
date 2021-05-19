from distutils.core import setup

setup(
name='GphotoCanonTriggerUtils',
version='0.0.1',
author='Floris van Breugel',
author_email='floris@gmail.com',
packages = ['gphoto_canon_trigger_utils'],
license='BSD',
description='ROS triggering of canon SLRs using gphoto',
long_description=open('README.md').read(),
)
