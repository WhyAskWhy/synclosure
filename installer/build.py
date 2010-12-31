# $Id$
# $HeadURL$

# Purpose: 
#   Build installers for upload to hosting services.The goal is to use
#   this for development and release builds.

import os
import os.path
import sys
import datetime
import shutil

import pysvn

# Printout verbose bits of info during execution? True/False
DEBUG_ON = False

# Printout status messages, current build phase, etc
INFO_ON = True


def main():
    APPLICATION_NAME = 'Synclosure'

    APP_DEV_RELEASE_PREFIX = 'dev-svn'

    # value of APP_DEV_RELEASE_PREFIX for dev builds, '0.2' for release build
    APPLICATION_RELEASE_VERSION = APP_DEV_RELEASE_PREFIX # '0.2'
    APP_RELEASE_VER_PLACEHOLDER = 'VERSION_PLACEHOLDER'

    # Use a tag if doing a release build
    SYNCLOSURE_REPO_URL='http://projects.whyaskwhy.org/svn/synclosure/trunk/'
    INSTALLED_PYTHON_VERSION='2.7'
    ICON_FILE = 'synclosure.ico'
    SOURCES_DIST = 'sources.dist.ini'
    SOURCES_PRODUCTION = 'sources.ini'

    # If not hardcoded, the BUILD_DIR is the path where this script is located,
    # not where it's run from. Use os.getcwd() instead if that is your goal.
    BUILD_DIR = sys.path[0]
    OUTPUT_DIR = sys.path[0]

    CHECKOUT_PATH = BUILD_DIR + os.sep + APPLICATION_NAME

    # The contents included within the installer
    PACKAGE_DIR = CHECKOUT_PATH + os.sep + 'package'
    DATE = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    # #####################
    # Project Files
    # #####################
    # These need to stay as separate values from 
    # files_with_placeholder_content var due to use in build functions?
    CX_FREEZE_SETUP = CHECKOUT_PATH + os.sep + 'setup_freeze.py'

    INNO_SETUP_PROJECT_FILE = CHECKOUT_PATH + os.sep + 'installer' \
        + os.sep + 'setup.iss'

    WIX_PROJECT_FILE = CHECKOUT_PATH + os.sep + 'installer' \
        + os.sep + 'setup.wxs'

    # ######################################## #
    # Files to have placeholder values updated during build
    # ######################################## #

    files_with_placeholder_content = [

        # Shown during installation.
        CHECKOUT_PATH + os.sep + 'installer' + os.sep + 'infobefore.rtf',
        CHECKOUT_PATH + os.sep + 'docs' + os.sep + 'readme.txt',
        CHECKOUT_PATH + os.sep + 'synclosure.py',

        # Not sure when it's shown, but the CX_FREEZE_SETUP is used
        # to build the "compiled" exe version of Synclosure.
         CX_FREEZE_SETUP,
         INNO_SETUP_PROJECT_FILE,
         WIX_PROJECT_FILE,
    ]

    def checkout_svn(url, CHECKOUT_PATH):
        """Checks out SVN working copy"""

        if INFO_ON: print '[INFO] Checking out working copy of %s' % url
        client = pysvn.Client()
        client.checkout(url, CHECKOUT_PATH)

    def get_revision():
        """Returns revision number of working copy as a string"""

        client = pysvn.Client()
        return str(client.info(CHECKOUT_PATH).revision.number)

    def compile_python_code(python_setup_file):
        """Produce a Windows executable that doesn't rely on a pre-existing
           installation of Python"""

        if os.path.exists(PACKAGE_DIR):
            if INFO_ON: 
                print '[INFO] Compiled Python code exists, skipping compilation'

        else:
            if INFO_ON: print '[INFO] Compiling Python code'
            # Using triple quotes to handle path with spaces
            compile_command = """python "%s" build """ % python_setup_file
            result = os.system(compile_command)
            if DEBUG_ON:
                print "The result of the Python code compile is: %s" % result


    def update_package_dir():
        """Moves content to be installed into package dir"""

        # Skip moving/copying anything if the directory exists.
        if not os.path.exists(PACKAGE_DIR):

            # Move compiled files to 'package' dir.
            os.rename(CHECKOUT_PATH + os.sep + 'build\exe.win32-' \
                + INSTALLED_PYTHON_VERSION, PACKAGE_DIR)
            os.rmdir(CHECKOUT_PATH + os.sep + 'build')

            # Move docs & licenses to 'package' dir.
            os.rename(CHECKOUT_PATH + os.sep + 'docs', PACKAGE_DIR \
                + os.sep + 'docs')
            os.rename(CHECKOUT_PATH + os.sep + 'licenses', PACKAGE_DIR \
                + os.sep + 'licenses')

            # Get a copy of the icon
            shutil.copyfile(CHECKOUT_PATH + os.sep + 'installer' + os.sep \
                + ICON_FILE, PACKAGE_DIR + os.sep + ICON_FILE)

    def update_dist_files(dist_file, production_file):
        """Renames example files so they can be used"""

        # Reset variables to full path to files
        production_file = CHECKOUT_PATH + os.sep + production_file
        dist_file = CHECKOUT_PATH + os.sep + dist_file

        # Skip renaming/moving anything if content has already been moved.
        if not os.path.exists(production_file):

            # Move sources.ini.dist to sources.ini
            os.rename(dist_file, production_file)


    def update_version_tag_in_files(files, release_version):
        """Update placeholder version information within a list of files"""

        for file in files:
            if INFO_ON: print "[INFO] Updating version tag in: %s" % file

            # Open tmp file, read in orig and make changes in tmp file.
            o = open("updated_file.tmp","a")
            for line in open(file):
                line = line.replace(APP_RELEASE_VER_PLACEHOLDER, release_version)
                o.write(line) 
            o.close()

            # Replace original with updated copy
            os.remove(file)
            os.rename("updated_file.tmp", file)

    def build_innosetup_installer(project_file, release_version):
        """Produce an Inno Setup installer"""

        if INFO_ON: print '[INFO] Compiling Inno Setup project'

        # iscc /Q /O"%OUTPUT_DIR%" "%BUILD_DIR%\%APPLICATION_NAME%\%APP_ISS_FILE%"
        # Using triple quotes to handle paths with spaces
        compile_command = """iscc /Q /O"%s" "%s" """ % \
            (OUTPUT_DIR, project_file)

        if DEBUG_ON: print compile_command
        os.system(compile_command)

    def build_wix_project(project_file, release_version):
        """Build MSI (Windows Installer) file"""
        # stub function
        pass

