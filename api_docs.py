#! /usr/bin/env python3

import sys
import os
import re
import subprocess
import glob
print("")


def get_python_files(path):
	files = []
	for filename in os.listdir(path):
		if filename.endswith(".py") and "__" not in filename:
			with open("{}/{}".format(path, filename)) as f:
				data = f.read()
			if data[:3] == '"""':
				files.append(".".join(filename.split(".")[:-1]))
	return files


def create_file(name):
	file_lines = []
	file_lines.append(name)
	file_lines.append("-" * len(file_lines[0]))
	file_lines.append("")
	file_lines.append(".. automodule:: {}".format(name))
	file_lines.append("\t:members:")
	file_lines.append("\t:inherited-members:")
	with open("docs/source/api/{}.rst".format(name.split(".")[-1]), "w") as f:
		f.write("\n".join(file_lines))


def add_toctree(lines, files):
	lines.append(".. toctree ::")
	for py in files:
		lines.append("\tapi/" + py)
	lines.append("\n")


# Get package
package = os.getcwd().split(os.path.sep)[-1]


# Get files
files = get_python_files(package)

# Get sub-packages
sub_packages = [
 f for f in os.listdir(package) if "." not in f and "__" not in f
]


# Create api file
api_lines = ["Full API", "--------", ""]
if files:
	add_toctree(api_lines, files)
for sub_package in sub_packages:
	api_lines.append(sub_package.title())
	api_lines.append("~" * len(sub_package))
	api_lines.append("")
	add_toctree(
	 api_lines, get_python_files("{}/{}".format(package, sub_package))
	)
with open("docs/source/api.rst", "w") as f:
	f.write("\n".join(api_lines))


# Create individual files
for pyfile in files:
	create_file("{}.{}".format(package, pyfile))
for sub_package in sub_packages:
	files = get_python_files("{}/{}".format(package, sub_package))
	for pyfile in files:
		create_file("{}.{}.{}".format(package, sub_package, pyfile))
