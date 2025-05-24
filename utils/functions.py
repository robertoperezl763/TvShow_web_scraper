import requests
from datetime import datetime
from typing import (
  Union
)
# returns string.strip() if string is not None and is a string, else returns None    
def getStripStringOrNone(string: str) -> Union[str, None]:
  if string and type(string) == str:
    return string.strip()
  else:
    return None
  
# requests html from given url and returns html response
def getHTTPResponse(url: str) -> Union[requests.Response, None]:
  try:
    response = requests.get(url, timeout=5)
    return response
  except TimeoutError:
    print(f'---Got no response from URL {url}')
    return 'N/A'
  except Exception as e:
    print(f'---Other Random Error: {e}')


# returns True if if response is a valid HTML response, else returns False
def isValidateHTML(response: requests.Response) -> bool:
  if(not isinstance(response, requests.Response)):
    print(f'--Invalid Response: Value given ["{response}"] not a response')
    return False
  elif(response.status_code != 200):
    print(f'--Error: Response status code recieved is NOT 200, got {response.status_code}')
    return False
  elif(not '<html' in response.text):
    print(f'--Error: Response text is not valid HTML, printing first 200 characters:\n{response.text[:200]}' )
    return False
  else:
    return True

# Returns the parsed date for a given date format into default iso format for database entry
def parseDate(scrappedDate: str, dateFormat: str = '%b %d, %Y') -> Union[str, None]:
  try:
    parsed_date = datetime.strptime(scrappedDate, dateFormat).date()
    return parsed_date.isoformat()

  except ValueError:
    print(f'---ValueError: Date String ["{scrappedDate}"] does not match date format given ["{dateFormat}"]. Verify date value or enter new dateFormat parameter.')
    return None

# Returns a string of the number given with a leading zero
def appendZero(num: int) -> str:
    try:
        return '0' + str(num)
    except Exception as e:
        print(f'---Error: {e}')
        return num

