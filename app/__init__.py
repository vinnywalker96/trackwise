from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_marshmallow import Marshmallow
  
db = SQLAlchemy()
migrate = Migrate()  
bootstrap = Bootstrap()
login = LoginManager()
csrf = CSRFProtect()
mail = Mail()
ma = Marshmallow()



    # instantiate the app
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
bootstrap.init_app(app)
login.login_view = 'login'
csrf.init_app(app)
mail.init_app(app)
ma.init_app(app)

from app.main import bp as main_bp
    
app.register_blueprint(main_bp)
    
    
    
CORS(app, resources={r'/*': {'origins': '*'}})


    
   








# enable CORS
