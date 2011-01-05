# $Id$
# $HeadURL$

from cx_Freeze import setup, Executable
import os

release_version = "VERSION_PLACEHOLDER"

if release_version[0:3] == "dev":
    exe_version = '0.0.' + str(release_version[9:])
else:
    exe_version = release_version

Exe_Target = Executable (
      # what to build
      script = "synclosure.py",
      initScript = None,
      targetName = "synclosure.exe",
      compress = True,
      copyDependentFiles = True,
      appendScriptToExe = False,
      appendScriptToLibrary = False,
      icon = 'installer' + os.sep + 'synclosure.ico',
      #copyright = 'Original code and name (C) by raphael balimann, 2004. Modifications (C) 2007 WhyAskWhy.org',
    )
    
setup(
    name = "Synclosure",
    version = exe_version,
    author='WhyAskWhy.org',
    url='http://projects.whyaskwhy.org/projects/synclosure/',
    description = "Synclosure is a RSS aggregator to flexibly download " \
        "files in enclosures. It supports filter keywords, custom actions " \
        "and a caching mechanism.",
    options = {'build_exe':{"silent": True}},
    executables = [Exe_Target]
    )

# To compile, do the following:
# python setup_freeze.py build
