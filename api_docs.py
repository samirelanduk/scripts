#! /usr/bin/env python3

import sys
import os
import re
import subprocess
import glob
print("")


def get_python_files(path):
	return [".".join(f.split(".")[:-1]) for f in os.listdir(path)
	 if f.endswith(".py") and "__" not in f]


# Get package
package = os.getcwd().split(os.path.sep)[-1]


# Get sub-packages
sub_packages = [f for f in os.listdir(package) if "." not in f and "__" not in f]


# Create api file
api_lines = ["Full API", "--------", ""]
for sub_package in sub_packages:
	api_lines.append(sub_package.title())
	api_lines.append("~" * len(sub_package))
	api_lines.append("")
	api_lines.append(".. toctree ::")
	for py in get_python_files("{}/{}".format(package, sub_package)):
		api_lines.append("\tapi/" + py)
	api_lines.append("\n")
with open("docs/source/api.rst", "w") as f:
	f.write("\n".join(api_lines))


# Create individual files
for sub_package in sub_packages:
	files = get_python_files("{}/{}".format(package, sub_package))
	for py in files:
		file_lines = []
		file_lines.append("{}.{}.{}".format(package, sub_package, py))
		file_lines.append("-" * len(file_lines[0]))
		file_lines.append("")
		file_lines.append(".. automodule:: {}.{}.{}".format(package, sub_package, py))
		file_lines.append("\t:members:")
		file_lines.append("\t:inherited-members:")
		with open("docs/source/api/{}.rst".format(py), "w") as f:
			f.write("\n".join(file_lines))