#####################################
# Initial Setup
#####################################

    if INFO_ON: print "[INFO] Beginning build - %s" % DATE

    if os.path.exists(CHECKOUT_PATH):
        if INFO_ON:
            print '[INFO] Already exists: %s' % CHECKOUT_PATH
            print '[INFO] Skipping checkout'
    else:
        # Change CWD to BUILD_DIR
        os.chdir(BUILD_DIR)
        checkout_svn(SYNCLOSURE_REPO_URL, CHECKOUT_PATH)

    # Change CWD to working copy
    os.chdir(CHECKOUT_PATH)

    revision = get_revision()

    # If this is a development build, append the revision number
    if APPLICATION_RELEASE_VERSION == APP_DEV_RELEASE_PREFIX:
        release_version = APP_DEV_RELEASE_PREFIX + '-r' + revision
    else:
        release_version = APPLICATION_RELEASE_VERSION

    if DEBUG_ON: 
        print "[DEBUG] release_version is %s" % release_version

    if INFO_ON:
        print '[INFO] Attempting to build %s %s' \
            % (APPLICATION_NAME, release_version)

    update_version_tag_in_files(files_with_placeholder_content, release_version)

    compile_python_code(CX_FREEZE_SETUP)

    update_package_dir()

    update_dist_files(SOURCES_DIST, SOURCES_PRODUCTION)

    build_innosetup_installer(INNO_SETUP_PROJECT_FILE, release_version)

    build_wix_project(WIX_PROJECT_FILE, release_version)


if __name__ == "__main__":
    main()
