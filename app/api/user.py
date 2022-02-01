import os
import base64
import json
from flask import make_response, abort, request
from config import db
from models.user import User, UserSchema, LocalityVisited, LocalityVisitedSchema, UserInterests, UserInterestsSchema, UserLanguages, UserLanguagesSchema, UserStar, UserPasswordCode
from models.locality import Locality, LocalitySchema
from models.tip import Tip, TipSchema
from models.itinerary import Itinerary, ItinerarySchema
import utils
from dictionary._dictionary import dictionary
import connexion
import api._common as common
import datetime

"""
This is the people module and supports all the ReST actions for the
User collection
"""


def create(language, data):
    """ Function to create user with basic matadory information """
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    existing_user = (
        User.query.filter(User.email == email)
        .one_or_none()
    )
    # Check password not empty
    if email == "":
        abort(400, dictionary(language, "Insert a not empty email"))
    elif username == "":
        abort(400, dictionary(language, "Insert a not empty username"))
    elif password == "":
        abort(400, dictionary(language, "Insert a not empty password"))
    # Can we insert this user?
    elif existing_user is None:
        # Create a user instance using the schema and the passed in user
        schema = UserSchema()
        data_db = {'username': username, 'password': password, 'email': email}
        new_user = schema.load(data_db, session=db.session)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created user in the response

        return make_response({'message': dictionary(language, "Registration success"), 'status': 201}, 201)

    # Otherwise, nope, user exists already
    else:
        abort(409, dictionary(language, "This Email registered already"))


def delete(language):
    """ Delete one user and all information about it """
    user = common.check_token(connexion, language)

    # Remove interests and languages
    UserInterests.query.filter(UserInterests.idUser == user.id).delete()
    UserLanguages.query.filter(UserLanguages.idUser == user.id).delete()
    # Remove home
    common.remove_locality(db, user.home)
    # Remove profile image
    if user.profileImagePath != None:
        if os.path.isfile(common.IMAGES_PATH + user.profileImagePath):
            os.remove(common.IMAGES_PATH + user.profileImagePath)
    # Remove localities visited
    localities = LocalityVisited.query.add_columns(
        'idUser', 'idLocality').filter(LocalityVisited.idUser == user.id)
    locality_schema = LocalityVisitedSchema(many=True)
    localities = locality_schema.dump(localities)

    for l in localities:
        common.remove_locality(db, l['idLocality'])
    LocalityVisited.query.filter(LocalityVisited.idUser == user.id).delete()
    # Remove user
    User.query.filter(User.token == token).delete()
    db.session.commit()
    return make_response(
        {'message': dictionary(
            language, "User removed successfully"), 'status': 200},
        200
    )


def delete_interest(language, interest):
    user = common.check_token(connexion, language)

    if interest is None:
        abort(400, dictionary(language, "Error"))
    else:
        schema = UserInterestsSchema()
        userInterest = UserInterests.query.filter(
            UserInterests.idUser == user.id, UserInterests.interest == interest).delete()

        db.session.commit()

        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )


def delete_locality(language, locality):
    user = common.check_token(connexion, language)

    if locality is None:
        abort(400, dictionary(language, "Error"))

    # Remove locality visited
    row = LocalityVisited.query.filter(
        LocalityVisited.idUser == user.id, LocalityVisited.idLocality == locality).delete()
    db.session.commit()
    if row > 0:
        # if city present in locality visited remove, or decrement counter, to locality table
        common.remove_locality(db, locality)
    return make_response(
        {'message': 'Ok', 'status': 200},
        200
    )


def login(language, data):
    email = data.get("email")
    password = data.get("password")

    checkEmail = (
        User.query.filter(User.email == email)
        .one_or_none()
    )

    check_password = (
        User.query.filter(User.email == email)
        .filter(User.password == password)
        .one_or_none()
    )

    if checkEmail is None:
        abort(400, dictionary(language, "This email isn't registered"))
    elif check_password is None:
        abort(400, dictionary(language, "Wrong password"))
    else:
        token = utils.get_random_string(32)
        # turn the passed in user into a db object
        schema = UserSchema()
        user = {
            'token': token,
            'lastLogin': str(datetime.datetime.utcnow())
        }
        update = schema.load(user, session=db.session)
        # Set the id to the user we want to login
        update.id = checkEmail.id
        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return token and id user in the response
        return make_response(
            {'token': token, 'id': checkEmail.id,
                'username': checkEmail.username, 'status': 200},
            200
        )


