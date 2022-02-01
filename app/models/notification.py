from config import db, ma
from marshmallow import Schema, fields
import datetime

class Notification(db.Model):
    __tablename__ = "Notification"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    visualized = db.Column(db.Integer, default=0)
    title = db.Column(db.String(64), db.ForeignKey('Locality.id'))
    text = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class NotificationSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    title = fields.String()
    visualized = fields.Integer()
    date = fields.DateTime()
