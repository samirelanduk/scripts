#! /usr/bin/env python3

import os
from shutil import copyfile

# Get package
package = os.getcwd().split(os.path.sep)[-1]

# Get script location
here = os.path.dirname(os.path.realpath(__file__))

# Copy files over
for filename in ["PULL_REQUEST_TEMPLATE.md", "ISSUE_TEMPLATE.md"]:
	with open("{}/templates/{}".format(here, filename)) as f:
		data = f.read()
	with open(".github/{}".format(filename), "w") as f:
		f.write(data.format(*[package] * data.count("{}")))


# Copy contribution docs
with open("{}/templates/CONTRIBUTING.rst".format(here)) as f:
	data = f.read()
with open("docs/source/contributing.rst", "w") as f:
	f.write(data.format(*[package] * data.count("{}")))
with open(".github/CONTRIBUTING.rst", "w") as f:
	f.write(data.format(*[package] * data.count("{}")))