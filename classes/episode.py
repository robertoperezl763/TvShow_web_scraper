from typing import (
    List,
    Optional
)
from .actor import Actor
from .role_handler import RoleHandler
from services import fetchTableID
from utils import getStripStringOrNone

class Episode(RoleHandler):
  def __init__(self,
               episode_number: int,
               episode_name: Optional[str] = None,
               rt_rating: Optional[float] = None,
               release_date: Optional[str] = None,
               director: Optional[str] = None,
               executive_producer: Optional[str] = None,
               screenwriter: Optional[str] = None,
               reviews: Optional[List[str]] = None,
               actors:  Optional[List[Actor]] = None,
               ):
    self.episode_number = episode_number
    self.episode_name = episode_name
    self.rt_rating = rt_rating
    self.release_date = release_date
    self.director = director
    self.executive_producer = executive_producer
    self.screenwriter = screenwriter
    self.reviews = reviews if reviews is not None else []
    self.actors = actors if actors is not None else []

    self.episode_number_name = str(episode_number) + "_" + episode_name

  def getEpisode__all(self):
    return {
      'episode_number': self.episode_number,
      'episode_name': self.episode_name,
      'episode_number_name': self.episode_number_name,
      'rt_rating': self.rt_rating,
      'release_date': self.release_date,
      'directors': self.director,
      'executive_productes': self.executive_producer,
      'screenwriters': self.screenwriter,
      'reviews': self.reviews,
      'actors': [actor.getActorsData() for actor in self.actors]
    }

  def getCrew(self, crew_Role):
    crew_dict = {
      'Director': self.director, # type: ignore
      'Executive Producer': self.executive_producer, #type: ignore
      'Screenwriter': self.screenwriter #type: ignore
    } # type: ignore
    
    return crew_dict[crew_Role] if crew_dict[crew_Role] else None

    # match crew_Role:
    #   case 'Director':
    #     return self.director
    #   case 'Executive Producer':
    #     return self.executive_producer
    #   case 'Screenwriter':
    #     return self.screenwriter


  def getThisEpisodeData(self):
    return {
        "director_id": fetchTableID('People', [('person_name', self.director)]),
        "executive_producer_id": fetchTableID('People', [('person_name', self.executive_producer)]),
        "screenwriter_id": fetchTableID('People', [('person_name', self.screenwriter)]),
        "episode_number": self.episode_number,
        "episode_name": getStripStringOrNone(self.episode_name),
        "episode_and_name": self.episode_number_name,
        "rt_rating": self.rt_rating,
        "release_date": getStripStringOrNone(self.release_date)
    }

  def getEpisodeId(self):
    if not hasattr(self, 'episode_id'):
      self.episode_id = fetchTableID('Episodes', [
                ('episode_name', self.episode_name),
                ('episode_number', self.episode_number)
                ])
    return self.episode_id

  def getAllEpisodeReviews(self):
    return [
        {
            'episode_id': self.getEpisodeId(),
            'review_text': review
        }
        for review in self.reviews
    ]


  def getAllEpisodeActors(self):
    return [
        {
          'episode_id': self.getEpisodeId(),
          'people_id': fetchTableID('People', [
              ('person_name', actor.actorName)
          ])
        }
        for actor in self.actors
    ]