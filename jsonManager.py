import json
import io
import os


class JsonManager:
  def __init__(self):
    self.filePath = 'config.json'

  def readConfig(self):
    filePath = self.filePath
    if os.path.isfile(filePath) and os.access(filePath, os.R_OK):
      with open(filePath) as json_file:
        data = json.load(json_file)
    else:
        print("Config file is either missing or is not readable, creating file...", end="\n\n")
        print("For first-time setup, please add autoRunner.py to crontab file")
        print("Ex. \'0 6 * * * cd PROJECT_DIR && python3 autoRunner.py > PROJECT_DIR/log.txt\'", end="\n\n\n")

        data = {'defaults': {'schoolId': '', 'email': '', 'studentId': '****'}, 'users': []}

        # Dictonary structure for a user
        '''
        'users': [{
          'email': '', 
          'password': '', 
          'schoolId': '', 
          'studentId': ''
          'eventIds': [
            {'registrationDay': '', 'eventId': ''}
          ]
          }]
        '''

        with io.open(os.path.join(filePath), 'w') as db_file:
            db_file.write(json.dumps(data))
        
    return data



  def writeConfig(self, data):
    filePath = self.filePath
    with open(filePath, 'w') as outfile:
      json.dump(data, outfile)