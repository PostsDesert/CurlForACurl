import requests
import json
import uuid

class ImLeaguesAPI:
  def __init__(self, username, password, schoolId):

    self.login(username, password, schoolId)
    


  def registerEvent(self, studentId, eventId):
    loginUrl = 'https://www.imleagues.com/Services/AjaxRequestHandler.ashx?class=imLeagues.Web.Members.Services.BO.Fitness.RegisterEventBO&method=RegisterSession&paramType=imLeagues.Internal.API.VO.Input.Fitness.RegisterSessionInVO'
    cookies = {'ASP.NET_SessionId': self.sessionId}
    data = {"eventId": eventId, 
            "acceptTerms": True, 
            "sid": studentId,
            "allowSMSMessage":False,
            "allowMobileAppSMS":True,
            "allowSessionReminder":True,
            "remindDays":1}
    response = requests.post(loginUrl, data = json.dumps(data), cookies = cookies).json()

    if response['isDone'] == False:
      raise EventRegistrationError(response)

    return f"Event: {eventId} registration was successful!"



  def login(self, username, password, schoolId):
    sessionIdUrl = 'https://www.imleagues.com/Services/AjaxRequestHandlerWithWritableSession.ashx?class=imLeagues.Web.Members.Services.BO.Account.LoginBO&method=Initialize&paramType=imLeagues.Internal.API.VO.Input.InitLoginInViewVO&urlReferrer=https://www.imleagues.com/spa/account/login'
    sessionId = requests.post(sessionIdUrl, data = json.dumps({'entityType':'account'}))
    sessionId = sessionId.cookies['ASP.NET_SessionId']
    self.sessionId = sessionId
    self.schoolId = schoolId

    loginUrl = 'https://www.imleagues.com/Services/AjaxRequestHandlerWithWritableSession.ashx?class=imLeagues.Web.Members.Services.BO.Account.LoginBO&method=Login&paramType=imLeagues.Internal.API.VO.Input.LoginInSchoolVO&urlReferrer=https://www.imleagues.com/spa/account/enterpass'
    cookies = {'ASP.NET_SessionId': sessionId}
    data = {'email':    username,
            'password': password,
            'schoolId': schoolId }
    loginRequest = requests.post(loginUrl, data = json.dumps(data), cookies = cookies)
    successfulLogin = loginRequest.json()['isDone']

    if successfulLogin == False:
      raise AuthenticationError("The login was unsuccesful")

    return sessionId



  def getEventInfo(self, eventId):
    url = 'https://www.imleagues.com/Services/AjaxRequestHandler.ashx?class=imLeagues.Web.Members.Services.BO.Fitness.ViewEventBO&method=Initialize&paramType=imLeagues.Internal.API.VO.Input.Fitness.GetViewEventVMInVO'
    cookies = {'ASP.NET_SessionId': self.sessionId}
    data = {"entityType":"fitness",
             "entityId": self.schoolId, 
             "pageType":"Fitness", 
             "eventId": eventId}
    eventDetails = requests.post(url, data = json.dumps(data), cookies = cookies).json()
    
    if eventDetails['isDone'] == False:
      raise EventDoesNotExist("The requested event does not exist")

    return eventDetails['data']['sessionOutVM']['session']
    


class AuthenticationError(Exception):
  """Raised when the authentication is unsuccessful"""
  pass

class EventDoesNotExist(Exception):
  """Raised when an event does not exist"""
  pass

class EventHasAlreadyOccurred(Exception):
  """Raised when an event has already occcured"""
  pass

class EventAlreadyAdded(Exception):
  """Raised when an event is already in the config file"""

class EventRegistrationError(Exception):
  """Raised when there is an error with event registration"""