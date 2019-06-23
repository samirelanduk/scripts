#! /usr/bin/env python3

import sys
import os
import re
import subprocess
import requests
import json
print("")

# Use downloads?
package = os.getcwd().split(os.path.sep)[-1]
downloads = requests.get("https://pypistats.org/api/packages/{}/recent".format(package)).json()["data"]["last_month"] > 100

# Add badges
blocks = []
branch = subprocess.check_output("git branch", shell=True).decode()
branches = branch.split("\n")
current_branch = [branch for branch in branches if branch.startswith("*")][0]
branch = current_branch.split()[1]
blocks.append(
 package + "\n" + "=" * len(package)
)
blocks.append(
"|travis| |coveralls| |pypi| |version| |commit|" + (" |downloads|" if downloads else "")
)

blocks.append(
 ".. |travis| image:: https://api.travis-ci.org/samirelanduk/{}.svg?branch={}".format(package, branch)
)
blocks[-1] += (
 "\n  :target: https://travis-ci.org/samirelanduk/{}/".format(package)
)
blocks.append(
 ".. |coveralls| image:: https://coveralls.io/repos/github/samirelanduk/{}/badge.svg?branch={}".format(package, branch)
)
blocks[-1] += (
 "\n  :target: https://coveralls.io/github/samirelanduk/{}/".format(package)
)
blocks.append(
".. |pypi| image:: https://img.shields.io/pypi/pyversions/{}.svg".format(package)
)
blocks[-1] += (
 "\n  :target: https://pypi.org/project/{}/".format(package)
)
blocks.append(
".. |version| image:: https://img.shields.io/pypi/v/{}.svg".format(package)
)
blocks[-1] += (
 "\n  :target: https://pypi.org/project/{}/".format(package)
)
blocks.append(
".. |commit| image:: https://img.shields.io/github/last-commit/samirelanduk/{}/{}.svg".format(package, branch)
)
blocks[-1] += (
 "\n  :target: https://github.com/samirelanduk/{}/tree/{}/".format(package, branch)
)

if downloads:
    blocks.append(
    ".. |downloads| image:: https://img.shields.io/pypi/dm/{}.svg".format(package)
    )
    blocks[-1] += (
     "\n  :target: https://pypi.org/project/{}/".format(package)
    )
    downloads = True



# Get text blocks
files = ["installing.rst", "overview.rst", "changelog.rst"]
with open("docs/source/index.rst") as f:
    block = f.read()
block = block.split("Table of Contents")[0]
blocks.append(block)
for file_name in files:
    with open("docs/source/%s" % file_name) as f:
        blocks.append(f.read())

# Remove pointless RST formatting
blocks = [re.sub(r":py:(.+?):\`~*\.(.+?)\`", r"``\2``", block) for block in blocks]

blocks[7 + downloads] = "\n".join(blocks[7 + downloads].split("\n")[2:])
# Save as README.rst
with open("README.rst", "w") as f:
    f.write("\n\n".join(blocks))
