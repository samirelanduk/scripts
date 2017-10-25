#! /usr/bin/env python3

import sys
import os
import re
print("")

# Add badges
blocks = []
package = os.getcwd().split(os.path.sep)[-1]
blocks.append(
 ".. |travis| image:: https://api.travis-ci.org/samirelanduk/{}.svg?branch=master".format(package)
)
blocks.append(
 ".. |coveralls| image:: https://coveralls.io/repos/github/samirelanduk/{}/badge.svg?branch=master".format(package)
)
blocks.append(
".. |pypi| image:: https://img.shields.io/pypi/pyversions/{}.svg".format(package)
)
blocks.append(
"\n|travis| |coveralls| |pypi|"
)


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


# Save as README.rst
with open("README.rst", "w") as f:
    f.write("\n\n".join(blocks))
