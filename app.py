from flask import Flask,request,jsonify
from flask_restful import Api
from dbmodels import User, db,Venue ,VenueBookingData, EventDb
from flask_cors import CORS, cross_origin
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import func
from sqlalchemy import and_ , or_

app=Flask(__name__)
from flask_migrate import Migrate

migrate = Migrate(app, db)

CORS(app, support_credentials=True)

#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://gxjfdchnmhuirn:ea19d6889c206194deea9dacb409fc57a2a1d265e3ce0ba669caff392485ebd5@ec2-3-219-19-205.compute-1.amazonaws.com:5432/dd705kk5bnt131'

api=Api(app)
db.init_app(app)

@app.before_first_request
def create_Table():
    db.create_all()

#=================================> Registration and login related apis

@app.route('/register', methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def registartion():
  if(request.method == 'POST'):
    req = request.get_json()
    username = req['username']
    firstname = req['firstname']
    lastname = req['lastname']
    email = req['email']
    password = req['password']
    role = req['role']
    educationLevel = req['educationLevel']
    if((db.session.query(User).filter(User.username == username).count() == 0)
    and (db.session.query(User).filter(User.email == email).count() == 0)):
      data = User(email,username,firstname,lastname,password,role,educationLevel)
      db.session.add(data)
      db.session.commit()
      return {"message" : "Success" , "statusCode" : 200}
    else:
      return {"message" : "Username or Email already exists" , "statusCode" : 200}
  else:
    return {"message" : "Failure" , "statusCode" : 404}

@app.route('/userDetails/<string:email>' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def userDetails(email):
  if(request.method == 'GET'):
    if db.session.query(User).filter(User.email == email).count() == 1:
      userDetail = User.query.filter_by(email = email).first()
      return {"message" : "Success" , "data" : userDetail.jsonUserDetails() ,"statusCode" : 200}
    elif db.session.query(User).filter(User.email == email).count() == 0:
      return {"message" : "email not found" , "data" : {} , "statusCode" : 200}
    else:
      return {"message" : "Something went wrong" , "data" : {} ,"statusCode" : 200}
  else:
    return {"message" : "Bad Request" , "data" : {} ,"statusCode" : 500}

@app.route('/organiserDetails/<string:email>' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def organiserDetails(email):
  if(request.method == 'GET'):
    if db.session.query(User).filter(User.email == email).count() == 1:
      userDetail = User.query.filter_by(email = email).first()
      return {"message" : "Success" , "data" : userDetail.jsonUserDetails() ,"statusCode" : 200}
    elif db.session.query(User).filter(User.email == email).count() == 0:
      return {"message" : "email not found" , "data" : {} , "statusCode" : 200}
    else:
      return {"message" : "Something went wrong" , "data" : {} ,"statusCode" : 200}
  else:
    return {"message" : "Bad Request" , "data" : {} ,"statusCode" : 500}

@app.route('/userDetailsChange' , methods = ['PUT'])
@cross_origin(supports_credentials=True)
def userDetailsChange():
  if(request.method == 'PUT'):
    req = request.get_json()
    email = req['email']
    firstname = req['firstname']
    lastname = req['lastname']
    educationLevel = req['educationLevel']
    if db.session.query(User).filter(User.email == email).count() == 1:
      userDetail = User.query.filter_by(email = email).first()
      firtsnameUser = userDetail.firstname
      lastnameUser = userDetail.lastname
      educationLevelUser = userDetail.educationLevel
      if(len(firstname) != 0 and firtsnameUser!= firstname):
        userDetail.firstname = firstname
        flag_modified(userDetail, "firstname")
      if(len(lastname) != 0 and lastnameUser != lastname):
        userDetail.lastname = lastname
        flag_modified(userDetail, "lastname")
      if(len(educationLevel) != 0 and educationLevelUser != educationLevel):
        userDetail.educationLevel = educationLevel
        flag_modified(userDetail, "educationLevel")
      db.session.merge(userDetail)
      db.session.commit()
      return {"message" : "Success" ,"statusCode" : 200}
    elif db.session.query(User).filter(User.email == email).count() == 0:
      return {"message" : "email not found","statusCode" : 200}

@app.route('/getAll' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def getAll():
  if(request.method == 'GET'):
    userdetail =  db.session.query(User).all()
    return {"message" : "Success" ,"statusCode" : 200 , "User":list(x.json() for x in userdetail)}

@app.route('/login' , methods = ['POST'])
@cross_origin(supports_credentials=True)
def login():
  if(request.method == 'POST'):
    req = request.get_json()
    email = req['email']
    password = req['password']
    if(db.session.query(User).filter(User.email == email).count() == 1):
      userDetail = User.query.filter_by(email = email).first()
      if(userDetail.password == password):
        role = str(userDetail.role)
        return {"message" : "Success" , "statusCode" : 200 , "role" : role}
      else:
        return {"message" : "Wrong Password" , "statusCode" : 200}
    else:
      return {"message" : "Email Doesn't exist" , "statusCode" : 200}
  else:
    return {"message" : "Failure" , "statusCode" : 404}


#============================================> Venue Apis

@app.route('/createVenue' , methods = ['POST'])
@cross_origin(supports_credentials=True)
def createVenue():
  if(request.method == 'POST'):
    req = request.get_json()
    venueName = req['venueName']
    description = req['description']
    bookingFee = req['bookingFee']
    location = req['location']
    maximumOccupancy = req['maximumOccupancy']
    createdBy = req['createdBy']
    venueBookingStart = req['venueBookingStart']
    venueBookingEnd = req['venueBookingEnd']
    venueBookingStart = venueBookingStart[:2]
    venueBookingEnd = venueBookingEnd[:2]
    venueNumber = ""
    if(db.session.query(Venue.venueNumber).all()):
      venueNumber = db.session.query(func.max(Venue.venueNumber)).first()
      venueNumber  = venueNumber[0]
      vNumber = int(venueNumber[1:]) + 1
      venueNumber = venueNumber[0] + str(vNumber)
    else:
      venueNumber = "V10000"

    eventData = Venue(venueNumber,venueName,description,bookingFee,location,
    maximumOccupancy,createdBy,venueBookingStart,venueBookingEnd)
    db.session.add(eventData)
    db.session.commit()
    return {"message" : "Success" , "statusCode" : 200}



@app.route('/getAllVenues' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def getAllVenues():
  if(request.method == 'GET'):
    userdetail =  db.session.query(Venue).all()
    return {"message" : "Success" , "statusCode" : 200 ,"Venues":list(x.json() for x in userdetail)}

@app.route('/venueOwnerVenues/<email>' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def venueOwner(email):
  if(request.method == 'GET'):
    venueDetails =  db.session.query(Venue).filter(Venue.createdBy == email).all()
    return {"message" : "Success" ,"statusCode" : 200,"Venues":list(x.json() for x in venueDetails)}

@app.route('/removeVenues/<venueNumber>' , methods = ['DELETE'])
@cross_origin(supports_credentials=True)
def removeVenues(venueNumber):
  if(request.method == 'DELETE'):
    if(db.session.query(Venue).filter(Venue.venueNumber == venueNumber).count() == 1):
      db.session.query(Venue).filter(Venue.venueNumber == venueNumber).delete()
      db.session.commit()
      return {"message" : "Success" , "statusCode" : 200}
    else:
      return {"message" : "Something went wrong" , "statusCode" : 404}

#===========================================================> Event Apis

@app.route('/createEvent' , methods = ['POST'])
@cross_origin(supports_credentials=True)
def createEvent_2():
  if(request.method == 'POST'):
    req = request.get_json()
    eventName = req['eventName']
    description = req['description']
    eventEntryFee = req['eventEntryFee']
    location = req['location']
    maximumOccupancy = req['maximumOccupancy']
    createdBy = req['createdBy']
    eventDate = req['eventDate']
    eventStartTime = req['eventStartTime']
    eventEndTime = req['eventEndTime']
    venueNumber = req['venueNumber']
    graduationLevel= req['graduationLevel']
    eventNumber = ""
    print("before Event Number")
    if(db.session.query(EventDb).all()):
      eventNumber = db.session.query(func.max(EventDb.eventNumber)).first()
      eventNumber  = eventNumber[0]
      eNumber = int(eventNumber[1:]) + 1
      eventNumber = eventNumber[0] + str(eNumber)
    else:
      eventNumber = "E10000"
    print(eventNumber)
    venueDetails = db.session.query(Venue).filter(Venue.venueNumber == venueNumber).first()
    print("venue call")
    venueName = venueDetails.venueName
    venueLocation = venueDetails.location
    venueBookingFee = venueDetails.bookingFee
    eventData_2 = EventDb(eventNumber,eventName,description,eventEntryFee,location,
    maximumOccupancy,createdBy,eventDate,eventStartTime,eventEndTime,venueNumber,
    venueName,venueLocation,venueBookingFee,graduationLevel)
    print("before Event setting")
    db.session.add(eventData_2)
    db.session.commit()
    return {"message" : "Success" , "statusCode" : 200}  

@app.route('/unregisterEvent' , methods = ['POST'])
@cross_origin(supports_credentials=True)
def unregisterEvent():
  if(request.method == 'POST'):
    req = request.get_json()
    userEmail = req['userEmail']
    eventNumber = req['eventNumber']
    eventDetails = db.session.query(EventDb).filter(EventDb.eventNumber == eventNumber).first()
    if(eventDetails.usersAttending):
      if(userEmail not in eventDetails.usersAttending):
        return {"message" : "User not registered" , "statusCode" : 200}

    if(eventDetails.usersAttending):
      if(userEmail in eventDetails.usersAttending):
        eventDetails.usersAttending.remove(userEmail)
        if(eventDetails.waitList and len(eventDetails.waitList) > 0):
          joinedUser = eventDetails.waitList.pop(0)
          if(eventDetails.usersAttending):
            eventDetails.usersAttending.append(joinedUser)
          else:
            eventDetails.usersAttending = [joinedUser]
        else:
          eventDetails.numberAttending -= 1
          pass
      else:
        return {"message" : "Something went wrong" , "statusCode" : 404}
        
    '''userDetails = db.session.query(User).filter(User.email == userEmail).first()
    if(userDetails.eventsAttending):
      if(eventNumber in userDetails.eventsAttending):
        userDetails.eventsAttending.remove(eventNumber)
    '''
    
    flag_modified(eventDetails, "usersAttending")
    flag_modified(eventDetails, "numberAttending")
    flag_modified(eventDetails, "waitList")
    db.session.merge(eventDetails)
    '''flag_modified(userDetails, "eventsAttending")
    db.session.merge(userDetails)'''
    db.session.commit()
    return {"message" : "Success" , "statusCode" : 200}

  else:
    return {"message" : "Something went wrong" , "statusCode" : 404}


@app.route('/registerEvent' , methods = ['PUT'])
@cross_origin(supports_credentials=True)
def registerEvent():
  if(request.method == 'PUT'):
    req = request.get_json()
    userEmail = req['userEmail']
    eventNumber = req['eventNumber']
    eventDetails = db.session.query(EventDb).filter(EventDb.eventNumber == eventNumber).first()
    if(eventDetails.usersAttending):
      if(userEmail in eventDetails.usersAttending):
        return {"message" : "User Already Registered" , "statusCode" : 200}
    if(eventDetails.numberAttending and eventDetails.numberAttending >= eventDetails.maximumOccupancy):
      if(eventDetails.waitList and len(eventDetails.waitList) >= eventDetails.maximumOccupancy//2):
        return {"message" : "Waitlist Full" , "statusCode" : 202}
      else:
        if(eventDetails.waitList):
          eventDetails.waitList.append(userEmail)
        else:
          eventDetails.waitList = [userEmail]
        
        flag_modified(eventDetails, "waitList") 
        db.session.merge(eventDetails)
        db.session.commit()
        return {"message" : "Waitlisted" , "statusCode" : 201}
    if(eventDetails.usersAttending):
      for i in eventDetails.usersAttending:
        if(i == userEmail):
          return {"message" : "User Already Registered" , "statusCode" : 200}
      eventDetails.usersAttending.append(userEmail)
    else:
      eventDetails.usersAttending = [userEmail]
    
    if(eventDetails.numberAttending):
      eventDetails.numberAttending += 1
    else:
      eventDetails.numberAttending = len(eventDetails.usersAttending)

    flag_modified(eventDetails, "usersAttending")
    flag_modified(eventDetails, "numberAttending")
    db.session.merge(eventDetails)
    
    '''userDetails = db.session.query(User).filter(User.email == userEmail).first()
    if(userDetails.eventsAttending):
      userDetails.eventsAttending.append(eventNumber)
    else:
      userDetails.eventsAttending = [eventNumber]

    flag_modified(userDetails, "eventsAttending")
    db.session.merge(userDetails)'''
    db.session.commit()

    return {"message" : "Success" , "statusCode" : 200}
  else:
    return {"message" : "Something went wrong" , "statusCode" : 404}

@app.route('/getAllEvents' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def getAllEvents():
  if(request.method == 'GET'):
    userEmail  = request.args.get('userEmail', None)
    event_owner_detail =  db.session.query(EventDb).all()
    data = []
    if(event_owner_detail is not None):
      for details in event_owner_detail:
        if(details.usersAttending is None):
          data.append(details)
        elif(details.usersAttending and (userEmail not in details.usersAttending)):
          data.append(details)
    return {"message" : "Success" , "statusCode" : 200 ,"Events":list(x.json() for x in data)}   

@app.route('/getEventsAttending' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def getEventsAttending():
  if(request.method == 'GET'):
    userEmail  = request.args.get('userEmail', None)
    event_owner_detail =  db.session.query(EventDb).all()
    data = []
    if(event_owner_detail is not None):
      for details in event_owner_detail:
        if(details.usersAttending and (userEmail in details.usersAttending)):
          data.append(details)
    return {"message" : "Success" , "statusCode" : 200 ,"Events":list(x.json() for x in data)}

@app.route('/removeEvents/<eventNumber>' , methods = ['DELETE'])
@cross_origin(supports_credentials=True)
def removeEvents(eventNumber):
  if(request.method == 'DELETE'):
    if(db.session.query(EventDb).filter(EventDb.eventNumber == eventNumber).count() == 1):
      db.session.query(EventDb).filter(EventDb.eventNumber == eventNumber).delete()
      db.session.commit()
      return {"message" : "Success" , "statusCode" : 200}
    else:
      return {"message" : "Something went wrong" , "statusCode" : 404}


#===========================================================> "Venue Booking APIs"

@app.route('/bookVenue' , methods = ['POST'])
@cross_origin(supports_credentials=True)
def bookVenue():
  if(request.method == 'POST'):
    req = request.get_json()
    venueNumber = req['venueNumber']
    bookedBy = req['bookedBy']
    venueBookedDate = req['venueBookedDate']
    venueBookingStart = req['venueBookingStart']
    venueBookingEnd = req['venueBookingEnd']
    if(db.session.query(Venue).filter(Venue.venueNumber == venueNumber).count() != 1):
      return {"message" : "Wrong Venue Number" , "statusCode" : 404}
    else:
      venueDetails = db.session.query(Venue).filter(Venue.venueNumber == venueNumber).first()
      venueName = venueDetails.venueName
      bookingFee = venueDetails.bookingFee
      location = venueDetails.location
      maximumOccupancy = venueDetails.maximumOccupancy
      venueStartTime = venueDetails.venueBookingStart
      venueEndTime =venueDetails.venueBookingEnd
      venueBookingId = ""
      if(db.session.query(VenueBookingData.venueBookingId).all()):
        venueBookingId = db.session.query(func.max(VenueBookingData.venueBookingId)).first()
        venueBookingId  = venueBookingId[0]
        bookingNumber = int(venueBookingId[4:]) + 1
        venueBookingId = venueBookingId[0] + str(bookingNumber)
      else:
        venueBookingId = "VBEF100000"
      #Change code but might be used later
      '''prevBookingDetails = db.session.query(VenueBookingData).filter(and_(VenueBookingData.venueNumber == venueNumber , 
      VenueBookingData.venueBookedDate == venueBookedDate)).all()
      if(prevBookingDetails is not None):
        for prevdetails in prevBookingDetails:
          a = [i for i in range(int(prevdetails.venueBookingStart) , int(prevdetails.venueBookingEnd) + 1)]
          if((int(venueBookingEnd) in a) and (not (int(venueBookingEnd) == int(prevdetails.venueBookingStart)))):
            return {"message" : "Venue is already booked in those timings" , "statusCode" : 200}
          elif((int(venueBookingStart) in a) and (not (int(venueBookingStart) == int(prevdetails.venueBookingEnd)))):
            return {"message" : "Venue is already booked in those timings" , "statusCode" : 200}
        bookingData = VenueBookingData(venueBookingId,venueNumber,venueName,bookingFee,location,
        maximumOccupancy,bookedBy,venueBookedDate,venueStartTime,venueEndTime,venueBookingStart,venueBookingEnd)
        db.session.add(bookingData)
        db.session.commit()
        return {"message" : "Success" , "statusCode" : 200}
      else:'''
      bookingData = VenueBookingData(venueBookingId,venueNumber,venueName,bookingFee,location,
      maximumOccupancy,bookedBy,venueBookedDate,venueStartTime,venueEndTime,venueBookingStart,venueBookingEnd)
      db.session.add(bookingData)
      db.session.commit()
      return {"message" : "Success" , "statusCode" : 200 , "venueNumber": venueNumber,
      "venueLocation" : location,
      "venueBookingStart" : venueBookingStart,"venueBookingEnd":venueBookingEnd,
      "maximumOccupancy" : maximumOccupancy}
  else:
      return {"message" : "Something went wrong" , "statusCode" : 404}


@app.route('/venueBookingDetails' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def venueBookingDetails():
  if(request.method == 'GET'):
    venueNumber  = request.args.get('venueNumber', None)
    venueBookedDate  = request.args.get('venueBookedDate', None)
    venueDetails = db.session.query(VenueBookingData).filter(and_(VenueBookingData.venueNumber == venueNumber ,
    VenueBookingData.venueBookedDate == venueBookedDate)).all()
    data = []
    if(venueDetails is not None):
      for details in venueDetails:
        data.append([details.venueBookingStart , details.venueBookingEnd])
      return {"message" : "Success" , "statusCode" : 200 , "bookedTimings" : data}
    else:
      return {"message" : "Something went wrong" , "statusCode" : 404}

  else:
      return {"message" : "Something went wrong" , "statusCode" : 404}




#==========================================> Event flow

@app.route('/venueSearch' , methods = ['GET'])
@cross_origin(supports_credentials=True)
def venueSearch():
  if(request.method == 'GET'):
    date  = request.args.get('date', None)
    startTime  = request.args.get('startTime', None)
    endTime = request.args.get('endTime', None)
    maximumOccupancy = request.args.get('maximumOccupancy', None)
    maximumOccupancy = int(maximumOccupancy)
    startTime = int(startTime[:2])
    endTime = int(endTime[:2])
    data = []
    venueNumberDetails = []
    venueDetails = db.session.query(Venue).all()
    for details in venueDetails:
      if(int(details.maximumOccupancy) >= maximumOccupancy and int(details.venueBookingStart) <= startTime and int(details.venueBookingEnd) >= endTime):
        data.append(details)
        venueNumberDetails.append(details.venueNumber)
    prevBookingDetails = db.session.query(VenueBookingData).filter(VenueBookingData.venueBookedDate == date).all()
    outliers = set()
    if(prevBookingDetails is not None):
      for details in prevBookingDetails:
        a = [i for i in range(int(details.venueBookingStart) , int(details.venueBookingEnd)+1)]
        if((int(endTime) in a) and (not (int(endTime) == int(details.venueBookingStart)))):
          outliers.add(details.venueNumber)
          continue
        elif((int(startTime) in a) and (not (int(startTime) == int(details.venueBookingEnd)))):
          outliers.add(details.venueNumber)
          continue
      out = []
      for i in data:
        if(not (i.venueNumber in outliers)):
          out.append(i)
      
      return {"message":"Success","statusCode": 200, "data" : list(x.json() for x in out)}
    else:
      return {"message":"Success","statusCode": 200, "data" : list(x.json() for x in data)}

#=========================================================================> END
if __name__=='__main__':
    app.run(debug = True)