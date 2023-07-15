from flask import Blueprint
from app import app

app_views = Blueprint('app_views', __name__, url_prefix='/api/')

from app.api import products, users




