"""Minimal setup script to appease buildout for Melange.
"""
import os
import re
from setuptools import setup, find_packages

match_version = re.compile("version: ([0-9\-]+)")
try:
    appyaml = open(os.path.join("app", "app.yaml.template"))
    version = match_version.findall(appyaml.read())[0]
except:
    version = "UNKNOWN"


setup(
    name = 'melange',
    description=("The goal of this project is to create a framework for "
                 "representing Open Source contribution workflows, such as"
                 " the existing Google Summer of Code TM (GSoC) program."),
    version = version,
    package_dir = {'':'src'},
    packages=find_packages('src'),
    author=open("AUTHORS").read(),
    url='http://code.google.com/p/soc',
    license='Apache2',
    install_requires = [
        'PyYAML',
        'WebOb',
        'zope.testbrowser',
        'pylint',
        'nose',
        'Django==1.1.0',
        'fixture',
        ],
    tests_require=[
        ],
    entry_points = {'console_scripts': ['run-tests = tests.run:main',
                                        'gen-app-yaml = scripts.gen_app_yaml:main',
                                        ],
                    },
    include_package_data = True,
    zip_safe = False,
    )
