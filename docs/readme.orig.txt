Synclosure v0.1 [15. September 2004]
Raphael Balimann
http://raphb.ch/c/synclosure

Description, Usage, Install, Requirements, Todo, Bugs.


DESCRIPTION:
Synclosure is a rss enclosure aggregator to flexibly download the files. It supports filter keywords, custom actions and a caching mechanism.


USAGE:
 - Edit the "sources.ini" file. One RSS URL fits on one line. Deleting it will create a default file.
 - Think about include keywords. Only want mp3 files? Include them: <synclosure -imp3>
 - Think about exclude keywords. Don't want mov files? Exclude them: <synclosure -emov>
 - Think about custom actions. You want torrent files to be automatically handled over to your BitTorrent Client?
	<synclosure -a torrent "c:\program files\abc\abc.exe">
 - Where would you like your destination folder?
 - Adapt the link to synclosure.exe. Include it in your cronjob/scheduler or
	manually start it when your computer is idle.


INSTALL:
Either start the binary installation file (synclosure.exe) or just start the Python file (synclosure.py).


REQUIREMENTS binary installation:
 - Windows 98/ME/2k/XP


REQUIREMENTS source installation:
 - Python 2.3
	http://www.python.org/2.3.4/
	http://www.python.org/ftp/python/2.3.4/Python-2.3.4.exe

 - Universal Feed Parser
	http://www.feedparser.org/
	http://prdownloads.sourceforge.net/feedparser/feedparser-3.3.zip?download
	

TODO:
 - alternatively configure using file instead of parameters (OptParse hurts!)
 - write GUI for configuration and easy starting
 - binary installer for Linux + Mac OS X
 - caching for xml files (don't really feel like going for it, i'd start that script only once or twice a day anyway)


KNOWN BUGS:
none yet..


Copyright (C) 2004 Raphael Balimann

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.