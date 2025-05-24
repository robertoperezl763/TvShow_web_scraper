from typing import (
  List, 
  Optional
)
from .role_handler import RoleHandler
from .episode import Episode
from services import fetchTableID

class Season(RoleHandler):

  def __init__(self,
               season_name: Optional[str] = None,
               rt_rating: Optional[float] = None,
               release_date: Optional[str] = None,
               total_episodes: Optional[int] = None,
               director: Optional[List[str]] = None,
               executive_producer: Optional[List[str]] = None,
               screenwriter: Optional[List[str]] = None,
               ):
    self.season_name = season_name
    self.rt_rating = rt_rating
    self.release_date = release_date
    self.total_episodes = total_episodes
    self.director = director if director is not None else []
    self.executive_producer = executive_producer if executive_producer is not None else []
    self.screenwriter = screenwriter if screenwriter is not None else []

    self.episodes: List[Episode] = []

  def add_episode(self, episode: Episode):
    self.episodes.append(episode)

  def getSeasonId(self):
    if not hasattr(self, 'season_id'):
      self.season_id = fetchTableID('Seasons', [
          ('season_name', self.season_name.strip())
      ])
    return self.season_id

  def getAllSeasonEpisodesData(self):
    return [
        {
            'season_id': self.getSeasonId(),
            **episode.getThisEpisodeData()
        }
        for episode in self.episodes
    ]

  def getSeasonData(self):
    return {
        "season_name": self.season_name.strip(),
        "rt_rating": self.rt_rating,
        'release_date': self.release_date.strip(),
        'total_episodes': self.total_episodes
    }

  def getSeasonEpisodeActors(self):
    return [
        actors_episode_data
        for episode in self.episodes
        for actors_episode_data in episode.getAllEpisodeActors()
    ]

  def getSeasonEpisodeReviews(self):
    return [
        reviews
        for episode in self.episodes
        for reviews in episode.getAllEpisodeReviews()
    ]

  def getSeasonCrews(self):
    return [
        {
          'season_id': self.getSeasonId(),
          'people_id': fetchTableID('People', [('person_name', crew)]),
          'crew_role': role
        }
        for role, crew_list in [
          ('Director', self.director),
          ('Executive Producer', self.executive_producer),
          ('Screenwriter', self.screenwriter)
        ]
        for crew in crew_list
    ]