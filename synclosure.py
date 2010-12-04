#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Raphael Balimann (spam@raphb.ch)"
__version__ = "$Revision$"
__copyright__ = "Copyright (c) 2004 Raphael Balimann"

"""
Synclosure automatically downloads files found in RSS enclosures.
"""

import feedparser, sys, os, urllib, ConfigParser, os


#customized user agent, python docs to urllib
class AppURLopener(urllib.FancyURLopener):
    def __init__(self, *args):
        self.version = "Synclosure 0.1"
        urllib.FancyURLopener.__init__(self, *args)
urllib._urlopener = AppURLopener()


feedlist, enclosures, oldenclosures, nl = [], [], [], '\n'

#OptParse is a pain, so as of now i'm sticking to that custom format
configfile, cache = 'sources.ini', 'cache.ini'

def WriteFile(filename, msg):
    if os.access(filename, os.W_OK) and os.path.isfile(filename):
        f = open(filename, 'a')
        f.write(msg)
        f.close()
    else:
        try:
            f = open(filename,'w')
            f.write(msg)
            f.close()
        except:
            print nl+'[error] couldnt create/access/read file (' + filename + '), ' \
                'check permissions.'+nl
            return False

#load a file into a list, ignore lines beginning with a '#'
def ParseFile(filename):
    result = []
    if os.access(filename, os.W_OK) and os.path.isfile(filename):
        f = open(filename)
        for line in f.xreadlines():
            if line[0] == '#': continue
            result.append(line[:-1])
        f.close()
    else:
        return False
    return result


#parse command line arguments, 'sys.argv'
from optparse import *
optParser = OptionParser()

optParser.add_option( "-e", "--exclude", action="append",
    dest="excludes", help="Specify exclude keywords in URL's", metavar='KEYWORD')
optParser.add_option( "-i", "--include", action="append",
    dest="includes", help="Specify include keywords in URL's", metavar='KEYWORD')

optParser.add_option( "-a", "--action", action="append", dest="action_list", nargs=2, 
    help="File matching keyword (string 1) gets executed as param of program (string 2)")

optParser.add_option( "-d", "--destination", action="store",
    dest="destination", help="Destination folder for downloaded files")

(cmdlineOptions, remainingArgs) = optParser.parse_args()

includes, excludes, action_list, destination = cmdlineOptions.includes, cmdlineOptions.excludes, \
    cmdlineOptions.action_list, cmdlineOptions.destination


# pickle this or something. ugly.
defaultfeedlist = '# Default list of xml feeds with enclosures\n# this is a comment\n' \
        'http://radio.weblogs.com/0001014/categories/dailySourceCode/rss.xml\n' \
        'http://www.evilgeniuschronicles.org/cgi-bin/blosxom.cgi/index.rss\n' \
        'http://www.itconversations.com/rss/recentWithEnclosures.php\n' \
        'http://www.blogdigger.com/media/avi.xml\n' \
        'http://www.blogdigger.com/media/mp3.xml\n' \
        'http://www.blogdigger.com/media/mov.xml\n' \
        'http://www.blogdigger.com/media/wmv.xml\n' \
        'http://www.scripting.com/rss.xml\n'

feedlist = ParseFile(configfile) #load rss list
oldenclosures = ParseFile(cache) #load downloaded files list

if not feedlist: #feedlist empty, create default
    WriteFile(configfile, defaultfeedlist)
    feedlist = ParseFile(configfile)
    
if not oldenclosures: #cache empty, create new file
    WriteFile(cache, '')
    oldenclosures = ParseFile(cache)

for feed in feedlist:
    print 'parsing: ' + feed[-60:]
    try:
        parsed = feedparser.parse(feed, agent="Synclosure 0.1")
    except KeyboardInterrupt:
        sys.exit(nl+'[error] parsing interrupted')
        
    except bozo_exception: #ignoring the feedparser 'parsing illformed xml' exception
        continue
    
    for entry in parsed['entries']:
        if entry.has_key('enclosures'):
            for _enclosure in entry['enclosures']:
                enclosure = _enclosure['url']
                if enclosure not in oldenclosures:
                    if includes:
                        if not [True for include in includes if include in enclosure]:
                            continue

                    if excludes:
                        if [True for exclude in excludes if exclude in enclosure]:
                            continue
                        

                    try:
                        print 'downloading: ' + enclosure[-60:]

                        #define download folder, etc
                        if destination and os.path.isdir(cmdlineOptions.destination) and not os.path.isfile(cmdlineOptions.destination):
                            downloadfolder = cmdlineOptions.destination
                        else:
                            downloadfolder = parsed.feed.title.replace(' ', '')

                        if not os.path.isdir(downloadfolder):
                            try:
                                    os.mkdir(downloadfolder)
                            except:
                                    sys.exit(nl+'[error] cannot create download folder (' + downloadfolder + ') ' \
                                    'check permissions')
                        
                        enclosurefilename = os.path.join(downloadfolder, os.path.basename(enclosure))
                        urllib.urlretrieve(enclosure, enclosurefilename.replace('%20', ' '))
                        WriteFile(cache, enclosure+'\n')
                            
                        if action_list:
                            for action in action_list:
                                keyword, program = action
                                if keyword in enclosure:
                                    tempname = 'actionstart.bat'
                                    WriteFile(tempname, '@start "'+program+'" "'+os.path.abspath(enclosurefilename.replace('%20', ' '))+'"')
                                    os.system(tempname)
                                    os.remove(tempname)
                    
                    except IOError:
                        print nl+'[error] url broken/no more disk space (..'\
                            +enclosure[-60:]+')'+nl
                    except KeyboardInterrupt:
                        sys.exit(nl+'[error] interrupted. file ('\
                            +os.path.basename(enclosure)+') unfinished')
