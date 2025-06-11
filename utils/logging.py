from datetime import datetime

def print_and_log(filePath: str, suffix: str = '', message: str = '') -> None:
    """
    Helper Function to write to a txt file in order to keep a log of previews times ive ran this script.
    """
    try:
        with open(filePath, "a", encoding="UTF-8") as file:
            file.write(suffix + message + '\n')

    except FileNotFoundError as e:
        print(f'ERROR WITH LOGS: could not find dir/file ["{filePath}"]. The expected message will be printed but not saved...')
    except Exception as e:
        print(e)
    print(suffix + message + '\n')

def get_new_filePath() -> str:
    """
    Returns a string for the path to newly created logs.txt file
    file is unique with date and timestamp
    """

    tempString = "-".join(str(datetime.now()).split())
    
    datetimeString = tempString.replace(':', ';')
    newFilePath = 'logs/'+datetimeString+'.txt'

    return newFilePath


