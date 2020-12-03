#! /usr/bin/env python3

import sys
import os
import re
import subprocess
import glob
print("")

# Which package?
package = os.getcwd().split(os.path.sep)[-1]

# Get analytics code
os.chdir("docs")
with open("source/conf.py") as f:
    lines = f.read().splitlines()
    for line in lines:
        if line.startswith('analytics = "'):
            code = line.split()[2][1:-1]
            break
    else:
        print("Can't find analytics code")
        sys.exit()


# Define google analytics code
ga = """<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
  ga('create', '%s', 'auto');
  ga('send', 'pageview');
</script>"""

# Delete existing HTML files
html_files = glob.iglob('**/*.html', recursive=True)
for html_file in html_files:
    print("rm " + html_file)
    subprocess.call("rm " + html_file, shell=True)

# Build docs locally
subprocess.call("make html", shell=True)

# Add google analytics to each html file
html_files = glob.iglob('**/*.html', recursive=True)
for html_file in html_files:
    with open(html_file) as f:
        html = f.read()
    html = html.replace("</head>", (ga % code) + "</head>")
    with open(html_file, "w") as f:
        f.write(html)