from app import app, db
from app.models import User, Product, Order

with app.context():
    """create_all method creates all the tables in the database"""
    db.create_all()