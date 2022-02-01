import os
import base64
import json
from flask import make_response, abort, request
from sqlalchemy import func, or_
from config import db
from models.experience import Experience, ExperienceVotes, ExperienceLanguages, ExperienceTags, ExperienceImages, ExperienceDates, ExperienceTagsSchema, ExperienceSchema, ExperienceVotesSchema, ExperienceLanguagesSchema,  ExperienceImagesSchema, ExperienceDatesSchema, ExperienceBooks, ExperienceBooksSchema, ExperienceBookedSchema
from models.locality import Locality, LocalitySchema
from models.user import User, UserSchema
import utils
from dictionary._dictionary import dictionary
import connexion
from datetime import datetime
import api._common as common

def _abort_creation(message, id):
    Experience.query.filter(Experience.id == id).delete()
    ExperienceLanguages.query.filter(ExperienceLanguages.idExperience == id).delete()
    ExperienceTags.query.filter(ExperienceTags.idExperience == id).delete()
    db.session.commit()
    abort(400, message)

def _check_if_experience_exist(language, id):
    experience = Experience.query.filter(Experience.id == id).one_or_none()
    if experience is None:
        abort(400, dictionary(language,"Experience not found"))

def _check_valid_data(language, experience):
    if experience["longText"] and experience["text"] and len(experience["text"])<=128 and experience["title"] and len(experience["title"])<=64 and experience["country"] and experience["province"] and experience["city"] and experience["languages"] and len(experience["languages"]) > 0 and experience["tags"] and len(experience["tags"]) > 0 and experience["images"] and len(experience["images"]) > 0 and experience["dates"] and len(experience["dates"]) > 0:
        return True
    abort(400, dictionary(language, "Fill all fields correctly"))

def add_date(language, data):  
    """Add 1 new date for an existing experience

    Add 1 new date for an existing experience 

    :param language: Language using in client
    :type language: str
    """
    user = common.check_token(connexion, language)
    date = {
        "idExperience": data.get("id"),
        "date": data.get("date"),
        "places": data.get("places")
    }
    experience = Experience.query.filter(Experience.id == date["idExperience"]).one_or_none()
    if experience is None:
        abort(400, dictionary(language,"Experience not found"))
    try:
        newDate = ExperienceDates(idExperience = date["idExperience"], date=date["date"], availablePlaces=date["places"])
        # merge the new object into the old and commit it to the db
        db.session.add(newDate)
        db.session.commit() 
    except:
        abort(400, dictionary(language,"This date already exist"))
    return make_response(
                { 'message': 'Ok', 'status':200},
                200 
            )

def book_date(language, data):  
    """Book 1 date for an experience

    Book 1 date for an experience 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to book a data for an existing experience
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    book = {
        "idExperience": data.get("id"),
        "date": data.get("date"),
        "places": data.get("places")
    }
    # Check if experience exist
    _check_if_experience_exist(language, book['idExperience'])
    # check if user already book this experience for thsi date
    userBooked = db.session.query(ExperienceBooks.idExperience).filter(ExperienceBooks.idUser == user.id, ExperienceBooks.date == book["date"]).one_or_none()

    # First check if there is free places or if user already booked this date
    experience = db.session.query(ExperienceDates.availablePlaces).filter(ExperienceDates.idExperience == book["idExperience"], ExperienceDates.date == book["date"]).one_or_none()
    allPlaces = experience[0]
    # books done of all users for this experience
    booksDone = db.session.query(func.sum(ExperienceBooks.places)).filter(ExperienceBooks.date == book["date"]).group_by(ExperienceBooks.date).all()

    if userBooked != None:
        abort(400, dictionary(language, "User already booked for this date"))
    if allPlaces < len(booksDone) + book["places"]:
        abort(400, dictionary(language, "Not enought available places"))
    newBook = ExperienceBooks(idExperience = book["idExperience"], date=book["date"], idUser=user.id, places=book["places"])
    # merge the new object into the old and commit it to the db
    db.session.add(newBook)
    db.session.commit() 

    return make_response(
                { 'message': 'Ok', 'status':200},
                200 
            )

def create(language, data):  
    """Create 1 new experience

    Create 1 new experience 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to create a new experience
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    experience = common.from_data_to_structure(data)
    if _check_valid_data(language,experience):
        ## Add locality of Experience
        idLocality = common.add_locality(db, experience["country"], experience["province"], experience["city"])
        ## Add Experience
        now = datetime.now()
        dtString = now.strftime("%Y-%m-%d %H:%M:%S")
        newExperience = Experience(title=experience["title"], text=experience["text"], longText=experience["longText"], idUser=user.id, date=dtString, locality=idLocality)
        # Add experience to the database
        db.session.add(newExperience)
        db.session.commit()

        ## Add Experience Images
        # Check images type before save them
        common.images_type_is_correct(experience['images'])
        # image type is ok, save them
        for index,image in enumerate(experience["images"]):
            imgtype = image.split(",")[0].split("/")[1].split(";")[0]
            imgdata = base64.b64decode(image.split(",")[1])
            path = common.IMAGES_PATH
            filename = "experience_" + str(newExperience.id) + "_" + str(index) + "." + imgtype
            with open((path + filename), 'wb') as f:
                f.write(imgdata)
            newImage = ExperienceImages(idExperience = newExperience.id, image = filename)
            db.session.add(newImage)
        db.session.commit()

        ## Add Experience Languages
        for l in experience["languages"]:
            if(l!=""):
                newLanguage = ExperienceLanguages(idExperience = newExperience.id, language=l)
                # merge the new object into the old and commit it to the db
                db.session.add(newLanguage)
        db.session.commit()

        ## Add Experience Tags
        for t in experience["tags"]:
            if(t != ""):
                newTag = ExperienceTags(idExperience = newExperience.id, tag=t)
                # merge the new object into the old and commit it to the db
                db.session.add(newTag)
        db.session.commit() 

        ## Add Experience Dates
        for date in experience['dates']:
            if(date != ""):
                newTag = ExperienceDates(idExperience = newExperience.id, date = date['date'], availablePlaces=date['availablePlaces'])
                # merge the new object into the old and commit it to the db
                db.session.add(newTag)
        db.session.commit() 
        
        return make_response(
            { 'message': 'Ok', 'status':200, "id": newExperience.id, "date":dtString },
            200 
        )

