from utils import appendZero


def getURI(seasonNum: int, episodeNum: int = None) -> str:
  base = 's'
  episodeBase = '/e'
  seasonNumberURI = ''
  episodeNumberURI = ''
  if(seasonNum < 10):
    seasonNumberURI = appendZero(seasonNum)
  else:
    seasonNumberURI = str(seasonNum)

  if(episodeNum):
    if (episodeNum < 10):
      episodeNumberURI = episodeBase + appendZero(episodeNum)
    else:
      episodeNumberURI = episodeBase + str(episodeNum)

  return base+seasonNumberURI+episodeNumberURI