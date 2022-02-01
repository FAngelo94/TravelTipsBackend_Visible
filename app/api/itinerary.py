import os
import base64
import json
from flask import make_response, abort, request
from sqlalchemy import func, or_
from config import db
from models.itinerary import Itinerary, ItineraryVotes, ItineraryLanguages, ItineraryTags, ItineraryImages, ItineraryTagsSchema, ItinerarySchema, ItineraryVotesSchema, ItineraryLanguagesSchema, ItineraryImagesSchema
from models.locality import Locality, LocalitySchema
from models.user import User, UserSchema
import utils
from dictionary._dictionary import dictionary
import connexion
from datetime import datetime
import api._common as common

def _abort_creation(message, id):
    Itinerary.query.filter(Itinerary.id == id).delete()
    ItineraryLanguages.query.filter(ItineraryLanguages.idItinerary == id).delete()
    ItineraryTags.query.filter(ItineraryTags.idItinerary == id).delete()
    db.session.commit()
    abort(400, message)

def _check_valid_data(language, itinerary):
    if itinerary["text"] and itinerary["title"] and itinerary["country"] and itinerary["province"] and itinerary["city"] and itinerary["languages"] and len(itinerary["languages"]) > 0 and itinerary["tags"] and len(itinerary["tags"]) > 0 and itinerary["images"] and len(itinerary["images"]) > 0:
        return True
    abort(400, dictionary(language, "Fill all fields correctly"))

def create(language, data):
    user = common.check_token(connexion, language)

    itinerary = common.from_data_to_structure(data)
    _check_valid_data(language,itinerary)
    ## Add locality of Itinerary
    idLocality = common.add_locality(db, itinerary["country"], itinerary["province"], itinerary["city"])
    ## Add Itinerary
    now = datetime.now()
    dtString = now.strftime("%Y-%m-%d %H:%M:%S")
    newItinerary = Itinerary(title=itinerary["title"], text=itinerary["text"], longText=itinerary["longText"], idUser=user.id, date=dtString, locality=idLocality)
    # Add itinerary to the database
    db.session.add(newItinerary)
    db.session.commit()

    ## Add Itinerary Images
    # check images type before save them
    for index,image in enumerate(itinerary["images"]):
        if(image != ""):
            imgtype = image.split(",")[0].split("/")[1].split(";")[0]
            if not(imgtype in ['jpeg','jpg','png']):
                _abort_creation((dictionary(language, "Image type not valid")), newItinerary.id)
        else:
            _abort_creation((dictionary(language, "Compile all fields")), newItinerary.id)
    # image type is ok, save them
    for index,image in enumerate(itinerary["images"]):
        imgtype = image.split(",")[0].split("/")[1].split(";")[0]
        imgdata = base64.b64decode(image.split(",")[1])
        path = common.IMAGES_PATH
        filename = "itinerary_" + str(newItinerary.id) + "_" + str(index) + "." + imgtype
        with open((path + filename), 'wb') as f:
            f.write(imgdata)
        newImage = ItineraryImages(idItinerary = newItinerary.id, image = filename)
        db.session.add(newImage)
    db.session.commit()

    ## Add Itinerary Languages
    for l in itinerary["languages"]:
        if(l!=""):
            newLanguage = ItineraryLanguages(idItinerary = newItinerary.id, language=l)
            # merge the new object into the old and commit it to the db
            db.session.add(newLanguage)
    db.session.commit()

    ## Add Itinerary Tags
    for t in itinerary["tags"]:
        if(t != ""):
            newTag = ItineraryTags(idItinerary = newItinerary.id, tag=t)
            # merge the new object into the old and commit it to the db
            db.session.add(newTag)
    db.session.commit() 
    
    return make_response(
        { 'message': 'Ok', 'status':200, "id": newItinerary.id, "date":dtString },
        200 
    )

