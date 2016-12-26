from bs4 import BeautifulSoup
import requests
import calendar

years = [2016]
months = [calendar.month_name[n + 1] for n in range(12)]

for year in years:
    for month in months[:3]:
        # Get page
        html = requests.get(
         "https://en.wikipedia.org/wiki/Deaths_in_%s_%i" % (month, year)
        ).text
        page = BeautifulSoup(html, "html.parser")
