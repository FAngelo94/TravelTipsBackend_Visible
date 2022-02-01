# 3rd party moudles
from flask import render_template
import utils
import smtplib, ssl

# local modules
import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/

    :return:        the rendered template "home.html"
    """
    return render_template("home.html")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    connex_app.run(host='0.0.0.0', port=5000, debug=True)

'''
from flask import render_template, jsonify
import json
import connexion
# import flask_cors
import utils

# Instantiate global variables
app = connexion.App(__name__, specification_dir='./')
# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

# flask_cors.CORS(app)

# Routing Functions
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html', message="Hello World")

@app.route('/login/', methods=['POST'])
def login():
    token = utils.get_random_string(30)
    message = {
        'id': 0,
        'token': token
    }
    return json.dumps(message)

@app.route('/fakelogin/', methods=['GET'])
def fakelogin():
    token = utils.get_random_string(30)
    message = {
        'id': 0,
        'token': token
    }
    return json.dumps(message)
    
# Comment to use this server in pythonanywhere

if __name__ == '__main__':
    host = '0.0.0.0'  # Set 0.0.0.0 to have server available externally
    port = 5000
    # Active debug for the server, it refreshes when there are updates
    app.run(host=host, port=port, debug=True)
    '''