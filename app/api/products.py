from app.api import app_views
from app.models import Product, ProductList, productlist_schema, productlists_schema
from flask import flash, redirect, jsonify, request
from app import db

@app_views.route('/products', methods=['GET','POST'])
def create_product():
    try:
        name = request.json['name']
        description = request.json['description']
        new_product = Product(name=name, description=description)
        db.session.add(new_product)
        db.session.commit()
        return productlists_schema.jsonify(new_product)
    except Exception as e:
        return jsonify({'message': "Invalid request"}), 500
        
@app_views.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = productlists_schema.dump(products)
    return jsonify(result)

@app_views.route('/product/<int:id>', methods=['GET','DELETE'])
def delete_product(id):
    product = db.get_or_404(Product, id)
    db.session.delete(product)
    db.session.commit()
    return "product deleted"
        
    

