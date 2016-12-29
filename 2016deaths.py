from bs4 import BeautifulSoup
import requests
import calendar
from datetime import date
import json
import os
import numpy

years = [n + 2000 for n in range(14, 17)]
months = [calendar.month_name[n + 1] for n in range(12)]

data = {}
for year in years:
    for month_num, month in enumerate(months, start=1):
        # Get page
        html = requests.get(
         "https://en.wikipedia.org/wiki/Deaths_in_%s_%i" % (month, year)
        ).text
        page = BeautifulSoup(html, "html.parser")

        # Get content
        content = page.find("div", {"id": "mw-content-text"})

        # Get <li> for each death
        day = date(year, month_num, 1)
        data[day] = []
        list_started = False
        for child in content.findChildren(recursive=False):
            if child.name == "h2":
                list_started = True
            if child.name == "h3":
                day = date(year, month_num, int(child.text.split("[")[0]))
                data[day] = []
            elif child.name == "ul" and list_started:
                for item in child.find_all("li"):
                    first_link = item.a
                    if first_link and "/wiki/" in first_link["href"]:
                        data[day].append([
                         first_link.text,
                         first_link["href"]
                        ])

# Data analysis
deaths_per_year = []
deaths_per_month = []
for year in years:
    deaths_this_year = 0
    for day in data:
        if day.year == year:
            deaths_this_year += len(data[day])
    deaths_per_year.append(deaths_this_year)
    for month_num, month in enumerate(months, start=1):
        deaths_this_month = 0
        for day in data:
            if day.year == year and day.month == month_num:
                deaths_this_month += len(data[day])
        deaths_per_month.append(deaths_this_month)

# Output to terminal
print("Deaths per year")
for index, year in enumerate(years):
    print("\t%i: %i" % (year, deaths_per_year[index]))
print("Deaths per month")
for year_index, year in enumerate(years):
    print("\t%i:" % year, end=" ")
    for month_index, month in enumerate(months):
        print("%s:%i" % (
         months[month_index][:3],
         deaths_per_month[year_index * 12 + month_index]
        ), end=" ")
    print("")

# Replace dates with str date
str_data = dict(data)
for key in data:
    str_data[key.strftime("%Y %b %d")] = data[key]
    del str_data[key]

# Save as .json
with open("data%sdeaths.json" % os.path.sep, "w") as f:
    f.write(json.dumps(str_data))
