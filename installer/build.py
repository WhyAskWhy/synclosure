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


def main():
    application_name = 'Synclosure'
    application_release_version = 'svn-devel' # '0.2'
    synclosure_repo_url='http://projects.whyaskwhy.org/svn/synclosure/trunk/'
    installer_project_file='setup.iss'
    installed_python_version='2.7'
    
    # If not hardcoded, the build_dir is the path where this script is located,
    # not where it's run from. Use os.getcwd() instead if that is your goal.
    build_dir = sys.path[0]
    output_dir = sys.path[0]
    
    checkout_path = build_dir + os.sep + application_name
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    def CheckoutSVN:
        """Checks out SVN working copy"""
        client = pysvn.Client()
        #check out the current version of the pysvn project
        client.checkout(synclosure_repo_url, checkout_path)

    def GetRevision:
        """Returns revision number of working copy"""
        client = pysvn.Client()
        return client.info(checkout_path).revision.number

    def CompilePythonCode:
        os.system('python setup_freeze.py build')
        os.rename(checkout_path + os.sep + 'build\exe.win32-' + installed_python_version, checkout_path + os.sep + 'package')
        os.rmdir(checkout_path + os.sep + 'build)

    def BuildInnoSetupInstaller(release_version):
        print date 
        print 'Compiling: %s %s' % (application_name, release_version)

        # iscc /Q /O"%OUTPUT_DIR%" "%BUILD_DIR%\%APPLICATION_NAME%\%APP_ISS_FILE%"
        compile_command = 'iscc /Q /O' + output_dir + " " + checkout_path \
            + os.sep +  installer_project_file

        os.system(compile_command)

    def BuildWiXProject(release_version):
        pass

#####################################
# Initial Setup
#####################################

    # Change CWD to build_dir
    os.chdir(build_dir)

    if os.path.exists(checkout_path):

        revision = GetRevision()
    
        # If this is a development build, append the revision number
        if not application_release_version == 'svn-devel':
            release_version = application_release_version + '-r' + revision
    
        print 'Already exists: %s' % build_dir + os.sep + application_name
        print 'Skipping checkout and attempting to build ...'

        CompilePythonCode()
        BuildInnoSetupInstaller(release_version)
        BuildWiXProject(release_version)
        
        
    else:
        CheckoutSVN()
        CompilePythonCode()
        BuildInnoSetupInstaller(release_version)
        BuildWiXProject(release_version)


if __name__ == "__main__":
    main()
