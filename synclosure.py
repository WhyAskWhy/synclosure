#!/usr/bin/env python


"""
Synclosure automatically downloads files found in RSS enclosures.
"""

# $Id$
# $HeadURL$

# Built-in modules
import sys
import os
import urllib2
import ConfigParser

# parse command line arguments, 'sys.argv'
from optparse import OptionParser

import re
import httplib
import time
import socket


# 3rd party module, included in repo
# Homepage: http://www.feedparser.org/
import feedparser

# Build script should set this.
VERSION_TAG = 'VERSION_PLACEHOLDER'

# But if not, then get the revision of this file to use as version.
if VERSION_TAG == 'VERSION_' + 'PLACEHOLDER':
    # Strip out everything except for numbers from the svn Revision property
    __version__ = "dev-r" + re.sub(r'[^0-9]', '', "$Revision$") + "-svn"
else:
    __version__ = VERSION_TAG

__author__ = "Raphael Balimann (spam@raphb.ch)"
__copyright__ = """Copyright (c) 2004 Raphael Balimann
Copyright (c) 2007 deoren of WhyAskWhy.org"""
__license__ = "Licensed under the GPL.  See License.txt for details."
__product__ = "Synclosure %s" % __version__

__contributors__ = ["deoren <http://whyaskwhy.org/>",]

