from app.api import app_views
from app.models import Order
from flask import jsonify
from app import db


@app_views.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.filter_by(id=id).first_or_404()
    db.session.delete(order)
    db.commit()

