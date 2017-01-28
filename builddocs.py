"""Builds the documentation of a project and uploads it to the server."""

import sys
import os

# Get information from user
if len(sys.argv) < 2:
    print("\nWhere is the project?\n")
    sys.exit()
project_location = sys.argv[1]
project_name = sys.argv[1].split(os.path.sep)[-1]
