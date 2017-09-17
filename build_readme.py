#! /usr/bin/env python3

import sys
import os
import re
print("")

# Get text blocks
files = ["installing.rst", "overview.rst", "changelog.rst"]
with open("docs/source/index.rst") as f:
    block = f.read()
block = block.split("Table of Contents")[0]
blocks = [block]
for file_name in files:
    with open("docs/source/%s" % file_name) as f:
        blocks.append(f.read())

# Remove pointless RST formatting
blocks = [re.sub(r":py:(.+?):\`~*\.(.+?)\`", r"``\2``", block) for block in blocks]

# Save as README.rst
with open("README.rst", "w") as f:
    f.write("\n\n".join(blocks))
