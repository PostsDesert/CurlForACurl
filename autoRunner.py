from imleaguesAPI import *
from datetime import datetime as dt
import datetime
from jsonManager import JsonManager 

def autoRunner():
  jsonManager = JsonManager()
  config = jsonManager.readConfig()

  for i in range(len(config['users'])):
    print(f"Registering events for user: {config['users'][i]['email']}")
    studentId = config['users'][i]['studentId']

    todayEventIds = []
    for j in range(len(config['users'][i]['eventIds'])):
      startDate = datetime.date.fromisoformat(config['users'][i]['eventIds'][j]['registrationDay'])
      if startDate == dt.today().date():
        todayEventId = config['users'][i]['eventIds'].pop(j)
        todayEventIds.append(todayEventId['eventId'])

    jsonManager.writeConfig(config)
    
    if todayEventIds:
      imLeaguesAPI = ImLeaguesAPI(config['users'][i]['email'], config['users'][i]['password'], config['users'][i]['schoolId'])
      for eventId in todayEventIds:
        try:
          print(imLeaguesAPI.registerEvent(studentId, eventId))
        except EventRegistrationError as e:
          print(f"Error: Event Id: {eventId} Message: {e}")
    else:
      print(f"No events today for user: {config['users'][i]['email']}")
            



  
    



autoRunner()
