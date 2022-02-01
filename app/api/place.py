import os
import base64
import json
from flask import make_response, abort, request
from sqlalchemy import func, or_
from config import db
from models.place import Place, PlaceVotes, PlaceTags, PlaceImages, PlaceTagsSchema, PlaceSchema, PlaceVotesSchema, PlaceImagesSchema, PlaceReviews, PlaceReviewsLikes,PlaceReviewsSchema,PlaceLanguages
from models.locality import Locality, LocalitySchema
from models.user import User, UserSchema
import utils
from dictionary._dictionary import dictionary
import connexion
from datetime import datetime
import api._common as common

def _abort_creation(message, id):
    Place.query.filter(Place.id == id).delete()
    PlaceLanguages.query.filter(PlaceLanguages.idPlace == id).delete()
    PlaceTags.query.filter(PlaceTags.idPlace == id).delete()
    db.session.commit()
    abort(400, message)

def _check_if_place_exist(language, id):
    place = Place.query.filter(Place.id == id).one_or_none()
    if place is None:
        abort(400, dictionary(language,"Place not found"))
    return place

def _check_valid_data(language, place):
    if place["text"] and len(place["text"])<=300 and place["title"] and len(place["title"])<=64 and place["country"] and place["province"] and place["city"] and place["languages"] and len(place["languages"]) <= 32 and place["tags"] and len(place["tags"]) > 0 and place["images"] and len(place["images"]) > 0:
        return True
    abort(400, dictionary(language, "Fill all fields correctly"))

def confirm_new_place(language, idPlace):  
    """Approve 1 new place

    Approve 1 place inserted 

    :param token: Token created when user logged
    :type token: str
    :param language: Language using in client
    :type language: str
    :param idPlace: Language using in client
    :type idPlace: str
    :param id: User Id connected to the token
    :type id: int

    :rtype: None
    """
    place = _check_if_place_exist(language, idPlace)
    user = common.check_token(connexion, language)
    common.check_admin(user.id)
    
    updatePlace = Place(title=place.title, text=place.text, locality=place.locality, language=place.language, idUser=place.idUser,  confirmed=1)
    updatePlace.id = idPlace
    # Update place to the database
    db.session.merge(updatePlace)
    db.session.commit()
    return make_response(
            { 'message': 'Place confirmed', 'status':200 },
            200 
        )

def create(language, data):  
    """Create 1 new place

    Create 1 new place 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to create a new place
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    place = common.from_data_to_structure(data)
    if _check_valid_data(language, place):
        ## Add locality of Place
        idLocality = common.add_locality(db, place["country"], place["province"], place["city"])
        ## Add Place
        newPlace = Place(title=place["title"], text=place["text"], idUser=user.id, locality=idLocality, language=place['languages'])
        # Add place to the database
        db.session.add(newPlace)
        db.session.commit()

        ## Add Place Images
        # Check images type before save them
        common.images_type_is_correct(place['images'])
        # image type is ok, save them
        for index,image in enumerate(place["images"]):
            imgtype = image.split(",")[0].split("/")[1].split(";")[0]
            imgdata = base64.b64decode(image.split(",")[1])
            path = common.IMAGES_PATH
            filename = "place_" + str(newPlace.id) + "_" + str(index) + "." + imgtype
            with open((path + filename), 'wb') as f:
                f.write(imgdata)
            newImage = PlaceImages(idPlace = newPlace.id, image = filename)
            db.session.add(newImage)
        db.session.commit()

        ## Add Place Languages
        for l in place["languages"]:
            if(l!=""):
                newLanguage = PlaceLanguages(idPlace = newPlace.id, language=l)
                # merge the new object into the old and commit it to the db
                db.session.add(newLanguage)
        db.session.commit()

        ## Add Place Tags
        for t in place["tags"]:
            if(t != ""):
                newTag = PlaceTags(idPlace = newPlace.id, tag=t)
                # merge the new object into the old and commit it to the db
                db.session.add(newTag)
        db.session.commit() 

        return make_response(
            { 'message': 'Ok', 'status':200, "id": newPlace.id},
            200 
        )

def create_review(language, data):  
    """Create 1 new review

    Create 1 new review 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to create a new place
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    review = {
        "idPlace": data.get("idPlace"),
        "text": data.get("text")
    }
    _check_if_place_exist(language, review['idPlace'])
    checkReview = db.session.query(PlaceReviews.id).filter(PlaceReviews.idUser == user.id, PlaceReviews.idPlace == review['idPlace']).one_or_none()

    if checkReview is None:
        newReview = PlaceReviews(idPlace = review['idPlace'], idUser = user.id, text = review['text'])
        db.session.add(newReview)
        db.session.commit()
        
        return make_response(
            { 'message': 'Ok', 'status':200, "id": newReview.id},
            200 
        )
    else:
        abort(400, dictionary(language,"User already wrote a review for this place"))

