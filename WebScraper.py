import requests
import calendar
from bs4 import BeautifulSoup
from datetime import date

URL = "https://tickets.phoenixtheatres.com/browsing/Cinemas/Details/3503"

fullDate = date.today().strftime("%B %d %Y")
fullDateSplit = fullDate.split()
weekday = calendar.day_name[date.today().weekday()]
formattedDate = weekday + ", " + fullDateSplit[1] + " " + fullDateSplit[0] + " " + fullDateSplit[2]
print(formattedDate)

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

movies = soup.find_all("div", attrs={"class":"film-showtimes"})

for movie in movies:
    filmTitle = movie.find("h3", attrs={"class":"film-title"})
    sessionDates = movie.find_all("h4", attrs={"class":"session-date"})
    #for session in sessionDates:
        #if session.text