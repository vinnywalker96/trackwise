from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/views')

from app.api.views.products import *
from app.api.views.orders import *
from app.api.views.users import *