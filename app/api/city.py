import os
import base64
import json
from flask import make_response, abort, request
from sqlalchemy import func, or_
from config import db
from models.locality import Locality, LocalitySchema
from models.place import Place
from models.tip import Tip
from models.experience import Experience
from models.itinerary import Itinerary
from models.user import User
from models.user import User, UserSchema, UserStar
import utils
from dictionary._dictionary import dictionary
import connexion
from datetime import datetime
import api._common as common


def read_list(language, data={}):  

    """Get list of places

    Get list of places appling filters 

    :param language: Language using in client
    :type language: str
    :param data: Filters passed by the client to get only the desired places
    :type data: dict | bytes
    """
    if not("country" in data) and not("city" in data) and not("province" in data):
        return make_response(
         { 'message': 'Ok', 'status':200, "cities": [] },
         200
      )

    token = None
    user = None
    if 'token' in connexion.request.headers:
        token = connexion.request.headers['token']
        idUser = connexion.request.headers['id']
        user = User.query.filter(User.token == token, User.id == idUser).one_or_none()
    
    cities = db.session.query(Locality.id,Locality.country,Locality.province,Locality.city).order_by(Locality.id)
    if "country" in data:
        cities =cities.filter(Locality.country.like("%"+data["country"]+"%"))
    if "city" in data:
        cities =cities.filter(Locality.city.like("%"+data["city"]+"%"))
    if "province" in data:
        cities =cities.filter(Locality.province.like("%"+data["province"]+"%"))
    cities = LocalitySchema(many=True).dump(cities)

    for city in cities:
        # Get Places
        count = db.session.query(func.count(Place.id)).filter(Place.locality == city['id']).one_or_none()[0]
        city['places'] = count

        # Get Tips
        count = db.session.query(func.count(Tip.id)).filter(Tip.locality == city['id']).one_or_none()[0]
        city['tips'] = count

        # Get Experiences
        count = db.session.query(func.count(Experience.id)).filter(Experience.locality == city['id']).one_or_none()[0]
        city['experiences'] = count

        # Get Itineraries
        count = db.session.query(func.count(Itinerary.id)).filter(Itinerary.locality == city['id']).one_or_none()[0]
        city['itineraries'] = count

        # Get Travelers
        count = db.session.query(func.count(User.id)).filter(User.home == city['id']).one_or_none()[0]
        city['travelers'] = count

        # Get Matchings if user logged
        if user:
            count = db.session.query(func.count(User.id)).filter(User.home == city['id'], UserStar.idUserFollowed == User.id, UserStar.idUser == user.id).one_or_none()[0]
            city['matchings'] = count
        else:
            city['matchings'] = 0

    return make_response(
         { 'message': 'Ok', 'status':200, "cities": cities },
         200
      )
