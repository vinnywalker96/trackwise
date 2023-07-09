from app.api.views import app_views
from app.models import User
from flask import jsonify


@app_views.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = []
    for user in users:
        user_data = {
            "username": user.username
        }
        users_data.append(user_data) 
    return jsonify(users_data)

    
    
    
    
    
    
