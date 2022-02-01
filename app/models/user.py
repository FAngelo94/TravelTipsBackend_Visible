from config import db, ma
import datetime

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64))
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    token = db.Column(db.String(32))
    profileImagePath = db.Column(db.String(32))
    home = db.Column(db.Integer)
    role = db.Column(db.Integer, default=0)
    lastLogin = db.Column(db.DateTime, default=datetime.datetime.utcnow)
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class LocalityVisited(db.Model):
    __tablename__ = "LocalityVisited"
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    idLocality = db.Column(db.Integer, primary_key=True)
class LocalityVisitedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocalityVisited
        load_instance = True

class UserInterests(db.Model):
    __tablename__ = "UserInterests"
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    interest = db.Column(db.String(16), primary_key=True)
class UserInterestsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserInterests
        load_instance = True

class UserLanguages(db.Model):
    __tablename__ = "UserLanguages"
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    language = db.Column(db.String(32), primary_key=True)
class UserLanguagesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserLanguages
        load_instance = True

class UserStar(db.Model):
    __tablename__ = "UserStar"
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    idUserFollowed = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)

class UserPasswordCode(db.Model):
    __tablename__ = "UserPasswordCode"
    idUser = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    token = db.Column(db.String(32))
