# $Id$
# $HeadURL$

from cx_Freeze import setup, Executable

release_version = "VERSION_PLACEHOLDER"

if release_version[0:3] == "dev":
    exe_version = '0.0.' + str(release_version[9:])
else:
    exe_version = release_version

setup(
    name = "Synclosure",
    version = exe_version,
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
