"""Builds the documentation of a project and uploads it to the server."""

import sys
import os
import subprocess
import glob

# Define google analytics code
ga = """<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
  ga('create', '%s', 'auto');
  ga('send', 'pageview');
</script>"""

# Get information from user
if len(sys.argv) < 2:
    print("\nWhere is the project?\n")
    sys.exit()
project_location = sys.argv[1]
project_name = sys.argv[1].split(os.path.sep)[-1]
if len(sys.argv) < 3:
    print("\nWhat is the google analytics code?\n")
    sys.exit()
google_analytics_code = sys.argv[2]

# Delete existing HTML files
os.chdir(project_location)
os.chdir(os.path.sep.join([project_name, "docs"]))
html_files = glob.iglob('**/*.html', recursive=True)
for html_file in html_files:
    print("rm " + html_file)
    subprocess.call("rm " + html_file, shell=True)

# Build docs locally
os.chdir(project_location)
os.chdir(os.path.sep.join([project_name, "docs"]))
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
host = "stage.samireland.com"
remote_location = "~/docs/"
subprocess.call(
 "ssh %s 'rm -r %s%s/*'" % (host, remote_location, project_name), shell=True
)

# Push to server
subprocess.call(
 "scp -r build/html/* %s:%s%s/" % (host, remote_location, project_name), shell=True
)
