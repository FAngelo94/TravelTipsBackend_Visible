import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dictionary._dictionary import dictionary
from flask_cors import CORS


basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Only to server
#app.static_url_path=''
#app.static_folder="/static/"
CORS(app)

config = {
'host': '**',
'port': 0000,
'user': '****',
'password': '****',
'database': '****'
}

db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

# Build the Sqlite ULR for SqlAlchemy
sqlite_url = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_POOL_RECYCLE"] = 5
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
