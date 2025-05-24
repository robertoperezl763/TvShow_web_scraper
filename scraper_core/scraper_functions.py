from classes import TvShow, Season, Episode, Actor
from bs4 import BeautifulSoup
from utils import getHTTPResponse, isValidateHTML, parseDate
from config import TARGET_ROLES
from typing import (
    Union
)

def getSoup(url:str) -> Union[BeautifulSoup, None]:
    """
    Returns a BeautifulSoup object for the given URL if the response is valid HTML.
    """
    response = getHTTPResponse(url)
    if(isValidateHTML(response)):
        return BeautifulSoup(response.text, features="html.parser")

    else:
        print(f'Attempting url: ["{url}"]. Recieved invalid HTML')
        return None
        

def getTvShowData(soup: BeautifulSoup) -> TvShow:
    seasonTotal = int(soup.find_all('rt-text', slot='metadataProp')[-1].text.split()[0])
    seriesName = soup.find('media-hero', mediatype='TvSeries').find('rt-text', context='heading').text

    return TvShow(tv_show_title=seriesName, season_count=seasonTotal)

def getSeasonData(soup: BeautifulSoup) -> Season:
    """
    Returns a Season object with all Season relevant data.
    """
    #Find Show Name and Series Name
    rtTitle = soup.find('rt-text', context="heading", slot='title')
    thisSeason = Season(season_name = rtTitle.text)

    #finds the rotten tomato critics score for the season
    rtCriticReview = soup.find('div',class_='media-scorecard no-border').find('rt-text', slot='criticsScore').text[:-1]
    thisSeason.rt_rating = float(rtCriticReview)/100


    #finds the release date within media info for the season
    releaseDayRaw = soup.dl.find_all('div', class_='category-wrap')[-1].dd.find('rt-text').text
    thisSeason.release_date = parseDate(releaseDayRaw)

    #finds episode count for the given season
    thisSeason.total_episodes = len(soup.find('carousel-slider', tilewidth='240px').find_all('tile-episode'))

    #appends all crew member data for Director, Exec Prod, and Screenwriter for season

    for row in soup.dl.find_all("div", class_='category-wrap'):
        if(row.dt.contents[1].text in TARGET_ROLES):
            thisSeason.add_role_data(
                role=row.dt.contents[1].text,
                value= [
                    x.text 
                    for x in row.dd.find_all('rt-link')
                ]
            )

    return thisSeason

def getEpisodeData(soup: BeautifulSoup, episodeNumber: int) -> Episode:
    """
    Returns an Episode object with all Episode relevant data.
    """
    #get epsiode name
    episode_name = soup.find('rt-text', slot='episodeTitle').text

    thisEpisode = Episode(episode_number=episodeNumber, episode_name=episode_name)

    #get rt rating for ep
    thisEpisode.rt_rating = float(soup.find('rt-text', slot='criticsScore').text[:-1])/100

    #get release date for ep
    thisEpisode.release_date = parseDate(soup.dl.find_all('div')[-1].dd.find('rt-text').text)

    #get #1 director, #1 Exec, and #1 Screenwritter for ep
    for row in soup.dl.find_all("div", class_='category-wrap'):
        if(row.dt.contents[1].text in TARGET_ROLES):
            thisEpisode.add_role_data(
                role=row.dt.contents[1].text, 
                value=row.dd.find('rt-link').text
            )

    #get list of reviews for episode
    for reviewCard in soup.find('carousel-slider', attrs={'data-qa': 'carousel'}).find_all('media-review-card-critic'):
        thisEpisode.reviews.append([
            review 
            for review in reviewCard.find('drawer-more', slot='reviewQuote').find('rt-text').stripped_strings
        ][0]) #appending the stripped version (removing '\n') of each review into the review array for thisEpisode
 

    #get list of all actors for the episode
    thisEpisode.actors = [
        Actor(
            actorName=character.div.find('p', class_='name').text,
            characterName=character.div.find('p', class_='role').text
        )
        for character in soup.find('section', class_='cast-and-crew').find_all('a')
    ]

    return thisEpisode