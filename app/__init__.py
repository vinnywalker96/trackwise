from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
  
db = SQLAlchemy()
migrate = Migrate()  
bootstrap = Bootstrap()
login = LoginManager()
csrf = CSRFProtect()




    # instantiate the app
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
bootstrap.init_app(app)
login.login_view = 'login'
csrf.init_app(app)

from app.main import bp as main_bp
    
app.register_blueprint(main_bp)

    
from app.api.views import app_views
    
app.register_blueprint(app_views)
    
    
    
CORS(app, resources={r'/*': {'origins': '*'}})
    









# enable CORS
