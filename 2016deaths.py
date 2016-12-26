from bs4 import BeautifulSoup
import requests
import calendar

years = [2016]
months = [calendar.month_name[n + 1] for n in range(12)]

data = []
for year in years:
    for month in months[:3]:
        # Get page
        html = requests.get(
         "https://en.wikipedia.org/wiki/Deaths_in_%s_%i" % (month, year)
        ).text
        page = BeautifulSoup(html, "html.parser")

        # Get content
        content = page.find("div", {"id": "mw-content-text"})

        # Get <li> for each death
        month_data = {
         "year": year,
         "month": month
        }
        day = 1
        list_started = False
        for child in content.findChildren(recursive=False):
            if child.name == "h2":
                list_started = True
            if child.name == "h3":
                day = int(child.text.split("[")[0])
                month_data[day] = []
            elif child.name == "ul" and list_started:
                for item in child.find_all("li"):
                    month_data[day].append(item)
        data.append(month_data)