def delete(language, idPlace):  
    """Update 1 existing  place

    Delete 1 existing place 

    :param language: Language using in client
    :type language: str
    :param id: id that identify the Place
    :type id: int
    """
    user = common.check_token(connexion, language)
    oldPlace = Place.query.filter(Place.id == idPlace).filter(Place.idUser == user.id).one_or_none()
    if oldPlace is None:
        abort(400, dictionary(language,"Place not found"))
    else:
        # Remove Place Images
        images = PlaceImages.query.filter(PlaceImages.idPlace == idPlace)
        images = PlaceImagesSchema(many=True).dump(images)
        for image in images:
            os.remove(common.IMAGES_PATH+image['image'])
        PlaceImages.query.filter(PlaceImages.idPlace == idPlace).delete()
        db.session.commit()

        ## Remove Place
        common.remove_locality(db, oldPlace.locality)
        Place.query.filter(Place.id == idPlace).delete()
        db.session.commit()
        return make_response(
            { 'message': 'Ok', 'status':200 },
            200
        )

def delete_review(language, idReview):  
    """Delete 1 existing  review

    Delete 1 existing review 

    :param language: Language using in client
    :type language: str
    :param idPlace: id that identify the Place
    :type idPlace: int
    """
    user = common.check_token(connexion, language)
    checkReview = PlaceReviews.query.filter(PlaceReviews.idUser == user.id, PlaceReviews.id == idReview).delete()
    db.session.commit()
    if checkReview == 0:
        abort(400, dictionary(language,"Review not found"))
    else:
        return make_response(
            { 'message': 'Ok', 'status':200 },
            200 
        )
    
def read_list(language, confirmed=1, data={}):  
    """Get list of places

    Get list of places appling filters 

    :param language: Language using in client
    :type language: str
    :param data: Filters passed by the client to get only the desired places
    :type data: dict | bytes
    """
    token = None
    user = None
    if 'token' in connexion.request.headers:
        token = connexion.request.headers['token']
        idUser = connexion.request.headers['id']
        user = User.query.filter(User.token == token, User.id == idUser).one_or_none()
    places = db.session.query(Place.id,Place.title, Place.text,  Place.language, Place.date, Place.language, User.username, User.id.label("idUser"), Locality.country, Locality.province, Locality.city).filter(Place.idUser==User.id, Place.locality==Locality.id)
    #if(confirmed == 1 or confirmed == 0):
    #    places = places.filter(Place.confirmed == confirmed)
    places = common.apply_common_filters(db, data, places, "Place")
    places = places.order_by(Place.date.desc())
    schema = PlaceSchema(many=True)
    dataPlaces = schema.dump(places)
    
    for t in dataPlaces:
        # Get all tags for this place
        tags = db.session.query(PlaceTags.tag).filter(PlaceTags.idPlace==t['id'])
        dataTags = PlaceTagsSchema(many=True).dump(tags)
        arrayTags = ""
        for d in dataTags:
            arrayTags += "#"+d['tag']+" "
        t['tags'] = arrayTags[:-1]
        # Get all vote for this places
        votes = db.session.query(PlaceVotes.vote).filter(PlaceVotes.idPlace==t['id'])
        dataAverageVote = PlaceVotesSchema(many=True).dump(votes)
        if len(dataAverageVote) > 0:
            averageVote = 0
            for d in dataAverageVote:
                averageVote += d["vote"]
            t['averageVote'] = averageVote/len(dataAverageVote)
        else:
            t['averageVote'] = -1
        
        # Get user vote
        if not(user is None):
            votes = db.session.query(PlaceVotes.vote).filter(PlaceVotes.idPlace==t['id'],PlaceVotes.idUser==user.id).one_or_none()
            userVote = PlaceVotesSchema().dump(votes)
            if not(userVote is None) and userVote!={}:
                t['voted'] = userVote['vote']  
            else: 
                t['voted'] = -1
        
        # Images
        images = PlaceImages.query.filter(PlaceImages.idPlace == t["id"])
        images = PlaceImagesSchema(many=True).dump(images)
        arrayImage = []
        for image in images:
            arrayImage.append(image['image'])
        t['images'] = arrayImage

    return make_response(
         { 'message': 'Ok', 'status':200, "places": dataPlaces },
         200
      )

