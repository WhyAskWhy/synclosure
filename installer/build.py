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
debugon = False

# Printout status messages, current build phase, etc
infoon = True


def main():
    application_name = 'Synclosure'

    # svn-dev for dev builds, '0.2' for release build
    application_release_version = 'dev-svn'
    app_release_ver_placeholder = 'VERSION_PLACEHOLDER'

    # Use a tag if doing a release build
    synclosure_repo_url='http://projects.whyaskwhy.org/svn/synclosure/trunk/'
    inno_setup_project_file='setup.iss'
    wix_project_file='setup.wix'
    installed_python_version='2.7'
    infobefore_file="infobefore.rtf"
    cx_freeze_setup = 'setup_freeze.py'
    icon_file = 'synclosure.ico'
    sources_dist = 'sources.dist.ini'
    sources_production = 'sources.ini'
    synclosure = 'synclosure.py'

    # If not hardcoded, the build_dir is the path where this script is located,
    # not where it's run from. Use os.getcwd() instead if that is your goal.
    build_dir = sys.path[0]
    output_dir = sys.path[0]

    checkout_path = build_dir + os.sep + application_name

    # The contents included within the installer
    package_dir = checkout_path + os.sep + 'package'
    date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    def CheckoutSVN(url, checkout_path):
        """Checks out SVN working copy"""

        if infoon: print '[INFO] Checking out working copy of %s' % url
        client = pysvn.Client()
        client.checkout(url, checkout_path)

    def GetRevision():
        """Returns revision number of working copy as a string"""

        client = pysvn.Client()
        return str(client.info(checkout_path).revision.number)

    def CompilePythonCode():
        """Produce a Windows executable that doesn't rely on a pre-existing
           installation of Python"""

        if os.path.exists(package_dir):
            if infoon: 
                print '[INFO] Compiled Python code exists, skipping compilation'

        else:
            if infoon: print '[INFO] Compiling Python code'

            compile_command = 'python ' + checkout_path + os.sep \
                + 'setup_freeze.py build'
            result = os.system(compile_command)
            if debugon:
                print "The result of the Python code compile is: %s" % result


    def UpdatePackageDir():
        """Moves content to be installed into package dir"""

        # Skip moving/copying anything if the directory exists.
        if not os.path.exists(package_dir):

            # Move compiled files to 'package' dir.
            os.rename(checkout_path + os.sep + 'build\exe.win32-' \
                + installed_python_version, package_dir)
            os.rmdir(checkout_path + os.sep + 'build')

            # Move docs & licenses to 'package' dir.
            os.rename(checkout_path + os.sep + 'docs', package_dir \
                + os.sep + 'docs')
            os.rename(checkout_path + os.sep + 'licenses', package_dir \
                + os.sep + 'licenses')

            # Get a copy of the icon
            shutil.copyfile(checkout_path + os.sep + 'installer' + os.sep \
                + icon_file, package_dir + os.sep + icon_file)

    def UpdateDistFiles(dist_file, production_file):
        """Renames example files so they can be used"""

        # Reset variables to full path to files
        production_file = checkout_path + os.sep + production_file
        dist_file = checkout_path + os.sep + dist_file

        # Skip renaming/moving anything if content has already been moved.
        if not os.path.exists(production_file):

            # Move sources.ini.dist to sources.ini
            os.rename(dist_file, production_file)


    def UpdateVersionTagInFile(file, release_version):
        """Update the version information within an include file"""

        # Open tmp file, read in orig and make changes in tmp file.
        o = open("updated_include_file.tmp","a")
        for line in open(file):
            line = line.replace(app_release_ver_placeholder, release_version)
            o.write(line) 
        o.close()

        # Replace original with updated copy
        os.remove(file)
        os.rename("updated_include_file.tmp", file)

    def BuildInnoSetupInstaller(release_version):
        """Produce an Inno Setup installer"""

        if infoon: print '[INFO] Compiling Inno Setup project'

        # iscc /Q /O"%OUTPUT_DIR%" /d"MY_BUILD_VERSION=r9000" "%BUILD_DIR%\%APPLICATION_NAME%\%APP_ISS_FILE%"
        compile_command = 'iscc /Q  /O' + output_dir + " " \
            + '/d"MY_BUILD_VERSION=' + release_version + '"' + " " \
            + checkout_path \
            + os.sep + 'installer' + os.sep + inno_setup_project_file

        if debugon: print compile_command
        os.system(compile_command)

    def BuildWiXProject(release_version):
        """Build MSI (Windows Installer) file"""
        # stub function
        pass

#####################################
# Initial Setup
#####################################

    if infoon: print "[INFO] Beginning build - %s" % date

    # Change CWD to build_dir
    os.chdir(build_dir)

    if not os.path.exists(checkout_path):
        CheckoutSVN(synclosure_repo_url, checkout_path)

    # Change CWD to working copy
    os.chdir(checkout_path)

    revision = GetRevision()

    # If this is a development build, append the revision number
    if application_release_version == 'svn-dev':
        release_version = application_release_version + '-r' + revision
    else:
        release_version = application_release_version

    if debugon: 
        print "[DEBUG] release_version is %s" % release_version

    if infoon:
        print '[INFO] Already exists: %s' % \
            build_dir + os.sep + application_name
        print '[INFO] Skipping checkout and attempting to build %s %s' \
            % (application_name, release_version)

    # Shown during installation.
    infobefore_file = checkout_path + os.sep + 'installer' \
        + os.sep + infobefore_file

    # Not sure when it's shown, but the cx_freeze_setup is used
    # to build the "compiled" exe version of Synclosure.
    cx_freeze_setup = checkout_path + os.sep + cx_freeze_setup

    UpdateVersionTagInFile(infobefore_file, release_version)
    UpdateVersionTagInFile(cx_freeze_setup, release_version)
    UpdateVersionTagInFile(synclosure, release_version)
    CompilePythonCode()
    UpdatePackageDir()
    UpdateDistFiles(sources_dist, sources_production)
    BuildInnoSetupInstaller(release_version)
    BuildWiXProject(release_version)


if __name__ == "__main__":
    main()
