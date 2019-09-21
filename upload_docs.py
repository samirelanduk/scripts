#! /usr/bin/env python3

import sys
import os
import re
import subprocess
import requests
import glob
print("")


# Which package?
package = os.getcwd().split(os.path.sep)[-1]

# Get analytics code
if len(sys.argv) > 1:
    google_analytics_code = sys.argv[1]
else:
    html = requests.get("https://{}.samireland.com/".format(package)).text
    google_analytics_code = re.findall(r"ga\('create', '(.+?)\'", html)[0]


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
os.chdir("docs")
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
    html = html.replace("</head>", (ga % google_analytics_code) + "</head>")
    with open(html_file, "w") as f:
        f.write(html)


# Remove remote files
host = "159.65.18.68" # documentation server
subprocess.call(
 "ssh %s 'rm -r ~/%s.samireland.com/*'" % (host, package), shell=True
)

# Push to server
subprocess.call(
 "scp -r build/html/* %s:~/%s.samireland.com/" % (host, package), shell=True
)