def read_reviews(language, idPlace):
    """Read all reveiws of one place

    Read all reveiws of one place 

    :param language: Language using in client
    :type language: str
    :param id: Id that identify the place we want to read reviews
    :type id: int
    """
    _check_if_place_exist(language, idPlace)

    token = None
    user = None
    if 'token' in connexion.request.headers:
        token = connexion.request.headers['token']
        idUser = connexion.request.headers['id']
        user = User.query.filter(User.token == token, User.id == idUser).one_or_none()

    reviews = db.session.query(PlaceReviews.id,PlaceReviews.date, User.username, PlaceReviews.idUser, PlaceReviews.text).filter(PlaceReviews.idPlace == idPlace, User.id == PlaceReviews.idUser)
    reviews = PlaceReviewsSchema(many=True).dump(reviews)

    for review in reviews:
        review['likes']  = db.session.query(func.count(PlaceReviewsLikes.like)).filter(PlaceReviewsLikes.idReview == review['id'],PlaceReviewsLikes.like == 1, PlaceReviewsLikes.idUser != user.id).one_or_none()[0]
        review['unlikes']  = db.session.query(func.count(PlaceReviewsLikes.like)).filter(PlaceReviewsLikes.idReview == review['id'],PlaceReviewsLikes.like == -1, PlaceReviewsLikes.idUser != user.id).one_or_none()[0]
        if user != None:
            review['liked'] = db.session.query(PlaceReviewsLikes.like).filter(PlaceReviewsLikes.idReview == review['id'],PlaceReviewsLikes.idUser == user.id).one_or_none()
            if(review['liked'] != None):
                review['liked'] = review['liked'][0]
            else:
                review['liked'] = 0
        else:
            review['liked'] = 0
        
    return make_response(
         { 'message': 'Ok', 'status':200, "reviews": reviews },
         200
      )
    
