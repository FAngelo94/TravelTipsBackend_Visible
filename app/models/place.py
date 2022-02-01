from config import db, ma
from marshmallow import Schema, fields
import datetime

class Place(db.Model):
    __tablename__ = "Place"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), db.ForeignKey('Locality.id'))
    text = db.Column(db.String(300))
    locality = db.Column(db.Integer)
    language = db.Column(db.String(32))
    confirmed = db.Column(db.Integer, default=0)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class PlaceVotes(db.Model):
    __tablename__ = "PlaceVotes"
    idPlace = db.Column(db.Integer, db.ForeignKey('Place.id'), primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    vote = db.Column(db.Integer)

class PlaceLanguages(db.Model):
    __tablename__ = "PlaceLanguages"
    idPlace = db.Column(db.Integer, db.ForeignKey('Place.id'), primary_key=True)
    language = db.Column(db.String(32), primary_key=True)

class PlaceTags(db.Model):
    __tablename__ = "PlaceTags"
    idPlace = db.Column(db.Integer, db.ForeignKey('Place.id'), primary_key=True)
    tag = db.Column(db.String(16), primary_key=True)

class PlaceImages(db.Model):
    __tablename__ = "PlaceImages"
    idPlace = db.Column(db.Integer, db.ForeignKey('Place.id'), primary_key=True)
    image = db.Column(db.String(32), primary_key=True)

class PlaceReviews(db.Model):
    __tablename__ = "PlaceReviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPlace = db.Column(db.Integer, db.ForeignKey('Place.id'), primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    text = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class PlaceReviewsLikes(db.Model):
    __tablename__ = "PlaceReviewsLikes"
    idReview = db.Column(db.Integer, db.ForeignKey('PlaceReviews.id'), primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    like = db.Column(db.Integer)

class PlaceImagesSchema(Schema):
    image = fields.String()

class PlaceVotesSchema(Schema):
    vote = fields.Integer()

class PlaceTagsSchema(Schema):
    tag = fields.String()

class PlaceLanguagesSchema(Schema):
    language = fields.String()

class PlaceSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    title = fields.String()
    language = fields.String()
    country = fields.String()
    province = fields.String()
    city = fields.String()

class PlaceReviewsSchema(Schema):
    id = fields.Integer()
    idUser = fields.Integer()
    username = fields.String()
    text = fields.String()
    date = fields.DateTime()