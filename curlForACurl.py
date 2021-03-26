#!/usr/bin/env python3

from imleaguesAPI import *
from datetime import datetime as dt, timedelta
from jsonManager import JsonManager

class CurlForACurl:
  def __init__(self):
    self.configManager = JsonManager()

    self.config = self.configManager.readConfig()

    print("\n        Welcome to the CurlForACurl Auto Registration System!\n")
    print("Please enter your email address: ", end="")
    email = input()

    if not email:
      email = self.config['defaults']['email']

    newUser = True
    for i in range(len(self.config['users'])):
      if self.config['users'][i]['email'] == email:
        currentUser = i
        newUser = False

    if newUser == True :
      self.setUpUser(email)
      currentUser = len(self.config['users']) - 1
    else:
      self.imLeaguesAPI = ImLeaguesAPI(email, self.config['users'][currentUser]['password'], self.config['users'][currentUser]['schoolId'])
      print('\nWelcome Back ' + email + "!")

    self.addEvent(currentUser)



  def addEvent(self, currentUser):

    alreadyAddedEventIds = []
    for event in self.config['users'][currentUser]['eventIds']:
      alreadyAddedEventIds.append(event['eventId'])

    addEventId = True
    while addEventId == True:
      print("Please enter a WellRec/imLeagues event ID or link: ", end="")
      eventId = input()

      if "eventId=" in eventId:
        eventId = eventId.split("eventId=",1)[1] 

      try:
        for alreadyAddedId in alreadyAddedEventIds:
          if eventId == alreadyAddedId:
            raise EventAlreadyAdded
        
        eventInfo = self.imLeaguesAPI.getEventInfo(eventId)
        startDate = eventInfo['startDateDescription']
        startDate = dt.strptime(startDate, '%A, %B %d, %Y').date()
        if startDate <= dt.today().date():
          raise EventHasAlreadyOccurred
        elif startDate <= (dt.today().date() + timedelta(days=1)):
          try:
            print(self.imLeaguesAPI.registerEvent(self.config['users'][currentUser]['studentId'], eventId))
          except EventRegistrationError as e:
            print(f"Error: Event Id: {eventId} Message: {e}")
        else:
          # Registration opens the day before
          startDate = startDate - timedelta(days = 1)
          startDate = startDate.isoformat()
          data = {'registrationDay': startDate, 'eventId': eventId}
          self.config['users'][currentUser]['eventIds'].append(data)
          self.configManager.writeConfig(self.config)
          alreadyAddedEventIds.append(eventId)

          print(f"{eventInfo['subject']} is successful queued for preregistration on {startDate}!")

      except EventDoesNotExist:
        print("Error: The selected event does not exist. Please choose a different event.")
      except EventHasAlreadyOccurred:
        print("Error: The selected event has already occured or takes place today. Please choose a different event.")
      except EventAlreadyAdded:
        print("Error: The selected event has already been added for this user. Please choose a different event.")

      invalidResponse = True
      while invalidResponse:
        print("Would you like to preregister another event? (y/n): ", end="")
        response = str(input())[0].lower()
        if response == 'y':
          invalidResponse = False
        elif response == 'n':
          addEventId = False
          invalidResponse = False
        else:
          print('Please enter yes or no (y/n)')



  def setUpUser(self, email):
    successfulLogin = False
    while successfulLogin == False:
      print("Please enter your IMLeagues password: ", end="")
      password = input()
      print("Enter your student ID (Can be left blank if preferred): ", end="")
      studentId = input()
      print("Enter your school ID code (Leave blank if unknown): ", end="")
      schoolId = input()

      if not studentId:
        studentId = self.config['defaults']['studentId']

      if not schoolId:
        schoolId = self.config['defaults']['schoolId']

      print(f"Creating user {email}...\n")

      data = {'email': email, 
              'password': password, 
              'schoolId': schoolId, 
              'studentId': studentId,
              'eventIds': []
            }

      try:
        self.imLeaguesAPI = ImLeaguesAPI(email, password, schoolId)
        successfulLogin = True
      except AuthenticationError:
        print("Incorrect email/password")
        continue


    
    self.config['users'].append(data)
    self.configManager.writeConfig(self.config)
    



CurlForACurl()
