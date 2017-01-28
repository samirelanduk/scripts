"""Builds the documentation of a project and uploads it to the server."""

import sys
import os
import subprocess

# Get information from user
if len(sys.argv) < 2:
    print("\nWhere is the project?\n")
    sys.exit()
project_location = sys.argv[1]
project_name = sys.argv[1].split(os.path.sep)[-1]

# Build docs locally
os.chdir(project_location)
os.chdir(os.path.sep.join([project_name, "docs"]))
subprocess.call("make html", shell=True)

# Push to server
host = "stage.samireland.com"
remote_location = "~/docs/"
subprocess.call("scp -r build/html/* %s:%s%s/" % (host, remote_location, project_name), shell=True)
