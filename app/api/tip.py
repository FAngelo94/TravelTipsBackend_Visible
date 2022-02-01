import os
import json
from flask import make_response, abort, request
from sqlalchemy import func, or_
from config import db
from models.tip import Tip, TipVotes, TipLanguages, TipTags, TipTagsSchema, TipSchema, TipVotesSchema, TipLanguagesSchema
from models.locality import Locality, LocalitySchema
from models.user import User, UserSchema
import utils
from dictionary._dictionary import dictionary
import connexion
from datetime import datetime
import api._common as common


def _check_valid_data(language, tip):
    if tip["text"] and tip["title"] and tip["country"] and tip["province"] and tip["city"] and tip["languages"] and tip["tags"]:
        return True
    abort(400, dictionary(language, "Fill all fields correctly"))


def read_list(language, data={}):
    token = None
    user = None
    if 'token' in connexion.request.headers:
        user = common.check_token(connexion, language)

    tips = db.session.query(Tip.id, Tip.title, Tip.text, Tip.date, User.username, User.id.label(
        "idUser"), Locality.country, Locality.province, Locality.city).filter(Tip.idUser == User.id, Tip.locality == Locality.id)
    tips = common.apply_common_filters(db, data, tips, "Tip")
    tips = tips.order_by(Tip.date.desc())
    tips = tips.group_by(Tip.id, Tip.title, Tip.text, Tip.date,
                         User.username, Locality.country, Locality.province, Locality.city)
    schema = TipSchema(many=True)
    dataTips = schema.dump(tips)

    for t in dataTips:
        # Get all tags for this tip
        tags = db.session.query(TipTags.tag).filter(TipTags.idTip == t['id'])
        dataTags = TipTagsSchema(many=True).dump(tags)
        arrayTags = ""
        for d in dataTags:
            arrayTags += "#"+d['tag']+" "
        t['tags'] = arrayTags[:-1]
        # Get all languages for this tip
        languages = db.session.query(TipLanguages.language).filter(
            TipLanguages.idTip == t['id'])
        dataLanguage = TipLanguagesSchema(many=True).dump(languages)
        arrayLanguages = ""
        for d in dataLanguage:
            arrayLanguages += d['language'] + ", "
        t['languages'] = arrayLanguages[:-2]
        # Get all vote for this tips
        votes = db.session.query(TipVotes.vote).filter(
            TipVotes.idTip == t['id'])
        dataAverageVote = TipVotesSchema(many=True).dump(votes)
        if len(dataAverageVote) > 0:
            averageVote = 0
            for d in dataAverageVote:
                averageVote += d["vote"]
            t['averageVote'] = averageVote/len(dataAverageVote)
        else:
            t['averageVote'] = -1
        # Get user vote

        if not(user is None):
            votes = db.session.query(TipVotes.vote).filter(
                TipVotes.idTip == t['id'], TipVotes.idUser == user.id).one_or_none()
            userVote = TipVotesSchema().dump(votes)
            if not(userVote is None) and userVote != {}:
                t['voted'] = userVote['vote']
            else:
                t['voted'] = -1

    return make_response(
        {'message': 'Ok', 'status': 200, "tips": dataTips},
        200
    )


def create(language, data):
    user = common.check_token(connexion, language)

    tip = common.from_data_to_structure(data)
    _check_valid_data(language, tip)
    # Add locality of Tip
    idLocality = common.add_locality(
        db, tip["country"], tip["province"], tip["city"])
    # Add Tip
    now = datetime.now()
    dtString = now.strftime("%Y-%m-%d %H:%M:%S")
    newTip = Tip(title=tip["title"], text=tip["text"],
                 idUser=user.id, date=dtString, locality=idLocality)
    # Add tip to the database
    db.session.add(newTip)
    db.session.commit()

    # Add Tip Languages
    for l in tip["languages"]:
        if(l != ""):
            newLanguage = TipLanguages(idTip=newTip.id, language=l)
            # merge the new object into the old and commit it to the db
            db.session.add(newLanguage)

    # Add Tip Tags
    for t in tip["tags"]:
        if(t != ""):
            newTag = TipTags(idTip=newTip.id, tag=t)
            # merge the new object into the old and commit it to the db
            db.session.add(newTag)
    db.session.commit()
    return make_response(
        {'message': 'Ok', 'status': 200, "id": newTip.id, "date": dtString},
        200
    )


def update(language, data):
    user = common.check_token(connexion, language)
    oldTip = Tip.query.filter(Tip.id == data.get("id")).filter(
        Tip.idUser == user.id).one_or_none()

    if oldTip is None:
        abort(400, dictionary(language, "Tip not found"))
    else:
        tip = common.from_data_to_structure(data)
        _check_valid_data(language, tip)
        # Update locality of Tip
        common.remove_locality(db, oldTip.locality)
        idLocality = common.add_locality(
            db, tip["country"], tip["province"], tip["city"])
        # Update Tip
        updateTip = Tip(title=tip["title"], text=tip["text"],
                        idUser=user.id, locality=idLocality)
        updateTip.id = tip["id"]
        # Update tip to the database
        db.session.merge(updateTip)
        db.session.commit()

        # Update Tip Languages
        # First remove
        TipLanguages.query.filter(TipLanguages.idTip == updateTip.id).delete()
        db.session.commit()
        # Then add languages
        for l in tip["languages"]:
            if(l != ""):
                newLanguage = TipLanguages(idTip=updateTip.id, language=l)
                # merge the new object into the old and commit it to the db
                db.session.add(newLanguage)

        # Update Tip Tags
        # First remove
        TipTags.query.filter(TipTags.idTip == updateTip.id).delete()
        db.session.commit()
        # Then add tags
        for t in tip["tags"]:
            if(t != ""):
                newTag = TipTags(idTip=updateTip.id, tag=t)
                # merge the new object into the old and commit it to the db
                db.session.add(newTag)
        db.session.commit()

        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )


def delete(language, idTip):
    user = common.check_token(connexion, language)
    oldTip = Tip.query.filter(Tip.id == idTip).filter(
        Tip.idUser == user.id).one_or_none()

    if oldTip is None:
        abort(400, dictionary(language, "Tip not found"))
    else:
        # Remove Tip Languages
        TipLanguages.query.filter(TipLanguages.idTip == idTip).delete()
        db.session.commit()

        # Remove Tip Tags
        TipTags.query.filter(TipTags.idTip == idTip).delete()
        db.session.commit()

        # Remove Tip
        common.remove_locality(db, oldTip.locality)
        Tip.query.filter(Tip.id == idTip).delete()
        db.session.commit()

        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )


def update_vote(language, idTip, vote=None):
    user = common.check_token(connexion, language)
    checkTip = Tip.query.filter(Tip.id == idTip).one_or_none()

    if checkTip is None:
        abort(400, dictionary(language, "Tip not found"))
    elif vote is None or vote == -1:
        # First remove old vote if present
        TipVotes.query.filter(TipVotes.idTip == idTip).delete()
        db.session.commit()
        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )
    elif vote < 0 or vote > 4:
        abort(400, dictionary(language, "Vote not valid"))
    else:
        # First remove old vote if present
        TipVotes.query.filter(TipVotes.idTip == idTip).delete()
        db.session.commit()

        # Then add the vote
        newVote = TipVotes(idTip=idTip, idUser=user.id, vote=vote)
        db.session.add(newVote)
        db.session.commit()
        return make_response(
            {'message': 'Ok', 'status': 200},
            200
        )