def logout(language):
    user = common.check_token(connexion, language)
    schema = UserSchema()
    userLogout = {
        'token': None,
        'lastLogin': None
    }
    update = schema.load(userLogout, session=db.session)
    # Set the token None to the user we want to logout
    update.id = user.id
    # merge the new object into the old and commit it to the db
    db.session.merge(update)
    db.session.commit()

    return make_response(
        {'message': dictionary(
            language, "Logout successfully"), 'status': 200},
        200
    )


def put_interest(language, interest):
    user = common.check_token(connexion, language)

    if interest is None:
        abort(400, dictionary(language, "Error"))
    else:
        newInterest = UserInterests(idUser=user.id, interest=interest)
        db.session.add(newInterest)
        db.session.commit()

        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )


def put_locality(language, locality):
    """ Function to add a new locality visited by user"""
    user = common.check_token(connexion, language)
    country = locality.get("country").title()
    province = locality.get("province").title()
    city = locality.get("city").title()
    if country == "" or province == "" or city == "":
        abort(400, dictionary(language, "Compile all fields"))
    else:
        # All fields passed are valid
        idLocality = common.add_locality(db, country, province, city)
        checkIfLocalityVisitedExist = LocalityVisited.query.filter(
            LocalityVisited.idUser == user.id, LocalityVisited.idLocality == idLocality).one_or_none()
        if checkIfLocalityVisitedExist is None:
            # If the locality not exist yet in the list user add it
            schema = LocalityVisitedSchema()
            localityVisitedRow = {
                'idUser': user.id,
                'idLocality': idLocality
            }
            update = LocalityVisited(idUser=user.id, idLocality=idLocality)
            # merge the new object into the old and commit it to the db
            db.session.add(update)
            db.session.commit()
            return make_response(
                {'message': 'Ok', 'status': 200, 'idLocality': idLocality},
                200
            )
        else:
            # Locality already present
            common.remove_locality(db, idLocality)
            abort(409, dictionary(
                language, "This city is already present in your list"))


def read_list(language, id=None):
    """ Function that return the list of all user username of db"""
    token = None
    idUser = None
    if 'token' in connexion.request.headers:
        token = connexion.request.headers['token']
        idUser = connexion.request.headers['id']
    users = User.query.add_columns(
        'id', 'username', 'profileImagePath').order_by(User.id)

    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)

    for d in data:
        # Change name of profileImagePath
        d['image'] = d['profileImagePath']
        del d['profileImagePath']
        # Add home for each user
        home = db.session.query(Locality, User).add_columns('country', 'province', 'city').filter(
            User.home == Locality.id).filter(User.id == d['id']).one_or_none()
        if not(home is None):
            locality_schema = LocalitySchema()
            home = locality_schema.dump(home)
            d['home'] = home
        else:
            d['home'] = {
                "city": "",
                "country": "",
                "province": ""
            }
        # Add languages for each user
        # Read languages of user
        languages = UserLanguages.query.add_columns(
            'language').filter(UserLanguages.idUser == d['id'])
        if not(languages is None):
            lang_schema = UserLanguagesSchema(many=True)
            languages = lang_schema.dump(languages)
            d['languages'] = languages
        else:
            d['languages'] = []

        # If user pass id check follower user
        if idUser != None:
            checkFollowed = UserStar.query.filter(
                UserStar.idUser == idUser, UserStar.idUserFollowed == d['id']).one_or_none()
            if(checkFollowed != None):
                d['followed'] = True
    return make_response({'users': data, 'status': 200}, 200)


