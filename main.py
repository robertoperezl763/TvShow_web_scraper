from scraper_core import (
    getSoup, 
    getURI,
    getTvShowData,
    getSeasonData,
    getEpisodeData
)
from classes import Season, Episode
from time import sleep
from random import randint
from services import upsertTableValues
from utils import print_and_log, get_new_filePath

url_main = 'https://www.rottentomatoes.com/tv/the_walking_dead/'

UPLOAD_DATA = True
logfile = get_new_filePath()

# # get TV Show Soup
tvShowSoup = getSoup(url_main)
if tvShowSoup:
    thisTVShow = getTvShowData(tvShowSoup)
else: 
    exit()

for seasonNum in range(1, thisTVShow.season_count + 1):
    uri = getURI(seasonNum)
    urlSeason = url_main + uri

    seasonSoup = getSoup(urlSeason)
    if seasonSoup:
        thisSeason = getSeasonData(seasonSoup)
        print_and_log(logfile, '+++DATA GATHERED: ', str(thisSeason.getSeason__all()))
    else:
        print_and_log(logfile, '---ERROR WITH URL: ', 'Attempting url: {urlSeason} for Season ["{seasonNum}"]. Could not get Soup, adding missing values for row') 
        # print(f'Attempting url: {urlSeason} for Season ["{seasonNum}"]. Could not get Soup, adding missing values for row')
        thisSeason = Season('Season' + str(seasonNum))
        thisTVShow.add_season(thisSeason)
    
    for episodeNum in range(1, thisSeason.total_episodes + 1):
        uri = getURI(seasonNum=seasonNum, episodeNum=episodeNum)
        urlEpisode = url_main + uri

        episodeSoup = getSoup(urlEpisode)

        if episodeSoup:
            thisEpisode = getEpisodeData(episodeSoup, episodeNum)
            print_and_log(logfile, '+++++DATA GATHERED: ', str(thisEpisode.getEpisode__all()))
        else:
            print_and_log(logfile, '---ERROR WITH URL: ', f'Attempting url: {urlEpisode} for Episode Number ["{episodeNum}"] in Season Number ["{seasonNum}"]. Could not get Soup, adding missing values for row' )
            # print(f'Attempting url: {urlEpisode} for Episode Number ["{episodeNum}"] in Season Number ["{seasonNum}"]. Could not get Soup, adding missing values for row')
            thisEpisode = Episode(episode_number=episodeNum)
            thisSeason.add_episode(thisEpisode)
            continue
        
        # appends the episode object for current iteration onto the current iteration of the seaosn object
        thisSeason.add_episode(thisEpisode)
        
        # stops the code for an anywhere from 1 to 5 seconds to attempt to avoid server req overload 
        sleep(randint(1,5))

    # append the finalized Season object to the current TV Show Object
    thisTVShow.add_season(thisSeason)
    
    # stops the code for an anywhere from 1 to 5 seconds to attempt to avoid server req overload 
    sleep(randint(1,5))


########
# Run all required functions to transform data from scraped object into relational database 
########
if UPLOAD_DATA:
    # Upload all people data
    print_and_log(logfile, '########## NOW ATTEMPTING TO UPLOAD DATA ##########', '')


    allPeopleUpload = thisTVShow.getAllPeopleJSON()
    print_and_log(logfile, '+DATA UPLOADING - ALL PEOPLE: ', str(allPeopleUpload))
    # print(f' {allPeopleUpload}')
    upsertTableValues(
        data_to_insert=allPeopleUpload,
        supabase_table_name='People',
        on_conflict_arg=['person_name']
    )

    # Upload TV Show
    tvShowUpload = thisTVShow.getShowJSON()
    print_and_log(logfile, '+DATA UPLOADING - TV_SHOW: ', str(tvShowUpload))
    # print(f'+DATA UPLOADING - TV_SHOW: {tvShowUpload}')
    upsertTableValues(
        data_to_insert=tvShowUpload,
        supabase_table_name='TV_Show',
        on_conflict_arg=['tvshow_name']
    )


    # Upload Season Data
    seasonsUpload = thisTVShow.getSeasonJSON()
    print_and_log(logfile, '+DATA UPLOADING - SEASONS: ', str(seasonsUpload))
    # print(f'+DATA UPLOADING - SEASONS: {seasonsUpload}')
    upsertTableValues(
        data_to_insert=seasonsUpload,
        supabase_table_name='Seasons',
        on_conflict_arg=['season_name']
    )

    # Upload Episode Data
    episodesUpload = thisTVShow.getEpisodesJSON()
    print_and_log(logfile, '+DATA UPLOADING - EPISODES: ', str(episodesUpload))
    # print(f'+DATA UPLOADING - EPISODES: {episodesUpload}')
    upsertTableValues(
        data_to_insert=episodesUpload,
        supabase_table_name='Episodes',
        on_conflict_arg=['episode_and_name']
    )


    # Upload Episode-Review table
    episodeReviewsUpload = thisTVShow.getEpisodeReviewsJSON()
    print_and_log(logfile, '+DATA UPLOADING - EPISODE_REVIEWS: ', str(episodeReviewsUpload))
    # print(f'+DATA UPLOADING - EPISODE_REVIEWS: {episodeReviewsUpload}')
    upsertTableValues(
        data_to_insert=episodeReviewsUpload,
        supabase_table_name='Episode_Reviews',
        on_conflict_arg=['review_text']
    )


    # Upload Episode-Actors table
    episodeActorsUpload = thisTVShow.getEpisodeActorsJSON()
    print_and_log(logfile, '+DATA UPLOADING - EPISODE_ACTORS: ', str(episodeActorsUpload))
    # print(f'+DATA UPLOADING - EPISODE_ACTORS: {episodeActorsUpload}')
    upsertTableValues(
        data_to_insert=episodeActorsUpload,
        supabase_table_name='Episode_Actors'
    )


    # Upload Season-Crew Table
    seasonCrewUpload = thisTVShow.getSeasonCrewJSON()
    print_and_log(logfile, '+DATA UPLOADING - SEASON_CREW: ', str(seasonCrewUpload))
    # print(f'+DATA UPLOADING - SEASON_CREW: {seasonCrewUpload}')
    upsertTableValues(
        data_to_insert=seasonCrewUpload,
        supabase_table_name='Season_Crew'
    )