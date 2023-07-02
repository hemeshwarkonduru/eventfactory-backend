from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TIME
db= SQLAlchemy()

class User(db.Model):
    _tablename_='user'
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    username=db.Column(db.String(80),unique=True,nullable=False)
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100))
    role=db.Column(db.String(80),nullable=False)
    educationLevel = db.Column(db.String(100))
    eventsAttending = db.Column(db.PickleType)

    def __init__(self,email,username,firstname,lastname,password,role,educationLevel):
        self.email=email
        self.firstname = firstname
        self.username=username
        self.password=password
        self.firstname = firstname
        self.lastname = lastname
        self.role=role
        self.educationLevel = educationLevel

    def json(self):
        return {"email":self.email, "username": self.username, "firstname" : self.firstname,
                 "lastname" : self.lastname,"password": str(self.password), "role":self.role,
                 "educationLevel" : self.educationLevel}

    def jsonUserDetails(self):
        return {"email":self.email, "username": self.username, "firstname" : self.firstname,
                 "lastname" : self.lastname, "role":self.role,
                 "educationLevel" : self.educationLevel,"eventsAttending" : self.eventsAttending}


class Venue(db.Model):
    _tablename_='venue'
    id = db.Column(db.Integer, primary_key=True)
    venueNumber = db.Column(db.String(20),unique=True,nullable=False)
    venueName = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(1000))
    bookingFee = db.Column(db.Integer)
    location = db.Column(db.String(100),nullable=False)
    maximumOccupancy = db.Column(db.Integer,nullable=False)
    createdBy = db.Column(db.String(100))
    venueBookingStart = db.Column(db.String(20))
    venueBookingEnd = db.Column(db.String(20))

    
    def __init__(self,venueNumber,venueName,description,bookingFee,location,
    maximumOccupancy,createdBy,venueBookingStart,venueBookingEnd):
        self.venueNumber=venueNumber
        self.venueName = venueName
        self.description=description
        self.bookingFee=bookingFee
        self.location = location
        self.maximumOccupancy=maximumOccupancy
        self.createdBy = createdBy
        self.venueBookingStart = venueBookingStart
        self.venueBookingEnd = venueBookingEnd

    def json(self):
        return {"venueNumber":self.venueNumber, "venueName": self.venueName, 
        "description" : self.description,
                 "bookingFee" : self.bookingFee,"location": self.location, "maximumOccupancy":self.maximumOccupancy,
                 "createdBy" : self.createdBy,"venueBookingStart" : self.venueBookingStart,
                 "venueBookingEnd" : self.venueBookingEnd}



class VenueBookingData(db.Model):
    _tablename_='venueBookingDb'
    id = db.Column(db.Integer, primary_key=True)
    venueBookingId = db.Column(db.String, nullable=False)
    venueNumber = db.Column(db.String(20),nullable=False)
    venueName = db.Column(db.String(100),nullable=False)
    bookingFee = db.Column(db.Integer)
    location = db.Column(db.String(100))
    maximumOccupancy = db.Column(db.Integer,nullable=False)
    bookedBy = db.Column(db.String(100) , nullable = False)
    venueBookedDate = db.Column(db.String(100) , nullable = False)
    venueStartTime = db.Column(db.String(20))
    venueEndTime = db.Column(db.String(20))
    venueBookingStart = db.Column(db.String(20))
    venueBookingEnd = db.Column(db.String(20))

    def __init__(self,venueBookingId,venueNumber,venueName,bookingFee,location,
    maximumOccupancy,bookedBy,venueBookedDate,venueStartTime,venueEndTime,venueBookingStart,venueBookingEnd):
        self.venueBookingId = venueBookingId
        self.venueNumber=venueNumber
        self.venueName = venueName
        self.bookingFee=bookingFee
        self.location = location
        self.maximumOccupancy=maximumOccupancy
        self.bookedBy = bookedBy
        self.venueBookedDate = venueBookedDate
        self.venueStartTime = venueStartTime
        self.venueEndTime = venueEndTime
        self.venueBookingStart = venueBookingStart
        self.venueBookingEnd = venueBookingEnd

    def json(self):
        return {"venueBookingId" : self.venueBookingId,"venueNumber" : self.venueNumber
        ,"venueName" : self.venueName,"bookingFee" : self.bookingFee,"location" : self.location,
        "maximumOccupancy" : self.maximumOccupancy,"bookedBy" : self.bookedBy
        ,"venueBookedDate" : self.venueBookedDate,"venueStartTime" : self.venueStartTime,
        "venueEndTime" : self.venueEndTime,"venueBookingStart" : self.venueBookingStart
        ,"venueBookingEnd" : self.venueBookingEnd}