def update(language, data):  
    """Update 1 existing  place

    Update 1 existing place 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to create a new place
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    place = common.from_data_to_structure(data)
    if _check_valid_data(language, place):
        oldPlace = Place.query.filter(Place.id == place['id']).filter(Place.idUser == user.id).one_or_none()
        
        if oldPlace is None:
            abort(400, dictionary(language,"Place not found"))
        else:
            common.images_type_is_correct(place['images'])
            # First remove images
            images = PlaceImages.query.filter(PlaceImages.idPlace == place["id"])
            images = PlaceImagesSchema(many=True).dump(images)
            for image in images:
                os.remove(common.IMAGES_PATH+image['image'])
            PlaceImages.query.filter(PlaceImages.idPlace == place["id"]).delete()
            db.session.commit()
            
            # Then add
            for index,image in enumerate(place["images"]):
                imgtype = image.split(",")[0].split("/")[1].split(";")[0]
                imgdata = base64.b64decode(image.split(",")[1])
                path = common.IMAGES_PATH
                filename = "place_" + str(place["id"]) + "_" + str(index) + "." + imgtype
                with open((path + filename), 'wb') as f:
                    f.write(imgdata)
                newImage = PlaceImages(idPlace = place["id"], image = filename)
                db.session.add(newImage)
            db.session.commit()
            
            ## Update locality of Place
            common.remove_locality(db, oldPlace.locality)
            idLocality = common.add_locality(db, place["country"], place["province"], place["city"])
            
            ## Update Place
            updatePlace = Place(title=place["title"], text=place["text"], language=place["language"], idUser=user.id, locality=idLocality)
            updatePlace.id = place["id"]
            
            # Update place to the database
            db.session.merge(updatePlace)
            db.session.commit()
            

            ## Update Place Tags
            # First remove
            PlaceTags.query.filter(PlaceTags.idPlace == place["id"]).delete()
            db.session.commit()
            # Then add tags
            for t in place["tags"]:
                if(t !=""):
                    newTag = PlaceTags(idPlace = place["id"], tag=t)
                    # merge the new object into the old and commit it to the db
                    db.session.add(newTag)
            db.session.commit()

            return make_response(
            { 'message': 'Ok', 'status':200 },
            200
            )

def update_like(language, idReview, like=0):  
    """Update 1 like for a review

    Update 1 like user does for 1 place 

    :param language: Language using in client
    :type language: str
    :param id: Id that identify the review voted
    :type id: int
    :param like: Like or unlike given/removed to the review (1, -1 or 0)
    :type like: int
    """
    if not(like in [-1,0,1]):
        abort(400, dictionary(language,"Value not valid"))
    user = common.check_token(connexion, language)
    if like in [-1,1]:
        oldLike = db.session.query(PlaceReviewsLikes.like).filter(PlaceReviewsLikes.idUser == user.id, PlaceReviewsLikes.idReview == idReview).one_or_none()
        newLike = PlaceReviewsLikes(idReview=idReview,idUser=user.id, like=like)
        if oldLike is None:
            # First time user likes this review
            db.session.add(newLike)
        else:
            # User update its like
            db.session.merge(newLike)
    else:
        PlaceReviewsLikes.query.filter(PlaceReviewsLikes.idUser == user.id, PlaceReviewsLikes.idReview == idReview).delete()
    db.session.commit()
    return make_response(
        { 'message': 'Ok', 'status':200 },
        200
        )
    
def update_review(language, data):  
    """Update 1 existing  review

    Update 1 existing review 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to create a new place
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    review = {
        "idReview": data.get("idReview"),
        "text": data.get("text")
    }
    oldReview = db.session.query(PlaceReviews.idPlace,PlaceReviews.date).filter(PlaceReviews.id == review["idReview"], PlaceReviews.idUser == user.id).one_or_none()
    if oldReview is None:
        abort(400, dictionary(language,"Review not fould"))
    
    newReview = PlaceReviews(id=review["idReview"], idPlace = oldReview.idPlace, idUser = user.id, text = review["text"], date=oldReview.date)
    db.session.merge(newReview)
    db.session.commit()

    return make_response(
         { 'message': 'Ok', 'status':200 },
         200
      )

def update_vote(language, idPlace, vote=None):  
    """Update 1 vote

    Update 1 vote user does for 1 place 

    :param language: Language using in client
    :type language: str
    :param id: Id that identify the place voted
    :type id: int
    :param vote: Vote given (from 0 to 4)
    :type vote: int
    """
    user = common.check_token(connexion, language)
    _check_if_place_exist(language, idPlace)
    if vote is None or vote == -1:
        ## First remove old vote if present
        PlaceVotes.query.filter(PlaceVotes.idPlace == idPlace, PlaceVotes.idUser == user.id).delete()
        db.session.commit()
        return make_response(
                { 'message': 'Ok', 'status':200 },
                200
            )
    elif vote < 0 or vote > 4:
        abort(400, dictionary(language,"Vote not valid"))
    else:
        ## First remove old vote if present
        PlaceVotes.query.filter(PlaceVotes.idPlace == idPlace, PlaceVotes.idUser==user.id).delete()
        db.session.commit()

        ## Then add the vote
        newVote = PlaceVotes(idPlace=idPlace, idUser=user.id, vote=vote)
        db.session.add(newVote)
        db.session.commit()
        return make_response(
                { 'message': 'Ok', 'status':200 },
                200
            )

