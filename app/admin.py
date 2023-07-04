from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app, db
from models import User

admin = Admin(app, name='Dashboard')
admin.add_view(ModelView(User, db.session))
