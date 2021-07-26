import requests
import calendar
from bs4 import BeautifulSoup, NavigableString
from gtts import gTTS
from datetime import date

URL = "https://tickets.phoenixtheatres.com/browsing/Cinemas/Details/3503"
date = date.today().strftime("%A, %d %B %Y")

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

moviesoup = soup.find_all("div", attrs={"class":"film-showtimes"})
moviesAndTimes = {}
for movie in moviesoup:
    filmTitle = movie.find("h3", attrs={"class":"film-title"})
    sessionDateSoup = movie.find_all("h4", attrs={"class":"session-date"})
    for session in sessionDateSoup:
        if session.text == date:
            sessionTimeSoup = session.next_sibling
            while (isinstance(sessionTimeSoup, NavigableString)):
                sessionTimeSoup = sessionTimeSoup.next_sibling
            timeSoup = sessionTimeSoup.find_all("time")
            timeList = []
            for time in timeSoup:
                timeList.append(time.text)
            moviesAndTimes.update({filmTitle.text: timeList})

dictString = str(moviesAndTimes)
strResult = str('Lennox movie times for today, ' + date + ' are ' + dictString)
tts = gTTS(strResult, tld='ca', lang='en', slow ='true')
tts.save(date + '.mp3')