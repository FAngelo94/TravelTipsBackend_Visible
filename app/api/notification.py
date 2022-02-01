import os
import base64
import json
from flask import make_response, abort, request
from sqlalchemy import func, or_
from config import db
from models.notification import Notification, NotificationSchema
from models.user import User, UserSchema
import utils
from dictionary._dictionary import dictionary
import connexion
from datetime import datetime
import api._common as common

def _check_valid_data(data):
    if data['title'] and len(data['title']) <= 64 and data['text'] and len(data['text']) <= 128:
        return True
    abort(400, dictionary(language, "Fill all fields correctly"))

def create(language, data):
    """Create 1 new Notification

    :param language: Language using in client
    :type language: str
    :param data: Data passed to create a new place
    :type data: dict | bytes
    """
    if data['idUser'] and data['title'] and len(data['title'])<=64 and data['text'] and len(data['text'])<=64:
        newNotification = Notification(idUser = data['idUser'], title = data['title'], text = data['text'])
        db.session.add(newNotification)
        db.session.commit()
        return make_response(
                { 'message': 'Ok', 'status':200, "id": newNotification.id},
                200 
            )
    else:
        abort(400, dictionary(language, "Fill all fields"))

def delete(language, idNotification):
    """Delete 1 Notification

    :param language: Language using in client
    :type language: str
    :param idNotification: Id that identify the notification we want to delete
    :type idNotification: integer
    """
    user = common.check_token(connexion, language)
    result = Notification.query.filter(Notification.idUser == user.id, Notification.id == idNotification).delete()
    db.session.commit()
    return make_response(
                { 'message': 'Ok', 'status':200, "result": result},
                200 
            )

def read(language):
    """Return the list of notifications

    :param language: Language using in client
    :type language: str
    """
    user = common.check_token(connexion, language)
    notifications = Notification.query.filter(Notification.idUser == user.id)
    notifications = NotificationSchema(many=True).dump(notifications)
    return make_response(
                { 'message': 'Ok', 'status':200, "notifications": notifications},
                200 
            )

def visualized(language, idNotification):
    """Set 1 Notification visualized

    :param language: Language using in client
    :type language: str
    :param idNotification: Id that identify the notification we want to set visualized
    :type idNotification: integer
    """
    user = common.check_token(connexion, language)
    notification = Notification.query.filter(Notification.idUser == user.id, Notification.id == idNotification).one_or_none()
    if notification is None:
        abort(400, dictionary(language, "Notification not exist"))
    newNotification = Notification(idUser = notification.idUser, title = notification.title, text = notification.text, visualized = 1)
    newNotification.id = notification.id
    db.session.merge(newNotification)
    db.session.commit()
    return make_response(
                { 'message': 'Ok', 'status':200, "id": newNotification.id},
                200 
            )