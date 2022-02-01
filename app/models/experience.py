from config import db, ma
from marshmallow import Schema, fields

class Experience(db.Model):
    __tablename__ = "Experience"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), db.ForeignKey('Locality.id'))
    text = db.Column(db.String(128))
    longText = db.Column(db.Text)
    locality = db.Column(db.Integer)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    date = db.Column(db.DateTime)

class ExperienceVotes(db.Model):
    __tablename__ = "ExperienceVotes"
    idExperience = db.Column(db.Integer, db.ForeignKey('Experience.id'), primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    vote = db.Column(db.Integer)

class ExperienceLanguages(db.Model):
    __tablename__ = "ExperienceLanguages"
    idExperience = db.Column(db.Integer, db.ForeignKey('Experience.id'), primary_key=True)
    language = db.Column(db.String(32), primary_key=True)

class ExperienceTags(db.Model):
    __tablename__ = "ExperienceTags"
    idExperience = db.Column(db.Integer, db.ForeignKey('Experience.id'), primary_key=True)
    tag = db.Column(db.String(16), primary_key=True)

class ExperienceImages(db.Model):
    __tablename__ = "ExperienceImages"
    idExperience = db.Column(db.Integer, db.ForeignKey('Experience.id'), primary_key=True)
    image = db.Column(db.String(32), primary_key=True)

class ExperienceDates(db.Model):
    __tablename__ = "ExperienceDates"
    idExperience = db.Column(db.Integer, db.ForeignKey('Experience.id'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    availablePlaces = db.Column(db.Integer)

class ExperienceBooks(db.Model):
    __tablename__ = "ExperienceBooks"
    idExperience = db.Column(db.Integer, db.ForeignKey('Experience.id'), primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    date = db.Column(db.DateTime, db.ForeignKey('ExperienceDates.date'), primary_key=True)
    places = db.Column(db.Integer)

class ExperienceImagesSchema(Schema):
    image = fields.String()

class ExperienceVotesSchema(Schema):
    vote = fields.Integer()

class ExperienceTagsSchema(Schema):
    tag = fields.String()

class ExperienceDatesSchema(Schema):
    idExperience = fields.Integer()
    date = fields.DateTime()
    availablePlaces = fields.Integer()
    

class ExperienceBooksSchema(Schema):
    places = fields.Integer()

class ExperienceLanguagesSchema(Schema):
    language = fields.String()

class ExperienceBookedSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    date = fields.DateTime()
    places = fields.Integer()

class ExperienceSchema(Schema):
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