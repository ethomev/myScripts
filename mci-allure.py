#!/usr/bin/python
import subprocess
import argparse

'''
This is my convenience script for building test projects & executing the tests.
I'm lazy and don't like typing the same group of commands repeatedly so I wrote this script.

TODO:
Run the script through pyton static analysis checks.
Run the 'allure report open' command as a background process so the script exits.
'''

# Setup the command line arguments
parser = argparse.ArgumentParser(description='Build the project, execute the tests & generate the allure report.')
parser.add_argument("-s", "--suites", help="The suite(s) to execute, all suites will be executed if this is left blank")
parser.add_argument("-p", "--taf_profiles", help="The taf profile(s) to use at runtime.")
parser.add_argument("-c", "--taf_clusterId", help="The taf cluster Id to use at runtime.")
# How do I set it up that I don't have to give this parameter a value
parser.add_argument("--skip_tests", help="Skip the execution of the tests & generation of the allure report", action="store_true")
args = parser.parse_args()

# populate mvn argument list
mvnArgsList = ["mvn", "clean", "install"]
if args.suites:
    suites = "-Dsuites="+args.suites
    mvnArgsList.append(suites)
if args.taf_profiles:
    taf_profiles = "-Dtaf.profiles="+args.taf_profiles
    mvnArgsList.append(taf_profiles)
if args.taf_clusterId:
    taf_clusterId = "-Dtaf.clusterId="+args.taf_clusterId
    mvnArgsList.append(taf_clusterId)
if args.skip_tests:
    mvnArgsList.append("-DskipTests")

# execute mvn clean install with variables
mvn = subprocess.Popen(mvnArgsList, stdout=subprocess.PIPE)
subprocess.call(["tee", "console.log"], stdin=mvn.stdout)
mvn.wait()
print "mvn exit code: "+str(mvn.returncode)
print "mvn args: "+str(mvnArgsList)
# if install was successful generate allure report
if mvn.returncode == 0 and args.skip_tests == False:
    print "=== Generating allure report ==="
    subprocess.call(["allure", "generate", "target/allure-results"])
    # TODO: run this as a background process
    open_report = subprocess.call(["allure", "report", "open"])
    open_report.kill()
else:
    print "=== Not generating allure report ==="
    
