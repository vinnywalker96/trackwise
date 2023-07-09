from app.api.views import app_views
from app.models import Product
from flask import flash, redirect, jsonify
from app import db


@app_views.route('/products', method=['GET'])
def delete_product(id):
    product = Product.query.all()
  
    return 
        
    

