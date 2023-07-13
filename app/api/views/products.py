from app.api.views import app_views
from app.models import Product
from flask import flash, redirect, jsonify
from app import db


@app_views.route('/product/<int:id>', methods=['GET','DELETE'])
def delete_product(id):
    product = db.get_or_404(Product, id)
    db.session.delete(product)
    db.session.commit()
    return "product deleted"
        
    