def read_all_details(id, language):
    """ Get all information about 1 user """
    user = User.query.filter(User.id == id).one_or_none()
    if(user):
        # Read languages of user
        languages = UserLanguages.query.add_columns('language').filter(
            UserLanguages.idUser == id).order_by('language')
        lang_schema = UserLanguagesSchema(many=True)
        languages = lang_schema.dump(languages)

        # Read interests of user
        interests = UserInterests.query.add_columns(
            'interest').filter(UserInterests.idUser == id)
        interest_schema = UserInterestsSchema(many=True)
        interests = interest_schema.dump(interests)

        # Read locality visited by the user
        localities = db.session.query(Locality, LocalityVisited).add_columns('id', 'country', 'province', 'city').filter(
            LocalityVisited.idLocality == Locality.id).filter(LocalityVisited.idUser == id)
        locality_schema = LocalitySchema(many=True)
        localities = locality_schema.dump(localities)

        # Read home of user
        home = db.session.query(Locality, User).add_columns(
            'country', 'province', 'city').filter(user.home == Locality.id).filter(User.id == id)
        locality_schema = LocalitySchema(many=True)
        home = locality_schema.dump(home)

        # Read number of tips
        tips = db.session.query(Tip, User).add_columns(
            Tip.id, 'idUser').filter(Tip.idUser == User.id)
        tips = TipSchema(many=True).dump(tips)

        # Read number of itineraries
        itineraries = db.session.query(Itinerary, User).add_columns(
            Itinerary.id, 'idUser').filter(Itinerary.idUser == User.id)
        itineraries = ItinerarySchema(many=True).dump(itineraries)

        data = {}
        # TODO update to get all data when ready
        data['username'] = user.username
        data['home'] = home[0] if len(home) > 0 else {}
        data['id'] = user.id
        data['image'] = user.profileImagePath
        data['languages'] = languages
        data['interests'] = interests
        data['localities'] = localities
        data['experiences'] = 0
        data['matchings'] = 0
        data['itineraries'] = len(itineraries)
        data['tips'] = len(tips)

        return make_response({'user': data, 'status': 200}, 200)
    else:
        abort(404, dictionary(language, "User not found"))


def recover_password(language, email):
    """
    Method that create a token in db and send an email to reset the password
    """
    user = db.session.query(User.id).filter(User.email == email).one_or_none()
    if user is None:
        abort(400, dictionary(language, "Email not registered"))
    # Remove old code if present
    UserPasswordCode.query.filter(UserPasswordCode.idUser == user.id).delete()
    db.session.commit()
    token = utils.get_random_string(32)
    newPasswordCode = UserPasswordCode(idUser=user.id, token=token)
    # send email with link to reset password
    link = "http://localhost:5000/api/user/resetPassword?language=%s&id=%s&tokenPass=%s" % (
        language, user.id, token)
    msg = dictionary(language, "Press this link to reset your password: ")
    obj = dictionary(language, "Recover password")
    utils.send_email(email, obj, msg, link)
    # Add password token to the database
    db.session.add(newPasswordCode)
    db.session.commit()
    message = dictionary(language, "Check your email to set a new password")
    return make_response(
        # TODO remove token from here
        {'message': message, 'status': 200, 'token': token},
        200
    )


def reset_password(language, id, tokenPass):
    """
    Method that reset the forgotten password passing special code
    send to the email
    """
    user = db.session.query(UserPasswordCode.idUser).filter(
        UserPasswordCode.token == tokenPass).one_or_none()
    if not(user is None):
        UserPasswordCode.query.filter(
            UserPasswordCode.token == tokenPass).delete()
        newPassword = utils.generate_temporary_password()
        updatePassword = User(id=id, password=newPassword)
        db.session.merge(updatePassword)
        db.session.commit()
        message = dictionary(
            language, "New password set, change it after your first login: ") + newPassword
        return make_response(
            {'message': message, 'status': 200},
            200
        )
    abort(400, dictionary(language, "Token not valid"))


def star(language, otherUser, valueStar):
    user = common.check_token(connexion, language)
    checkOtherUser = User.query.filter(User.id == otherUser).one_or_none()

    if (user.id == otherUser or checkOtherUser == None):
        abort(400, dictionary(language, "Error"))

    if valueStar:
        newStar = UserStar(idUser=user.id, idUserFollowed=otherUser)
        db.session.add(newStar)
        db.session.commit()
    else:
        UserStar.query.filter(UserStar.idUser == user.id,
                              UserStar.idUserFollowed == otherUser).delete()
        db.session.commit()
    return make_response(
        {'message': 'Ok', 'status': 200},
        200
    )