class EventDb(db.Model):
    _tablename_ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    eventNumber = db.Column(db.String(20),unique=True,nullable=False)
    eventName = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(1000))
    eventEntryFee = db.Column(db.Integer)
    location = db.Column(db.String(100),nullable=False)
    maximumOccupancy = db.Column(db.Integer,nullable=False)
    createdBy = db.Column(db.String(100))
    eventDate = db.Column(db.String(100))
    eventStartTime = db.Column(db.String(20))
    eventEndTime = db.Column(db.String(20))
    venueNumber = db.Column(db.String(100),nullable=False)
    venueName = db.Column(db.String(100))
    venueLocation = db.Column(db.String(100),nullable=False)
    venueBookingFee = db.Column(db.Integer)
    graduationLevel= db.Column(db.String(20))
    usersAttending = db.Column(db.PickleType)
    numberAttending = db.Column(db.Integer)
    waitList = db.Column(db.PickleType)

    def __init__(self,eventNumber,eventName,description,eventEntryFee,location,
    maximumOccupancy,createdBy,eventDate,eventStartTime,eventEndTime,venueNumber,
    venueName,venueLocation,venueBookingFee,graduationLevel):
        self.eventNumber=eventNumber
        self.eventName = eventName
        self.description=description
        self.eventEntryFee=eventEntryFee
        self.location = location
        self.maximumOccupancy=maximumOccupancy
        self.createdBy = createdBy
        self.eventDate = eventDate
        self.eventStartTime = eventStartTime
        self.eventEndTime = eventEndTime
        self.venueNumber = venueNumber
        self.venueName = venueName
        self.venueLocation = venueLocation
        self.venueBookingFee = venueBookingFee
        self.graduationLevel=graduationLevel

    def json(self):
        return {"eventNumber":self.eventNumber, "eventName": self.eventName, 
        "description" : self.description,
                 "eventEntryFee" : self.eventEntryFee,"location": self.location, "maximumOccupancy":self.maximumOccupancy,
                 "createdBy" : self.createdBy,"eventDate" : self.eventDate,"eventStartTime" : self.eventStartTime,
                 "eventEndTime" : self.eventEndTime,"venueNumber" : self.venueNumber,"venueName" :self.venueName
                 ,"venueLocation" : self.venueLocation,"venueBookingFee":self.venueBookingFee,
                 "graduationLevel" : self.graduationLevel,"usersAttending" : self.usersAttending,
                 "numberAttending":self.numberAttending,"waitList" : self.waitList}                 


'''class EventBooking(db.Model):
    _tablename_='event_booking'
    id = db.Column(db.Integer, primary_key=True)
    eventBookingId = db.Column(db.String, nullable=False)
    eventNumber = db.Column(db.String(20),unique=True,nullable=False)
    eventEntryFee = db.Column(db.Integer)
    location = db.Column(db.String(100),nullable=False)
    maximumOccupancy = db.Column(db.Integer,nullable=False)
    createdBy = db.Column(db.String(100))
    eventDate = db.Column(db.String(100))
    eventStartTime = db.Column(db.String(20))
    eventEndTime = db.Column(db.String(20))
    venueNumber = db.Column(db.String(100),nullable=False)
    graduationLevel= db.Column(db.String(20))
    
    def __init__(self,eventBookingId,eventNumber,eventEntryFee,location,
    maximumOccupancy,createdBy,eventDate,eventStartTime,eventEndTime,venueNumber,
    graduationLevel):
        self.eventBookingId = eventBookingId
        self.eventNumber=eventNumber
        self.eventEntryFee=eventEntryFee
        self.location = location
        self.maximumOccupancy=maximumOccupancy
        self.createdBy = createdBy
        self.eventDate = eventDate
        self.eventStartTime = eventStartTime
        self.eventEndTime = eventEndTime
        self.venueNumber = venueNumber
        self.graduationLevel=graduationLevel

    def json(self):
        return {"eventNumber":self.eventNumber, 
                 "eventEntryFee" : self.eventEntryFee,"location": self.location, "maximumOccupancy":self.maximumOccupancy,
                 "createdBy" : self.createdBy,"eventDate" : self.eventDate,"eventStartTime" : self.eventStartTime,
                 "eventEndTime" : self.eventEndTime,"venueNumber" : self.venueNumber,
                 "graduationLevel" : self.graduationLevel}          '''       

'''class UserEventDb(db.Model):
    _tablename_='user_event'
    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(100),unique=True,nullable=False)
    eventAttending = db.Column(db.PickleType)

    def __init__(self,userEmail,eventAttending):
        self.userEmail = userEmail
        self.eventAttending = eventAttending

    def json(self):
        return {"userEmail" : self.userEmail , "eventAttending" : self.eventAttending}'''