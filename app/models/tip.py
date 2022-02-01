from config import db, ma
from marshmallow import Schema, fields

class Tip(db.Model):
    __tablename__ = "Tip"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), db.ForeignKey('Locality.id'))
    text = db.Column(db.Text)
    locality = db.Column(db.Integer)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    date = db.Column(db.DateTime)

class TipVotes(db.Model):
    __tablename__ = "TipVotes"
    idTip = db.Column(db.Integer, db.ForeignKey('Tip.id'), primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    vote = db.Column(db.Integer)

class TipLanguages(db.Model):
    __tablename__ = "TipLanguages"
    idTip = db.Column(db.Integer, db.ForeignKey('Tip.id'), primary_key=True)
    language = db.Column(db.String(32), primary_key=True)

class TipTags(db.Model):
    __tablename__ = "TipTags"
    idTip = db.Column(db.Integer, db.ForeignKey('Tip.id'), primary_key=True)
    tag = db.Column(db.String(16), primary_key=True)

class TipVotesSchema(Schema):
    vote = fields.Integer()

class TipTagsSchema(Schema):
    tag = fields.String()

class TipLanguagesSchema(Schema):
    language = fields.String()

class TipSchema(Schema):
    id = fields.Integer()
    idUser = fields.Integer()
    text = fields.String()
    title = fields.String()
    date = fields.DateTime()
    username = fields.String()
    country = fields.String()
    province = fields.String()
    city = fields.String()
    tags = fields.String()