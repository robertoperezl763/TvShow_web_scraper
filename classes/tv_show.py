from typing import List
from .season import Season
from services import fetchTableID
from config import TARGET_ROLES


class TvShow:
  def __init__(self, tv_show_title: str, season_count):
    self.tv_show_title = tv_show_title
    self.season_count = season_count
    self.seasons: List[Season] = []

  def add_season(self, season: Season):
    self.seasons.append(season)

  def getShowJSON(self):
    return {
        'tvshow_name': self.tv_show_title
    }

  def getTvShowId(self):
    if not hasattr(self, 'tv_show_id'):
      self.tv_show_id = fetchTableID('TV_Show', [('tvshow_name', self.tv_show_title)])
    return self.tv_show_id

  def getSeasonJSON(self):
    #gets all sql data for all season in this tv show
    return [
        {
         'tv_show_id': self.getTvShowId(),
         **season.getSeasonData()
        }
        for season in self.seasons
    ]


  def getAllPeopleJSON(self):
    #gets all the sql data for all people in the entire object
    allPeople = set()

    #season level crew data
    for season in self.seasons:
      for role_list in [season.director, season.executive_producer, season.screenwriter]:
        for person in role_list:
          allPeople.add((person.strip(), None)) #Crew will not get value for character name

      #episode level ALL people
      for episode in season.episodes:
        #episode level CREW Pople
        for crew in TARGET_ROLES:
          crew_name = episode.getCrew(crew)
          if crew_name:
            allPeople.add((crew_name.strip(), None))

        #Episode level Actors People
        for actor in episode.actors:
          allPeople.add((actor.actorName.strip(), actor.characterName.strip()))

    return [
        {
            "person_name": name,
            "character_name": characterName
        }
        for name, characterName in allPeople
    ]


  def getEpisodesJSON(self):
    return [
        episode_data
        for season in self.seasons
        for episode_data in season.getAllSeasonEpisodesData()
    ]

  def getEpisodeActorsJSON(self):
    return [
        aggregate_actors
        for season in self.seasons
        for aggregate_actors in season.getSeasonEpisodeActors()
    ]


  def getEpisodeReviewsJSON(self):
    return [
        review
        for season in self.seasons
        for review in season.getSeasonEpisodeReviews()
    ]

  def getSeasonCrewJSON(self):
    return [
        season_crew
        for season in self.seasons
        for season_crew in season.getSeasonCrews()
    ]