def delete(language, idExperience):  
    """Delete 1 existing  experience

    Delete 1 existing experience 

    :param language: Language using in client
    :type language: str
    :param id: id that identify the Experience
    :type id: int
    """
    user = common.check_token(connexion, language)
    oldExperience = Experience.query.filter(Experience.id == idExperience).filter(Experience.idUser == user.id).one_or_none()
    if oldExperience is None:
            abort(400, dictionary(language,"Experience not found"))
    else:
        # Remove Experience Images
        images = ExperienceImages.query.filter(ExperienceImages.idExperience == idExperience)
        images = ExperienceImagesSchema(many=True).dump(images)
        for image in images:
            os.remove(common.IMAGES_PATH+image['image'])
        ExperienceImages.query.filter(ExperienceImages.idExperience == idExperience).delete()
        db.session.commit()

        ## Remove Experience
        common.remove_locality(db, oldExperience.locality)
        Experience.query.filter(Experience.id == idExperience).delete()
        db.session.commit()
        return make_response(
            { 'message': 'Ok', 'status':200 },
            200
        )

def delete_date(language, date, idExperience):  
    """Unbook 1 date for an existing experience

    Unbook 1 date for an existing experience 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to delete a data for an existing experience
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    date = {
        "idExperience": idExperience,
        "date": date
    }
    experience = Experience.query.filter(Experience.id == date["idExperience"], Experience.idUser == user.id).one_or_none()
    if experience is None:
        abort(400, dictionary(language,"Experience not found"))
    ExperienceDates.query.filter(ExperienceDates.idExperience == date["idExperience"], ExperienceDates.date == date["date"]).delete()
    db.session.commit()
    return make_response(
                { 'message': 'Ok', 'status':200},
                200 
            )
        
def read_list(language, data=None):  
    """Get list of experiences

    Get list of experiences appling filters 

    :param language: Language using in client
    :type language: str
    :param data: Filters passed by the client to get only the desired experiences
    :type data: dict | bytes
    """
    token = None
    user = None
    if 'token' in connexion.request.headers:
        token = connexion.request.headers['token']
        idUser = connexion.request.headers['id']
        user = User.query.filter(User.token == token, User.id == idUser).one_or_none()
    experiences = db.session.query(Experience.id,Experience.title, Experience.text,  Experience.longText, Experience.date, User.username, User.id.label("idUser"), Locality.country, Locality.province, Locality.city).filter(Experience.idUser==User.id, Experience.locality==Locality.id)
    experiences = common.apply_common_filters(db, data, experiences, "Experience")
    experiences = experiences.order_by(Experience.date.desc())

    schema = ExperienceSchema(many=True)
    dataExperiences = schema.dump(experiences)
    
    for t in dataExperiences:
        # Get all tags for this experience
        tags = db.session.query(ExperienceTags.tag).filter(ExperienceTags.idExperience==t['id'])
        dataTags = ExperienceTagsSchema(many=True).dump(tags)
        arrayTags = ""
        for d in dataTags:
            arrayTags += "#"+d['tag']+" "
        t['tags'] = arrayTags[:-1]
        # Get all languages for this experience
        languages = db.session.query(ExperienceLanguages.language).filter(ExperienceLanguages.idExperience==t['id'])
        dataLanguage = ExperienceLanguagesSchema(many=True).dump(languages)
        arrayLanguages = ""
        for d in dataLanguage:
            arrayLanguages += d['language'] +", "
        t['languages'] = arrayLanguages[:-2]
        # Get all vote for this experiences
        votes = db.session.query(ExperienceVotes.vote).filter(ExperienceVotes.idExperience==t['id'])
        dataAverageVote = ExperienceVotesSchema(many=True).dump(votes)
        if len(dataAverageVote) > 0:
            averageVote = 0
            for d in dataAverageVote:
                averageVote += d["vote"]
            t['averageVote'] = averageVote/len(dataAverageVote)
        else:
            t['averageVote'] = -1
        
        # Get user vote
        if not(user is None):
            votes = db.session.query(ExperienceVotes.vote).filter(ExperienceVotes.idExperience==t['id'],ExperienceVotes.idUser==user.id).one_or_none()
            userVote = ExperienceVotesSchema().dump(votes)
            if not(userVote is None) and userVote!={}:
                t['voted'] = userVote['vote']  
            else: 
                t['voted'] = -1
        
        # Images
        images = ExperienceImages.query.filter(ExperienceImages.idExperience == t["id"])
        images = ExperienceImagesSchema(many=True).dump(images)
        arrayImage = []
        for image in images:
            arrayImage.append(image['image'])
        t['images'] = arrayImage

        # Dates
        dates = ExperienceDates.query.filter(ExperienceDates.idExperience == t["id"]).all()
        dates = ExperienceDatesSchema(many=True).dump(dates)
        arrayDates = []
        for date in dates:
            booked = db.session.query(func.sum(ExperienceBooks.places)).filter(ExperienceBooks.date == date["date"],ExperienceBooks.idExperience == date["idExperience"]).all()
            date['booked'] = booked[0][0] if booked[0][0] != None else 0
            arrayDates.append(date)
        t['dates'] = arrayDates
    return make_response(
         { 'message': 'Ok', 'status':200, "experiences": dataExperiences },
         200
      )

def read_list_booked(language, data=None):  
    """Get list of experiences

    Get list of experiences appling filters 

    :param language: Language using in client
    :type language: str
    :param data: Filters passed by the client to get only the desired experiences
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    experiences = db.session.query(Experience.id, Experience.title, ExperienceBooks.date, User.username,ExperienceBooks.places).filter(Experience.idUser==User.id, Experience.id==ExperienceBooks.idExperience, ExperienceBooks.idUser == user.id)
    experiences = common.apply_common_filters(db, data, experiences, "Experience")
    experiences = experiences.order_by(Experience.date.desc())

    dataExperiences = ExperienceBookedSchema(many=True).dump(experiences)

    '''
    for t in dataExperiences:
        # Dates
        dates = ExperienceDates.query.filter(ExperienceDates.idExperience == t["id"]).all()
        dates = ExperienceDatesSchema(many=True).dump(dates)
        arrayDates = []
        for date in dates:
            booked = db.session.query(func.sum(ExperienceBooks.places)).filter(ExperienceBooks.date == date["date"],ExperienceBooks.idExperience == date["idExperience"]).all()
            date['booked'] = booked[0][0] if booked[0][0] != None else 0
            arrayDates.append(date)
        t['dates'] = arrayDates
    '''
    return make_response(
         { 'message': 'Ok', 'status':200, "experiences": dataExperiences },
         200
      )


