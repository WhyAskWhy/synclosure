# $Id$
# $HeadURL$

from cx_Freeze import setup, Executable

setup(
    name = "Synclosure",
    version = "0.2",
    description = "Synclosure is a RSS aggregator to flexibly download " \
        "files in enclosures. It supports filter keywords, custom actions " \
        "and a caching mechanism.",
    executables = [Executable("synclosure.py")])

# To compile, do the following:
# python setup_freeze.py build


# FIXME: The following error was given when trying to compile

# Missing modules:
# ? chardet imported from feedparser
# ? cjkcodecs.aliases imported from feedparser
# ? iconv_codec imported from feedparser
# ? mx.Tidy imported from feedparser
# ? tidy imported from feedparser
