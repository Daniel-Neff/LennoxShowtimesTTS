import requests
import calendar
from bs4 import BeautifulSoup, NavigableString
from gtts import gTTS
from datetime import date

def main():
    URL = "https://tickets.phoenixtheatres.com/browsing/Cinemas/Details/3503"
    page = requests.get(URL)

    today = date.today().strftime("%A, %d %B %Y")

    soup = BeautifulSoup(page.content, "html.parser")
    result = process_soup(soup, today)
    tts = gTTS(result, tld='com', lang='en', slow ='true')
    tts.save(today + '.mp3')

def process_soup(soup, today):

    # Pull each movie listed
    moviesoup = soup.find_all("div", attrs={"class":"film-showtimes"})
    moviesAndTimes = {} 

    for movie in moviesoup:
        process_movie(movie, moviesAndTimes, today)
        
    dictString = str(moviesAndTimes)
    strResult = str('Lennox movie times for today, ' + today + ' are ' + dictString[:-1])
    print(strResult)
    return(strResult)

def process_movie(movie, moviesAndTimes, today):

    filmTitle = movie.find("h3", attrs={"class":"film-title"}) 
    filmTitleStr = filmTitle.text
    sessionDateSoup = movie.find_all("h4", attrs={"class":"session-date"})  
    for session in sessionDateSoup:
        # Site lists multiple days for each movie; check if session date is for current day
        if session.text == today:    
            process_session(session, filmTitleStr, moviesAndTimes)

def process_session(session, filmTitleStr, moviesAndTimes):
    sessionTimeSoup = session.next_sibling

    # Navigate whitespace to get to showtimes
    while (isinstance(sessionTimeSoup, NavigableString)):
        sessionTimeSoup = sessionTimeSoup.next_sibling
            
    # Add each showtime to list, then add film title and list to dictionary
    timeSoup = sessionTimeSoup.find_all("time")
    timeList = []
    for time in timeSoup:
        # Assume times are PM, only add AM if it is found
        if time.text[-2:] == "AM":
             timeList.append(time.text)
        else:
             timeList.append(time.text[:-3])

    title = process_title(filmTitleStr)
    moviesAndTimes.update({title: timeList})

def process_title(filmTitleStr):

    # Rearranges movie titles to have "The" in the beginning if applicable
    if len(filmTitleStr) > 3 and filmTitleStr[-3:] == "The":
        return "The " + filmTitleStr[:-5]
    elif len(filmTitleStr) > 8 and filmTitleStr[-8:-5] == "The":
        return "The " + filmTitleStr[:-10] + " IMAX"
    elif len(filmTitleStr) > 15 and filmTitleStr[-15:-12] == "The":
        return "The " + filmTitleStr[:-17] + " Dolby Atmos"
    else:
        return filmTitleStr

main()