def unbook_date(language, date, idExperience):  
    """Delete 1 date for an existing experience

    Delete 1 date for an existing experience 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to unbook a data for an existing experience
    :type data: dict | bytes
    """
    
    user = common.check_token(connexion, language)
    book = {
        "idExperience": idExperience,
        "date": date.replace("T"," ")
    }

    _check_if_experience_exist(language, book['idExperience'])
    result = ExperienceBooks.query.filter(ExperienceBooks.idExperience == book["idExperience"], ExperienceBooks.idUser == user.id, ExperienceBooks.date == book["date"]).delete()
    db.session.commit()
    return make_response(
        { 'message': 'Ok', 'status':200},
        200 
    )

def update(language, data):  
    """Update 1 existing  experience

    Update 1 existing experience 

    :param language: Language using in client
    :type language: str
    :param data: Data passed to create a new experience
    :type data: dict | bytes
    """
    user = common.check_token(connexion, language)
    experience = common.from_data_to_structure(data)

    if _check_valid_data(language,experience):
        oldExperience = Experience.query.filter(Experience.id == experience['id']).filter(Experience.idUser == user.id).one_or_none()
        
        if oldExperience is None:
            abort(400, dictionary(language,"Experience not found"))
        else:
            # Check image type
            common.images_type_is_correct(experience['images'])

            # First remove images
            images = ExperienceImages.query.filter(ExperienceImages.idExperience == experience["id"])
            images = ExperienceImagesSchema(many=True).dump(images)
            for image in images:
                os.remove(common.IMAGES_PATH+image['image'])
            ExperienceImages.query.filter(ExperienceImages.idExperience == experience["id"]).delete()
            db.session.commit()
            
            # Then add
            for index,image in enumerate(experience["images"]):
                imgtype = image.split(",")[0].split("/")[1].split(";")[0]
                imgdata = base64.b64decode(image.split(",")[1])
                path = common.IMAGES_PATH
                filename = "experience_" + str(experience["id"]) + "_" + str(index) + "." + imgtype
                with open((path + filename), 'wb') as f:
                    f.write(imgdata)
                newImage = ExperienceImages(idExperience = experience["id"], image = filename)
                db.session.add(newImage)
            db.session.commit()
            
            ## Update locality of Experience
            common.remove_locality(db, oldExperience.locality)
            idLocality = common.add_locality(db, experience["country"], experience["province"], experience["city"])
            
            ## Update Experience
            updateExperience = Experience(title=experience["title"], text=experience["text"], longText=experience["longText"], idUser=user.id, locality=idLocality)
            updateExperience.id = experience["id"]
            
            # Update experience to the database
            db.session.merge(updateExperience)
            db.session.commit()
            

            ## Update Experience Languages
            # First remove 
            ExperienceLanguages.query.filter(ExperienceLanguages.idExperience == experience["id"]).delete()
            db.session.commit()
            # Then add languages
            for l in experience["languages"]:
                if(l !=""):
                    newLanguage = ExperienceLanguages(idExperience = experience["id"], language=l)
                    # merge the new object into the old and commit it to the db
                    db.session.add(newLanguage)

            ## Update Experience Tags
            # First remove
            ExperienceTags.query.filter(ExperienceTags.idExperience == experience["id"]).delete()
            db.session.commit()
            # Then add tags
            for t in experience["tags"]:
                if(t !=""):
                    newTag = ExperienceTags(idExperience = experience["id"], tag=t)
                    # merge the new object into the old and commit it to the db
                    db.session.add(newTag)
            db.session.commit()

            return make_response(
            { 'message': 'Ok', 'status':200 },
            200
            )

def update_vote(language, idExperience, vote=None):  
    """Update 1 vote

    Update 1 vote user does for 1 experience 

    :param language: Language using in client
    :type language: str
    :param id: Id that identify the experience voted
    :type id: int
    :param vote: Vote given (from 0 to 4)
    :type vote: int
    """
    user = common.check_token(connexion, language)
    _check_if_experience_exist(language, idExperience)
    if vote is None or vote == -1:
        ## First remove old vote if present
        ExperienceVotes.query.filter(ExperienceVotes.idExperience == idExperience, ExperienceVotes.idUser == user.id).delete()
        db.session.commit()
        return make_response(
                { 'message': 'Ok', 'status':200 },
                200
            )
    elif vote < 0 or vote > 4:
        abort(400, dictionary(language,"Vote not valid"))
    else:
        ## First remove old vote if present
        ExperienceVotes.query.filter(ExperienceVotes.idExperience == idExperience, ExperienceVotes.idUser==user.id).delete()
        db.session.commit()

        ## Then add the vote
        newVote = ExperienceVotes(idExperience=idExperience, idUser=user.id, vote=vote)
        db.session.add(newVote)
        db.session.commit()
        return make_response(
                { 'message': 'Ok', 'status':200 },
                200
            )