def update_home(language, locality):
    """ Function to update home of user """
    user = common.check_token(connexion, language)

    if locality is None:
        abort(400, dictionary(language, "Error"))
    else:
        country = locality.get("country")
        province = locality.get("province")
        city = locality.get("city")
        # First remove the current locality, or decrement counter if it is different from current user locality
        if (user.home != None):
            common.remove_locality(db, user.home)
        check_loc_exist = Locality.query.filter(
            Locality.country == country, Locality.province == province, Locality.city == city).one_or_none()

        if not(check_loc_exist is None) and (user.home == check_loc_exist.id):
            # Location not changed
            return make_response(
                {'message': 'Ok', 'status': 200},
                200
            )

        if country != "" or province != "" or city != "":
            # Now add new home
            # If user add some information about locality save them
            home = common.add_locality(db, country, province, city)
            schema = UserSchema()
            userRow = {
                'home': home
            }
            update = schema.load(userRow, session=db.session)
            # Set the id to the user we want to login
            update.id = user.id
            # merge the new object into the old and commit it to the db
            db.session.merge(update)
            db.session.commit()

            return make_response(
                {'message': 'Ok', 'status': 200},
                200
            )
        else:
            # if user send empty fields just remove home
            schema = UserSchema()
            userRow = {
                'home': None
            }
            update = schema.load(userRow, session=db.session)
            # Set the id to the user we want to login
            update.id = user.id
            # merge the new object into the old and commit it to the db
            db.session.merge(update)
            db.session.commit()

        # User removed the locality without add an other locality
        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )


def update_languages(language, languages):
    user = common.check_token(connexion, language)
    if languages is None:
        abort(400, dictionary(language, "Error"))
    else:
        # Remove languages already present
        UserLanguages.query.filter(UserLanguages.idUser == user.id).delete()
        db.session.commit()

        # Add new languages
        returnLang = ""
        for l in languages:
            returnLang += l + ", "
            newLanguage = UserLanguages(idUser=user.id, language=l)
            # merge the new object into the old and commit it to the db
            db.session.add(newLanguage)
            db.session.commit()

        return make_response(
            {'message': 'Ok', 'status': 200, 'languages': returnLang[:-2]},
            200
        )


def update_password(language, data):
    """ Function to change password """
    user = common.check_token(connexion, language)
    newPassword = data.get("newPassword")
    oldPassword = data.get("oldPassword")

    user = User.query.filter(User.token == token).filter(
        User.password == oldPassword).one_or_none()
    if user is None or token is None:
        abort(400, dictionary(language, "Wrong password"))
    else:
        schema = UserSchema()
        row = {
            'password': newPassword
        }
        update = schema.load(row, session=db.session)
        # Set the id to the user we want to update password
        update.id = user.id
        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()
        return make_response(
            {'message': dictionary(
                language, "Password changed"), 'status': 200},
            200
        )


def update_profile_image(language, data={}):
    if data != {}:
        image = data['image']
    else:
        image = None
    user = common.check_token(connexion, language)
    common.images_type_is_correct([image])

    if image is None:
        if(user.profileImagePath != None):
            if os.path.isfile(common.IMAGES_PATH + user.profileImagePath):
                os.remove(common.IMAGES_PATH + user.profileImagePath)
            User.query.filter(User.id == user.id).update(
                {'profileImagePath': None})
            db.session.commit()
        return make_response({'message': 'Ok', 'status': 200}, 200)
    else:
        if(user.profileImagePath != None):
            if os.path.isfile(common.IMAGES_PATH + user.profileImagePath):
                os.remove(common.IMAGES_PATH + user.profileImagePath)
        imgtype = image.split(",")[0].split("/")[1].split(";")[0]
        imgdata = base64.b64decode(image.split(",")[1])
        path = common.IMAGES_PATH
        filename = "profile_" + str(user.id) + "." + imgtype
        with open((path + filename), 'wb') as f:
            f.write(imgdata)
        User.query.filter(User.id == user.id).update(
            {'profileImagePath': filename})
        db.session.commit()
        return make_response({'message': 'Ok', 'status': 200, 'image': filename}, 200)


def update_username(language, username):
    """ Function to change username """
    user = common.check_token(connexion, language)

    if username == "":
        abort(400, dictionary(language, "Insert a not empty password"))
    else:
        schema = UserSchema()
        row = {
            'username': username
        }
        update = schema.load(row, session=db.session)
        # Set the id to the user we want to update password
        update.id = user.id
        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()
        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )
