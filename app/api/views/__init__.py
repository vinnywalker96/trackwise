from flask import Blueprint
from app import app

app_views = Blueprint('app_views', __name__, url_prefix='/api/views')

from flask_restful import Resource, Api

api = Api(app)

from app.api.views.products import *
from app.api.views.orders import *
from app.api.views.users import *




