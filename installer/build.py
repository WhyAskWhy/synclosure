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

    app_dev_release_prefix = 'dev-svn'

    # value of app_dev_release_prefix for dev builds, '0.2' for release build
    application_release_version = app_dev_release_prefix # '0.2'
    app_release_ver_placeholder = 'VERSION_PLACEHOLDER'

    # Use a tag if doing a release build
    synclosure_repo_url='http://projects.whyaskwhy.org/svn/synclosure/trunk/'
    installed_python_version='2.7'
    icon_file = 'synclosure.ico'
    sources_dist = 'sources.dist.ini'
    sources_production = 'sources.ini'

    # If not hardcoded, the build_dir is the path where this script is located,
    # not where it's run from. Use os.getcwd() instead if that is your goal.
    build_dir = sys.path[0]
    output_dir = sys.path[0]

    checkout_path = build_dir + os.sep + application_name

    # The contents included within the installer
    package_dir = checkout_path + os.sep + 'package'
    date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    # #####################
    # Project Files
    # #####################
    # These need to stay as separate values from 
    # files_with_placeholder_content var due to use in build functions?
    cx_freeze_setup = checkout_path + os.sep + 'setup_freeze.py'

    inno_setup_project_file = checkout_path + os.sep + 'installer' \
        + os.sep + 'setup.iss'

    wix_project_file = checkout_path + os.sep + 'installer' \
        + os.sep + 'setup.wxs'

    # ######################################## #
    # Files to have placeholder values updated during build
    # ######################################## #

    files_with_placeholder_content = [

        # Shown during installation.
        checkout_path + os.sep + 'installer' + os.sep + 'infobefore.rtf',
        checkout_path + os.sep + 'docs' + os.sep + 'readme.txt',
        checkout_path + os.sep + 'synclosure.py',

        # Not sure when it's shown, but the cx_freeze_setup is used
        # to build the "compiled" exe version of Synclosure.
         cx_freeze_setup,
         inno_setup_project_file,
         wix_project_file,
    ]

    def CheckoutSVN(url, checkout_path):
        """Checks out SVN working copy"""

        if infoon: print '[INFO] Checking out working copy of %s' % url
        client = pysvn.Client()
        client.checkout(url, checkout_path)

    def GetRevision():
        """Returns revision number of working copy as a string"""

        client = pysvn.Client()
        return str(client.info(checkout_path).revision.number)

    def CompilePythonCode(python_setup_file):
        """Produce a Windows executable that doesn't rely on a pre-existing
           installation of Python"""

        if os.path.exists(package_dir):
            if infoon: 
                print '[INFO] Compiled Python code exists, skipping compilation'

        else:
            if infoon: print '[INFO] Compiling Python code'
            compile_command = 'python ' + python_setup_file + ' build'
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


    def UpdateVersionTagInFiles(files, release_version):
        """Update placeholder version information within a list of files"""

        for file in files:
            if infoon: print "[INFO] Updating version tag in: %s" % file

            # Open tmp file, read in orig and make changes in tmp file.
            o = open("updated_file.tmp","a")
            for line in open(file):
                line = line.replace(app_release_ver_placeholder, release_version)
                o.write(line) 
            o.close()

            # Replace original with updated copy
            os.remove(file)
            os.rename("updated_file.tmp", file)

    def BuildInnoSetupInstaller(project_file, release_version):
        """Produce an Inno Setup installer"""

        if infoon: print '[INFO] Compiling Inno Setup project'

        # iscc /Q /O"%OUTPUT_DIR%" /d"MY_BUILD_VERSION=r9000" "%BUILD_DIR%\%APPLICATION_NAME%\%APP_ISS_FILE%"
        compile_command = 'iscc /Q  /O' + output_dir + " " \
            + '/d"MY_BUILD_VERSION=' + release_version + '" ' + project_file

        if debugon: print compile_command
        os.system(compile_command)

    def BuildWiXProject(project_file, release_version):
        """Build MSI (Windows Installer) file"""
        # stub function
        pass

#####################################
# Initial Setup
#####################################

    if infoon: print "[INFO] Beginning build - %s" % date

    if os.path.exists(checkout_path):
        if infoon:
            print '[INFO] Already exists: %s' % \
                build_dir + os.sep + application_name
            print '[INFO] Skipping checkout and attempting to build %s %s' \
                % (application_name, release_version)
    else:
        # Change CWD to build_dir
        os.chdir(build_dir)
        CheckoutSVN(synclosure_repo_url, checkout_path)

    # Change CWD to working copy
    os.chdir(checkout_path)

    revision = GetRevision()

    # If this is a development build, append the revision number
    if application_release_version == app_dev_release_prefix:
        release_version = app_dev_release_prefix + '-r' + revision
    else:
        release_version = application_release_version

    if debugon: 
        print "[DEBUG] release_version is %s" % release_version


    UpdateVersionTagInFiles(files_with_placeholder_content, release_version)

    CompilePythonCode(cx_freeze_setup)

    UpdatePackageDir()

    UpdateDistFiles(sources_dist, sources_production)

    BuildInnoSetupInstaller(inno_setup_project_file, release_version)

    BuildWiXProject(wix_project_file, release_version)


if __name__ == "__main__":
    main()
