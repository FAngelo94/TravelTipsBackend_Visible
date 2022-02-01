from config import db, ma
from marshmallow import Schema, fields

class Locality(db.Model):
    __tablename__ = "Locality"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(64))
    province = db.Column(db.String(64))
    city = db.Column(db.String(64))
    counter = db.Column(db.Integer)

class LocalitySchema(Schema):
    id = fields.Integer()
    country = fields.String()
    province = fields.String()
    city = fields.String()

