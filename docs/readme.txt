$Id$
$HeadURL$

Synclosure VERSION_PLACEHOLDER
Deoren Moor
http://projects.whyaskwhy.org/

Description, Usage, Requirements, Install, Contact us, Bugs, Copyright, License.


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
 
  - Include on certain types of files. For example, only want mp3 files? 
    Include them: <synclosure -imp3>

  - Exclude certain types of files. For example, don't want mov files? 
    Exclude them: <synclosure -emov>

  - Use custom actions. You want torrent files to be automatically 
    handled over to your BitTorrent Client?
    <synclosure -a torrent "c:\program files\abc\abc.exe">

  - Where would you like your destination folder?
    synclosure -d COOKIES_PODCAST

  - Create a link to synclosure.exe (or synclosure.py if using source). 
    Include it in your cronjob/scheduler or manually start it when your
    computer is idle.


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

   Note: This is included with source and binary installations, but it has
         it's own license. See 'License' at the bottom of this file.


==================
INSTALLATION
==================

binary installation:

Run setup_synclosure.exe and follow the directions. You do not require 
administrator privileges to install or run Synclosure, but you have to
install to an unprotected location if installing as a non-administrator.

source installation:

Download latest source archive or checkout from version conntrol. Everything
you  need to run it should be included.

See http://projects.whyaskwhy.org/projects/synclosure/wiki/Installation for 
more details.


Please let us know if you successfully use Synclosure on Windows 98/ME)


==================
CONTACT US
==================

We look forward to hearing from you!

 Project homepage: http://projects.whyaskwhy.org/
          Twitter: http://twitter.com/synclosure
           Forums: http://projects.whyaskwhy.org/projects/synclosure/boards


==================
BUGS
==================

Before submitting a bug, please:

#1) Make sure you are running the latest version of Synclosure.
    See the upgrade notes for details:
    http://projects.whyaskwhy.org/projects/synclosure/wiki/Upgrade

    * Make sure to backup sources.ini and cache.ini before upgrading to
      a new version.

#2) Check the forums to see if someone else has already reported the problem.
    http://projects.whyaskwhy.org/projects/synclosure/boards

#3) Search for an existing issue that matches your problem.
    http://projects.whyaskwhy.org/search/index/synclosure?issues=1

#4) If none of the above are true, please submit a bug and include as much
    relevant information as you can to help with fixing it.

Thanks!


==================
COPYRIGHT (Synclosure)
==================

Original code and name (c) by raphael balimann, 2004
Copyright (C) 2007 deoren of WhyAskWhy.org ( > 0.1)


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
