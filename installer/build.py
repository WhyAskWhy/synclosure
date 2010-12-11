# $Id$
# $HeadURL$

# Purpose: 
#   Build installers for upload to hosting services.The goal is to use
#   this for development and release builds.

import os
import os.path
import sys
import datetime

import pysvn

# Printout verbose bits of info during execution? True/False
debugon = False

# Printout status messages, current build phase, etc
infoon = True


def main():
    application_name = 'Synclosure'

    # svn-dev for dev builds, '0.2' for release build
    application_release_version = 'svn-dev'

    # Use a tag if doing a release build
    synclosure_repo_url='http://projects.whyaskwhy.org/svn/synclosure/trunk/'
    inno_setup_project_file='setup.iss'
    wix_project_file='setup.wix'
    installed_python_version='2.7'
    infobefore_file="infobefore.rtf"
    
    # If not hardcoded, the build_dir is the path where this script is located,
    # not where it's run from. Use os.getcwd() instead if that is your goal.
    build_dir = sys.path[0]
    output_dir = sys.path[0]
    
    checkout_path = build_dir + os.sep + application_name
    
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

        # The contents included within the installer
        package_dir = checkout_path + os.sep + 'package'        

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

            os.rename(checkout_path + os.sep + 'build\exe.win32-' \
                + installed_python_version, package_dir)
            os.rmdir(checkout_path + os.sep + 'build')

    def UpdateIncludeFile(include_file, release_version):
        """Update the version information within an include file"""

        # Open tmp file, read in orig and make changes in tmp file.
        o = open("updated_include_file.tmp","a")
        for line in open(include_file):
            line = line.replace("VERSION_PLACEHOLDER",release_version)
            o.write(line) 
        o.close()

        # Replace original with updated copy
        os.remove(include_file)
        os.rename("updated_include_file.tmp", include_file)

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

    if os.path.exists(checkout_path):

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

        infobefore_file = checkout_path + os.sep + 'installer' \
            + os.sep + infobefore_file
        UpdateIncludeFile(infobefore_file, release_version)
        CompilePythonCode()
        BuildInnoSetupInstaller(release_version)
        BuildWiXProject(release_version)

    else:
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

        infobefore_file = checkout_path + os.sep + 'installer' \
            + os.sep + infobefore_file

        UpdateIncludeFile(infobefore_file, release_version)
        CompilePythonCode()
        BuildInnoSetupInstaller(release_version)
        BuildWiXProject(release_version)


if __name__ == "__main__":
    main()