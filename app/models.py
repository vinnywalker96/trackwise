"""Creates the database models for the application.
"""
from app import db, login, ma
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64
import os
from datetime import datetime, timedelta
from flask import url_for


CATEGORY = (
    ("Stationary", "Stationary"),
    ("Electronics", "Electronics"),
    ("Food", "Food"),
)

class User(UserMixin, db.Model):
    """Class User is a model for the user table in the database.

    Args:
        UserMixin (_type_): inherits from UserMixin class
        db (_type_): inherits from db.Model class

    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
   
    password_hash = db.Column(db.String(128))
    
    
    
    # @property
    # def password(self):
    #     raise AttributeError('Password is not readable')
    
    # @password.setter
    def set_password(self, password):
        """set_password method hashes the password

        Args:
            password (_type_): password to be hashed
        """
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """check_password method checks if the password is correct

        Args:
            password (_type_): password to be checked

        Returns:
            _type_: _description_
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return "<User {}>".format(self.username)
 

@login.user_loader
def load_user(id):
    """load_user method loads the user from the database

    Args:
        id (_type_): id of the user

    Returns:
        _type_: user object
        
    """
    return User.query.get(int(id))

class Product(db.Model):
    """Class Product is a model for the product table in the database."""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(20), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    

    def __init__(self, name, category, quantity, description):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.description = description
        
    def __str__(self):
        return self.name


class Order(db.Model):
    """Class Order is a model for the order table in the database."""
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    order_quantity = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    
    
    
    
    def set_current_user(self, current_user):
        """Sets the current user to the order"""
        self.created_by = current_user
    
    def set_date(self, date):
        """"
        Sets the date of the order"""
        self.date = date

  

    def __str__(self):
        return f"{self.product.name} ordered quantity {self.order_quantity}"
    
#Create a schema for the product
class ProductList(ma.Schema):
    """Class ProductCategory is a model for the product category schema in the database."""
    class Meta:
        fields = ('name', 'category', 'quantity', 'description', 'date_created') 
        
#create instance for schema
productlist_schema = ProductList(many=False)
productlists_schema = ProductList(many=True)