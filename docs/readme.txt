$Id$
$HeadURL$

Synclosure VERSION_PLACEHOLDER
Deoren Moor
http://projects.whyaskwhy.org/

Description, Usage, Install, Requirements, Bugs, Copyright, License.


==================
DESCRIPTION
==================

Synclosure is a rss enclosure aggregator to flexibly download the files. 
It supports filter keywords, custom actions and a caching mechanism.

==================
USAGE
==================
  - Edit the "sources.ini" file. One RSS URL fits on one line. Deleting it 
    will create a default file. Comments begin with a '#' character and 
    blank lines are allowed.
 
  - Think about include keywords. Only want mp3 files? 
    Include them: <synclosure -imp3>

  - Think about exclude keywords. Don't want mov files? 
    Exclude them: <synclosure -emov>

  - Think about custom actions. You want torrent files to be automatically 
    handled over to your BitTorrent Client?
    <synclosure -a torrent "c:\program files\abc\abc.exe">

  - Where would you like your destination folder?

  - Adapt the link to synclosure.exe. Include it in your cronjob/scheduler or
    manually start it when your computer is idle.


==================
INSTALLATION
==================

Run setup_synclosure.exe and follow the directions. You do not require 
administrator privileges to install or run Synclosure, but you have to
install to an unprotected location if installing as a non-administrator.

Alternatively you can checkout the latest code for Synclosure and run that.

See http://projects.whyaskwhy.org/projects/synclosure/wiki for more details.


Please let us know if you successfully use Synclosure on Windows 98/ME)

==================
REQUIREMENTS 
==================

binary installation:
    - Windows 2k
    - Windows XP
    - Windows Vista
    - Winvows 7

source installation:
 - Python 2.5.x
     http://www.python.org/download/releases/
     http://www.python.org/ftp/python/

 - Universal Feed Parser
     http://www.feedparser.org/




==================
BUGS
==================

Please submit a bug if you find an issue with Synclosure. The project page
is located here: 
    http://projects.whyaskwhy.org/projects/synclosure/issues



==================
COPYRIGHT
==================

Original code and name (c) by raphael balimann, 2004
Copyright (C) 2007 deoren of WhyAskWhy.org


==================
LICENSING
==================

This program is free software; you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or (at your option) 
any later version.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE.

In addition to the GPL this project also uses code that falls under other 
licenses. 

Please look within the included "licenses" folder for more information. If you 
do not agree with the terms of these licenses, please remove Synclosure.
