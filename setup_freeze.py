# $Id$
# $HeadURL$

from cx_Freeze import setup, Executable

setup(
    name = "Synclosure",
    version = "VERSION_PLACEHOLDER",
    author='TBD',
    url='http://projects.whyaskwhy.org/projects/synclosure/',
    description = "Synclosure is a RSS aggregator to flexibly download " \
        "files in enclosures. It supports filter keywords, custom actions " \
        "and a caching mechanism.",
    options = {'build_exe':{"silent": True}},
    executables = [Executable("synclosure.py")]
    )

# To compile, do the following:
# python setup_freeze.py build
