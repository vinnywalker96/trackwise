from app.api.views import app_views
from app.models import User
from flask import jsonify
from flask_restful import Resource,Api
from app import api

# class Users(Resource):
#     def get_users(self):
#         return{"Hello": "World"}
    
    
# api.add_resource(Users, '/api/views')
    


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

    
    
    
    
    
    
