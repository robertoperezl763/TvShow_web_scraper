class Actor:
  def __init__(self, actorName, characterName):
    self.actorName = actorName
    self.characterName = characterName

  def getActorsData(self):
    return{
      'ActorName': self.actorName,
      'Character Name':  self.characterName
    }
