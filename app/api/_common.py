from models.locality import Locality, LocalitySchema
from models.tip import Tip, TipVotes, TipLanguages, TipTags, TipTagsSchema, TipSchema, TipVotesSchema, TipLanguagesSchema
from models.itinerary import Itinerary, ItineraryVotes, ItineraryLanguages, ItineraryTags, ItineraryImages, ItineraryTagsSchema, ItinerarySchema, ItineraryVotesSchema, ItineraryLanguagesSchema, ItineraryImagesSchema
from models.user import User
from sqlalchemy import func, or_
from flask import abort
from dictionary._dictionary import dictionary
from flask import abort

IMAGES_PATH = "/home/FAngelo94/TravelTipsBackend/app/static/images/"


def add_locality(db, _country, _province, _city):
    country = _country.title()
    province = _province.title()
    city = _city.title()
    check_locality = Locality.query.filter(
        Locality.country == country, Locality.province == province, Locality.city == city).one_or_none()

    schema = LocalitySchema()
    if check_locality is None:
        new_row = {
            'country': country,
            'province': province,
            'city': city,
            'counter': 1
        }
        update_locality = schema.load(new_row, session=db.session)
        # merge the new object into the old and commit it to the db
        db.session.add(update_locality)
        db.session.commit()

        return update_locality.id
    else:
        new_row = {
            'counter': check_locality.counter + 1
        }
        update_locality = schema.load(new_row, session=db.session)
        update_locality.id = check_locality.id
        # merge the new object into the old and commit it to the db
        db.session.merge(update_locality)
        db.session.commit()

        return check_locality.id


def remove_locality(db, id):
    check_locality = Locality.query.filter(Locality.id == id).one_or_none()

    if not(check_locality is None):
        locality = Locality.query.filter(
            Locality.id == id, Locality.counter > 1).one_or_none()
        if locality is None:
            locality_unique = Locality.query.filter(
                Locality.id == id, Locality.counter <= 1).delete()
            db.session.commit()
        else:
            new_row = {
                'counter': locality.counter - 1
            }
            schema = LocalitySchema()
            update_locality = schema.load(new_row, session=db.session)
            update_locality.id = locality.id
            # merge the new object into the old and commit it to the db
            db.session.merge(update_locality)
            db.session.commit()


def images_type_is_correct(images):
    for index, image in enumerate(images):
        if(image != ""):
            imgtype = image.split(",")[0].split("/")[1].split(";")[0]
            if not(imgtype in ['jpeg', 'jpg', 'png']):
                abort(400, (dictionary(language, "Image type not valid")))
        else:
            abort(400, (dictionary(language, "Image type not valid")))


def check_token(connexion, language):
    token = connexion.request.headers['token']
    idUser = connexion.request.headers['id']

    user = User.query.filter(
        User.token == token, User.id == idUser).one_or_none()

    if user is None or token is None:
        abort(400, dictionary(language, "Session not found"))
    return user


def check_admin(idUser):
    user = User.query.filter(User.id == idUser).one_or_none()

    if user.role != 3:
        abort(400, dictionary(language, "You don't have enught POWER!"))
    return True


def from_data_to_structure(data):
    newStruct = {
        "id": data.get("id"),
        "text": data.get("text"),
        "longText": data.get("longText"),
        "title": data.get("title"),
        "country": data.get("country"),
        "province": data.get("province"),
        "city": data.get("city"),
        "languages": data.get("languages").split(",") if data.get("languages") else data.get("languages"),
        "language": data.get("language"),
        "tags": data.get("tags").split(",") if data.get("tags") else data.get("tags"),
        "dates": data.get("dates"),
        "images": data.get("images")
    }
    return newStruct


def apply_common_filters(db, data, query, contentType):
    filters = {
        "own": data.get("own"),
        "username": data.get("username"),
        "country": data.get("country"),
        "province": data.get("province"),
        "city": data.get("city"),
        "tags": data.get("tags").split(",") if data.get("tags") else data.get("tags"),
        "date": data.get("date"),
        "text": data.get("text"),
        "languages": data.get("languages").split(",") if data.get("languages") else data.get("languages")
    }

    # Apply filters when passed
    if filters['username']:
        query = query.filter(User.username == filters['username'])
    if filters['country']:
        query = query.filter(Locality.country == filters['country'])
    if filters['province']:
        query = query.filter(Locality.province == filters['province'])
    if filters['city']:
        query = query.filter(Locality.city == filters['city'])

    if(contentType == "Tip"):
        if filters['text']:
            query = query.filter(or_(Tip.text.like(
                "%"+filters['text']+"%"), Tip.title.like("%"+filters['text']+"%")))
        if filters['tags']:
            query = query.filter(Tip.id == TipTags.idTip,
                                 TipTags.tag.in_(filters['tags']))
        if filters['languages']:
            query = query.filter(Tip.id == TipLanguages.idTip,
                                 TipLanguages.language.in_(filters['languages']))
        if filters['own'] and user:
            query = query.filter(Tip.idUser == user.id)

    if(contentType == "Itinerary"):
        if filters['text']:
            query = query.filter(or_(Itinerary.text.like("%"+filters['text']+"%"), Itinerary.title.like(
                "%"+filters['text']+"%"), Itinerary.longText.like("%"+filters['text']+"%")))
        if filters['tags']:
            query = query.filter(
                Itinerary.id == ItineraryTags.idItinerary, ItineraryTags.tag.in_(filters['tags']))
        if filters['languages']:
            query = query.filter(Itinerary.id == ItineraryLanguages.idItinerary,
                                 ItineraryLanguages.language.in_(filters['languages']))
        if filters['own'] and user:
            query = query.filter(Itinerary.idUser == user.id)

    return query
