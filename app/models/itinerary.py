from config import db, ma
from marshmallow import Schema, fields

class Itinerary(db.Model):
    __tablename__ = "Itinerary"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), db.ForeignKey('Locality.id'))
    text = db.Column(db.String(128))
    longText = db.Column(db.Text)
    locality = db.Column(db.Integer)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    date = db.Column(db.DateTime)

class ItineraryVotes(db.Model):
    __tablename__ = "ItineraryVotes"
    idItinerary = db.Column(db.Integer, db.ForeignKey('Itinerary.id'), primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    vote = db.Column(db.Integer)

class ItineraryLanguages(db.Model):
    __tablename__ = "ItineraryLanguages"
    idItinerary = db.Column(db.Integer, db.ForeignKey('Itinerary.id'), primary_key=True)
    language = db.Column(db.String(32), primary_key=True)

class ItineraryTags(db.Model):
    __tablename__ = "ItineraryTags"
    idItinerary = db.Column(db.Integer, db.ForeignKey('Itinerary.id'), primary_key=True)
    tag = db.Column(db.String(16), primary_key=True)

class ItineraryImages(db.Model):
    __tablename__ = "ItineraryImages"
    idItinerary = db.Column(db.Integer, db.ForeignKey('Itinerary.id'), primary_key=True)
    image = db.Column(db.String(32), primary_key=True)

class ItineraryImagesSchema(Schema):
    image = fields.String()

class ItineraryVotesSchema(Schema):
    vote = fields.Integer()

class ItineraryTagsSchema(Schema):
    tag = fields.String()

class ItineraryLanguagesSchema(Schema):
    language = fields.String()

class ItinerarySchema(Schema):
    id = fields.Integer()
    idUser = fields.Integer()
    text = fields.String()
    longText = fields.String()
    title = fields.String()
    date = fields.DateTime()
    username = fields.String()
    country = fields.String()
    province = fields.String()
    city = fields.String()
    tags = fields.String()