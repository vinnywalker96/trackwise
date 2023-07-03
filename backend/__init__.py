
from flask import Flask
from flask_cors import CORS

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

from backend import routes

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