def main():

    # Create customized user agent
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', __product__)]


    feedlist, enclosures, oldenclosures, nl = [], [], [], '\n'

    #OptParse is a pain, so as of now i'm sticking to that custom format
    configfile, cache = 'sources.ini', 'cache.ini'

    #FIXME: Make this easier - perhaps a config file with each item per line?  Friendly keywords perhaps?
    # Characters or words to strip from Podcast Feed titles for directory creation.
    # See http://docs.python.org/lib/re-syntax.html
    destfolderfilter = "\W"
    filenamefilter ="\%20"
    urlfilter="\""

    # Print additional debug messages for troubleshooting  True|False
    debugmodeon = False

    # Grab 1 byte of enclosure for testing
    spidermodeon = False
    if spidermodeon: debugmodeon = False

    # Timeout between download requests (in seconds).
    waittime = 10

    # Set a timeout on blocking socket operations. Subsequent socket operations 
    # will raise a timeout exception if the timeout period value has elapsed 
    # before the operation has completed. 
    socket.setdefaulttimeout(1200)


    # Do we add enclosures to the cache file (cache.ini) that result in a HTTP 404 error? (iow, don't request again?)
    ignorenotfound = True

    # Do we add invalid enclosures links to the cache file (cache.ini)? (iow, don't request again?)
    ignoreinvalidlinks = True

    # How many times we should try to get the finalurl for an enclosure or attempt to download it
    retrylimit = 2

    # Should we remove the partial file on user abort or failure to download?
    removepartialfile = True

    def ShowProductInfo():
        """Print out app name, version, copyright and license info"""
        # FIXME: Improve this     
        print "\n",__product__, "\n"
        print '-' * 65
        print __copyright__
        print __license__
        print '-' * 65, "\n"

    def WriteFile(filename, msg):
        """Wrapper to safely read/write content to source and cache files"""
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
                print nl+'[error] couldnt create/access/read file (' \
                    + filename + '), ' + 'check permissions.'+nl
                return False

    #load a file into a list, ignore lines beginning with a '#'
    def ParseFile(filename):
        """Parse file into list for iterating through"""
        result = []
        if os.access(filename, os.W_OK) and os.path.isfile(filename):
            f = open(filename)
            for line in f:
                stripped_line = line.strip()

                # If line is commented out or is empty length ...
                if (len(stripped_line) <= 0) or (stripped_line[0] == '#'): 
                    # ... do not add it to feedlist
                    continue
                else:
                    result.append(stripped_line)
            f.close()
        else:
            return False
        return result


    def DownloadFile(url, downloadfolder, retrylimit, waittime):
        """Wrapper for urlopen to make use of retrylimit, waittime values"""

        # Filter out invalid content from author's XML feed
        if debugmodeon: print "original url is %s" % url
        url = SanitizeName(url, urlfilter, 'url')
        if debugmodeon: print "sanitized url is %s" % url

        try:
            # Create a file handle for enclosure (after redirects).  Use customized user agent.
            remotefile_fh = opener.open(url)

        except urllib2.HTTPError, e:
            # FIXME: Loop through a dictionary and define both template output and action based on that?
            if e.code == 404:
                print '*' * 60
                print '[WARNING] NOT FOUND:', url            
                if ignorenotfound:
                    print '[NOTICE ] Adding url to cache'
                    WriteFile(cache, url+'\n')
                print '*' * 60, "\n\n"
                oldenclosures.append(url)

            elif e.code == 403:
                print '*' * 60
                print '[WARNING] ACCESS DENIED:', url            
                if ignorenotfound:
                    print '[NOTICE ] Adding url to cache'
                    WriteFile(cache, url+'\n')
                print '*' * 60, "\n"
                oldenclosures.append(url)        
            else:
                print "geturl HTTPError %s on url %s" % (e.code, url)
                pass # FIXME: Is this being handled?  - May not be worth worrying about?

        # FIXME: This will need better handling
        except urllib2.URLError, e:
            print "geturl URLError %s on url %s" % (e.reason, url)

        # Perhaps handle socket.error differently?    
        except (socket.timeout, socket.error, IOError, httplib.BadStatusLine, httplib.IncompleteRead), errdesc:
            # Presumably the server have borked the connection for an unknown reason. Let's try again.
            if not retrylimit == 0:
                (dir, file) = os.path.split(url)
                print '*' * 60
                print "[WARNING] Failed to download %s to %s" % (file, dir)
                print "\t Error Description: ", errdesc, "\n"
                print "\tRetrying ..."
                print '*' * 60
                time.sleep(waittime)
                retrylimit -=1
                DownloadFile(url, downloadfolder, retrylimit, waittime)
            else:
                # Give up on this file (for this session) and proceed to the next one
                print "\t\tRetry limit exhausted, moving on to next file"

        else:
            # no problems encountered thus far
            finalurl = remotefile_fh.geturl()
            if finalurl is not None:
                remotefile = os.path.basename(finalurl)

                # FIXME:    Come up with a better variable name here, after all the 'enclosurefilename' variable
                #                   really should be something that reflects that it's a local file.  localenclosurefilename?
                enclosurefilename = os.path.join(downloadfolder, remotefile)

            if debugmodeon:
                print "Original enclosure url:", url
                print "Enc url after redirect:", finalurl        

            localfilename = SanitizeName(enclosurefilename, 
                filenamefilter, type='file')

            try:            
                localfile_fh = open(localfilename, 'wb')
            except IOError, errdesc:
                # FIXME: This "if" section 'may' not be necessary if the 404 section catches all of the invalid links
                if len(remotefile) == 0:                
                    # FIXME: Update comment - make sense?
                    # If the url listed in the enclosure was not to a file then add
                    # it to the cache so we will not try to download it again.
                    # ex: http://example.com/                 
                    print '\n', '*' * 60
                    print '[NOTICE ]  INVALID LINK ENCOUNTERED'
                    print '*' * 60

                    if ignoreinvalidlinks:                                    
                        print '\tAdding: ', url, \
                            '\n\tto cache to prevent future download attempts'

                        # Here we're using the the global 'enclosure' value instead of the sanitized 'url'
                        # value.  This is because the check for previously downloaded enclosures in the
                        # main body uses the entry in the cache file directly against the author's enclosure
                        # value.  They have to match exactly.
                        WriteFile(cache, enclosure+'\n')
                        oldenclosures.append(enclosure)            
                    else:
                        print "Skipping invalid link"
                #else:
                    # The problem is most likely a filename issue.  Previous revs 
                    # bombed out due to invalid characters.
                    # print '\n', '*' * 60
                    # print '[ERROR  ]  Could not save to file.  Check filename below'
                    # print '*' * 60
                    # print str(errdesc).split(':')[1]
                    # sys.exit()
            else:
                try:                
                    if spidermodeon: 
                        localfile_fh.write(remotefile_fh.read(1))
                    else:
                        localfile_fh.write(remotefile_fh.read())

                # if the file is currently being downloaded, a Ctrl-C will be caught here
                except (KeyboardInterrupt, SystemExit):
                    if debugmodeon: print "here i am after remotefile_fh.read()"

                    # If user wishes to remove failed downloaded file, do so
                    if removepartialfile:
                        if debugmodeon: print "removepartialfile setting is on"
                        RemoveFile(localfile_fh, localfilename)
                    raise

                except (socket.timeout, IOError, httplib.BadStatusLine), errdesc:
                    # Presumably the server have borked the connection for an unknown reason. Let's try again.
                    if not retrylimit == 0:
                        (dir, file) = os.path.split(enclosurefilename)
                        print '*' * 60
                        print "[NOTICE] Failed to download %s to %s" % (file, dir)
                        print "\t Error Description: ", errdesc, "\n"
                        print "\tRetrying ..."
                        print '*' * 60
                        time.sleep(waittime)
                        retrylimit -=1
                        DownloadFile(enclosure, enclosurefilename, 
                            retrylimit, waittime)
                    else:
                        # Give up on this file (for this session) and proceed to the next one
                        print "\t\tRetry limit exhausted, moving on to next file"

                else:
                    # File was successfully downloaded
                    localfile_fh.flush()

                    # Log the downloaded file (enclosure) to the cache list (cache.ini)
                    WriteFile(cache, enclosure+'\n')

                finally:                
                    localfile_fh.close()


    def SanitizeName(name, filter, type=""):
        """
        Accepts the name of a file or folder, which type 
        it is and a regex pattern of characters to strip
        from the name.
        """

        if str(type).lower() == "folder":
            cleanname = re.sub(filter, "", name)
            if debugmodeon: print "cleanname is %s" % cleanname
            return cleanname

        elif str(type).lower() == "file":
            # Strip away question mark and all characters follow it.
            file = name.split('?').pop(0)
            cleanname = re.sub(filter, "", file)
            if debugmodeon: print "cleanname is %s" % cleanname
            return cleanname

        elif str(type).lower() == "url":
            cleanname = re.sub(filter, "", name)
            if debugmodeon: print "cleanname is %s" % cleanname
            return cleanname

        else:
            functionname = sys._getframe().f_code.co_name 
            message = "INVALID USE OF %s" % functionname
            sys.exit(message)


    def RemoveFile(localfile_fh, file):
        """Receives file handle to saved copy of enclosure and full path to file"""

        # FIXME: Should this function do this, or should it be the calling block's responsibility?
        # Close file handle if it's still open
        localfile_fh.close()

        # remove file (if exists)
        if debugmodeon:print file
        if os.path.isfile(file):
            #urllib.urlcleanup()
            print "[NOTICE  ]\t* Removing partial file"
            os.unlink(file)
            if debugmodeon:print "just removed file"


    ShowProductInfo()

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


    defaultfeedlist = [
    '# Default list of xml feeds with enclosures',
    '#this is a comment',
    '#See http://projects.whyaskwhy.org/projects/synclosure/ for more information.',
    'http://radio.weblogs.com/0001014/categories/dailySourceCode/rss.xml',
    'http://www.evilgeniuschronicles.org/audio/podcast.xml',
    'http://www.itconversations.com/rss/recentWithEnclosures.php',
    'http://www.blogdigger.com/media/avi.xml',
    'http://www.blogdigger.com/media/mp3.xml',
    'http://www.blogdigger.com/media/mov.xml',
    'http://www.blogdigger.com/media/wmv.xml',
    'http://www.scripting.com/rss.xml',
    'http://www.cnet.com/i/pod/cnet_buzz.xml',
    'http://leo.am/podcasts/sn/',
    'http://feeds.feedburner.com/dailybreakfast',
    'http://feeds.feedburner.com/KathyMaistersStartCookingVideoCast',
    'http://radio.linuxquestions.org/syndicate/lq.php',
    'http://www.abc.net.au/rn/podcast/feeds/science.xml',
    'http://www.daveramsey.com/media/audio/podcast/podcast_itunes.xml',
    ]

    feedlist = ParseFile(configfile) #load rss list
    oldenclosures = ParseFile(cache) #load downloaded files list

    if not feedlist: #feedlist empty, create default
        for feed in defaultfeedlist:
            WriteFile(configfile, feed.strip() + '\n')

        feedlist = ParseFile(configfile)

    if not oldenclosures: #cache empty, create new file
        WriteFile(cache, '')
        oldenclosures = ParseFile(cache)

    feedcount = len(feedlist)
    print "Beginnging feed processing ..."
    for feed in feedlist:
        try:
            parsed = feedparser.parse(feed, agent=__product__)

            # If parser did not find a title from the feed url, consider it
            # to be invalid ...
            if not 'title' in parsed['feed']:
                print "[WARNING] Skipping invalid feed: %s \n" % feed
                continue

            # Don't echo 'parsing' for empty lines
            # FIXME: Isn't this already being handled by ParseFile?
            if len(feed) != 0: 
                # Show a countdown of the remaining feeds to be parsed (after this one) using 5 digit padding
                print '\n[%.5d left]' % (feedcount -1), 'parsing: ' + parsed['feed']['title']
                feedcount -= 1

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
                            print 'downloading: ' + enclosure.split("/")[-1]

                            #define download folder, etc
                            if destination and os.path.isdir(cmdlineOptions.destination) and not os.path.isfile(cmdlineOptions.destination):
                                downloadfolder = cmdlineOptions.destination
                            else:                            
                                # Apply the regular expression against the title of the RSS Podcast feed and 
                                # use the result as the folder to download the list of enclosures to             
                                downloadfolder = SanitizeName(parsed.feed.title, destfolderfilter, type="folder")

                            if not os.path.isdir(downloadfolder):
                                try:
                                        os.mkdir(downloadfolder)
                                except:
                                        sys.exit(nl+'[error] cannot create download folder (' + downloadfolder + ') ' \
                                        'check permissions')

                            DownloadFile(enclosure, downloadfolder, retrylimit, waittime)

                            if action_list:
                                for action in action_list:
                                    keyword, program = action
                                    if keyword in enclosure:
                                        tempname = 'actionstart.bat'
                                        WriteFile(tempname, '@start "'+program+'" "'+os.path.abspath(enclosurefilename.replace('%20', ' '))+'"')
                                        os.system(tempname)
                                        os.remove(tempname)

                        except KeyboardInterrupt:
                            # That's all folks
                            sys.exit("[quitting]\t* Aborting on user request")

    print "\nAll feeds parsed. Thank you for using",  __product__

if __name__ == "__main__":
    main()
