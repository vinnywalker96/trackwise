from app import db, login, ma
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64
import os
from flask import url_for

CATEGORY = (
    ("Stationary", "Stationary"),
    ("Electronics", "Electronics"),
    ("Food", "Food"),
)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Product(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String, nullable=True)
    created_by = db.Column(db.String, nullable=True)
    order_quantity = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


  
    def __str__(self):
        return f"{self.product.name} ordered quantity {self.order_quantity}"


class ProductList(ma.Schema):
    class Meta:
        fields = ('name', 'category', 'quantity', 'description', 'date_created')

productlist_schema = ProductList()
productlists_schema = ProductList(many=True)