def delete(language, idItinerary):
    user = common.check_token(connexion, language)
    oldItinerary = Itinerary.query.filter(Itinerary.id == idItinerary).filter(Itinerary.idUser == user.id).one_or_none()
    
    if oldItinerary is None:
        abort(400, dictionary(language,"Itinerary not found"))
    else:
        ## Remove Itinerary Languages
        ItineraryLanguages.query.filter(ItineraryLanguages.idItinerary == idItinerary).delete()
        db.session.commit()

        ## Remove Itinerary Tags
        ItineraryTags.query.filter(ItineraryTags.idItinerary == idItinerary).delete()
        db.session.commit()

        ## Remove Itinerary Images
        images = ItineraryImages.query.filter(ItineraryImages.idItinerary == idItinerary)
        images = ItineraryImagesSchema(many=True).dump(images)
        for image in images:
            os.remove(common.IMAGES_PATH+image['image'])
        ItineraryImages.query.filter(ItineraryImages.idItinerary == idItinerary).delete()
        db.session.commit()

        ## Remove Itinerary
        common.remove_locality(db, oldItinerary.locality)
        Itinerary.query.filter(Itinerary.id == idItinerary).delete()
        db.session.commit()

        return make_response(
                { 'message': 'Ok', 'status':200 },
                200
            )

def read_list(language, data={}):
    token = None
    user = None
    if 'token' in connexion.request.headers:
        user = common.check_token(connexion, language)
        
    itineraries = db.session.query(Itinerary.id,Itinerary.title, Itinerary.text,  Itinerary.longText, Itinerary.date, User.username, User.id.label("idUser"), Locality.country, Locality.province, Locality.city).filter(Itinerary.idUser==User.id, Itinerary.locality==Locality.id)
    itineraries = common.apply_common_filters(db, data, itineraries, "Itinerary")
    itineraries = itineraries.order_by(Itinerary.date.desc())
    itineraries = itineraries.group_by(Itinerary.id,Itinerary.title, Itinerary.text, Itinerary.longText, Itinerary.date, User.username, Locality.country, Locality.province, Locality.city)
    schema = ItinerarySchema(many=True)
    dataItineraries = schema.dump(itineraries)
    
    for t in dataItineraries:
        # Get all tags for this itinerary
        tags = db.session.query(ItineraryTags.tag).filter(ItineraryTags.idItinerary==t['id'])
        dataTags = ItineraryTagsSchema(many=True).dump(tags)
        arrayTags = ""
        for d in dataTags:
            arrayTags += "#"+d['tag']+" "
        t['tags'] = arrayTags[:-1]
        # Get all languages for this itinerary
        languages = db.session.query(ItineraryLanguages.language).filter(ItineraryLanguages.idItinerary==t['id'])
        dataLanguage = ItineraryLanguagesSchema(many=True).dump(languages)
        arrayLanguages = ""
        for d in dataLanguage:
            arrayLanguages += d['language'] +", "
        t['languages'] = arrayLanguages[:-2]
        # Get all vote for this itineraries
        votes = db.session.query(ItineraryVotes.vote).filter(ItineraryVotes.idItinerary==t['id'])
        dataAverageVote = ItineraryVotesSchema(many=True).dump(votes)
        if len(dataAverageVote) > 0:
            averageVote = 0
            for d in dataAverageVote:
                averageVote += d["vote"]
            t['averageVote'] = averageVote/len(dataAverageVote)
        else:
            t['averageVote'] = -1
        
        # Get user vote
        if not(user is None):
            votes = db.session.query(ItineraryVotes.vote).filter(ItineraryVotes.idItinerary==t['id'],ItineraryVotes.idUser==user.id).one_or_none()
            userVote = ItineraryVotesSchema().dump(votes)
            if not(userVote is None) and userVote!={}:
                t['voted'] = userVote['vote']  
            else: 
                t['voted'] = -1
        
        # Images
        images = ItineraryImages.query.filter(ItineraryImages.idItinerary == t["id"])
        images = ItineraryImagesSchema(many=True).dump(images)
        arrayImage = []
        for image in images:
            arrayImage.append(image['image'])
        t['images'] = arrayImage

    return make_response(
         { 'message': 'Ok', 'status':200, "itineraries": dataItineraries },
         200
      )

def update(language, data):
    user = common.check_token(connexion, language)
    oldItinerary = Itinerary.query.filter(Itinerary.id == data.get("id")).filter(Itinerary.idUser == user.id).one_or_none()
    
    if oldItinerary is None:
        abort(400, dictionary(language,"Itinerary not found"))
    else:
        itinerary = common.from_data_to_structure(data)
        _check_valid_data(language,itinerary)
        ## Update Itinerary Images
        # check images type before update them
        for index,image in enumerate(itinerary["images"]):
            if(image != ""):
                imgtype = image.split(",")[0].split("/")[1].split(";")[0]
                if not(imgtype in ['jpeg','jpg','png']):
                    abort(400, dictionary(language,"Image type not valid"))
            else:
                abort(400, dictionary(language,"Error image"))
        # First remove images
        images = ItineraryImages.query.filter(ItineraryImages.idItinerary == itinerary["id"])
        images = ItineraryImagesSchema(many=True).dump(images)
        for image in images:
            os.remove(common.IMAGES_PATH+image['image'])
        ItineraryImages.query.filter(ItineraryImages.idItinerary == itinerary["id"]).delete()
        db.session.commit()
        # Then add
        for index,image in enumerate(itinerary["images"]):
            imgtype = image.split(",")[0].split("/")[1].split(";")[0]
            imgdata = base64.b64decode(image.split(",")[1])
            path = common.IMAGES_PATH
            filename = "itinerary_" + str(itinerary["id"]) + "_" + str(index) + "." + imgtype
            with open((path + filename), 'wb') as f:
                f.write(imgdata)
            newImage = ItineraryImages(idItinerary = itinerary["id"], image = filename)
            db.session.add(newImage)
        db.session.commit()
        
        ## Update locality of Itinerary
        common.remove_locality(db, oldItinerary.locality)
        idLocality = common.add_locality(db, itinerary["country"], itinerary["province"], itinerary["city"])
        ## Update Itinerary
        updateItinerary = Itinerary(title=itinerary["title"], text=itinerary["text"], longText=itinerary["longText"], idUser=user.id, locality=idLocality)
        updateItinerary.id = itinerary["id"]
        # Update itinerary to the database
        db.session.merge(updateItinerary)
        db.session.commit()

        ## Update Itinerary Languages
        # First remove 
        ItineraryLanguages.query.filter(ItineraryLanguages.idItinerary == itinerary["id"]).delete()
        db.session.commit()
        # Then add languages
        for l in itinerary["languages"]:
            if(l !=""):
                newLanguage = ItineraryLanguages(idItinerary = itinerary["id"], language=l)
                # merge the new object into the old and commit it to the db
                db.session.add(newLanguage)

        ## Update Itinerary Tags
        # First remove
        ItineraryTags.query.filter(ItineraryTags.idItinerary == itinerary["id"]).delete()
        db.session.commit()
        # Then add tags
        for t in itinerary["tags"]:
            if(t !=""):
                newTag = ItineraryTags(idItinerary = itinerary["id"], tag=t)
                # merge the new object into the old and commit it to the db
                db.session.add(newTag)
        db.session.commit()

        return make_response(
            { 'message': 'Ok', 'status':200 },
            200
        )

def update_vote(language, idItinerary, vote=None):
    user = common.check_token(connexion, language)
    checkItinerary = Itinerary.query.filter(Itinerary.id == idItinerary).one_or_none()
    
    if checkItinerary is None:
        abort(400, dictionary(language, "Itinerary not found"))
    elif vote is None or vote == -1:
        ## First remove old vote if present
        ItineraryVotes.query.filter(ItineraryVotes.idItinerary == idItinerary).delete()
        db.session.commit()
        return make_response(
                { 'message': 'Ok', 'status':200 },
                200
            )
    elif vote < 0 or vote > 4:
        abort(400, dictionary(language,"Vote not valid"))
    else:
        ## First remove old vote if present
        ItineraryVotes.query.filter(ItineraryVotes.idItinerary == idItinerary, ItineraryVotes.idUser == user.id).delete()
        db.session.commit()

        ## Then add the vote
        newVote = ItineraryVotes(idItinerary=idItinerary, idUser=user.id, vote=vote)
        db.session.add(newVote)
        db.session.commit()
        return make_response(
                { 'message': 'Ok', 'status':200 },
                200
            )