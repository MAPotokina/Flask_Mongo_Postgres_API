from flask_api import FlaskAPI
from flask_pymongo import PyMongo
import pymongo

# local import
from instance.config import app_config
from flask import request, jsonify, abort
import os

mongo = PyMongo()

def create_mongo(app):
    from app.models import UserMongoDB

    
    mongo.init_app(app)

    @app.route('/mongodbUser/', methods=['POST'])
    def create_user_mongo():
        """
        Create a user
        ---
        tags:
            - User API
        parameters:
          - name: body
            in: body
            required: true
            schema:
                required:
                    - username
                    - firstname
                    - lastname
                properties:
                    username:
                        type: string
                        description: Unique identifier representing a username
                    firstname:
                        type: string
                        description: First Name
                    lastname:
                        type: string
                        description: Last Name
        responses:
          500:
            description: General error
          201:
            description: User created
          400:
            description: Username is not unique
        """
        username = str(request.data.get('username', ''))
        firstname = str(request.data.get('firstname', ''))
        lastname = str(request.data.get('lastname', ''))
        if username:
            user = UserMongoDB(username=username, firstname=firstname, lastname=lastname)
            users = UserMongoDB.get_all()
            if any(obj.username == username for obj in users):
                abort(400, 'Username is not unique')
            user.save()
            mongo.db.users.create_index([('username', pymongo.ASCENDING)], unique=True)

            response = jsonify({
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname
            })
            response.status_code = 201
            return response

    
        """
        Get all users
        ---
        tags:
            - User API
        responses:
          500:
            description: General error
          200:
            description: Users listed
        """
        users = UserMongoDB.get_all()
        results = []

        for user in users:
            obj = {
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/mongodbUser/<username>', methods=['DELETE'])
    def delete_user_mongo(username, **kwargs):
        """
        Delete a user
        ---
        tags:
            - User API
        parameters:
          - name: username
            in: path
            required: true
            type: string
        responses:
          500:
            description: General error
          200:
            description: User deleted successfully
          404:
            description: User not found
        """
        # retrieve a user using it's username
        user = UserMongoDB.find_by_username(username=username)
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404, 'User not found')
        if request.method == 'DELETE':
            user.delete()
            return {
            "message": "User '{}' deleted successfully".format(user.username) 
         }, 200
    
    @app.route('/mongodbUser', methods=['GET'])
    def get_user_mongo(**kwargs):
        """
        Get a user by username or all users if no username is supplied
        ---
        tags:
            - User API
        parameters:
          - name: username
            in: query
            required: false
            type: string
        responses:
          500:
            description: General error
          200:
            description: Users listed
          404:
            description: User not found
        """
        username = request.args.get('username', '')
        if not username:
            users = UserMongoDB.get_all()
            results = []
            for user in users:
                obj = {
                    'username': user.username,
                    'firstname': user.firstname,
                    'lastname': user.lastname
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            # retrieve a user using it's username
            user = UserMongoDB.find_by_username(username=username)
            if not user:
                # Raise an HTTPException with a 404 not found status code
                abort(404, 'User not found')
            response = jsonify({
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname
            })
            response.status_code = 200
            return response

    @app.route('/mongodbUser', methods=['PUT'])
    def user_mongo_manipulation(**kwargs):
        """
        Edit a user
        ---
        tags:
            - User API
        parameters:
          - name: username
            in: query
            required: true
            type: string
          - name: body
            in: body
            required: true
            schema:
                properties:
                    username:
                        type: string
                        description: Unique identifier representing a username
                    firstname:
                        type: string
                        description: First Name
                    lastname:
                        type: string
                        description: Last Name
        responses:
          500:
            description: General error
          200:
            description: User edited
          400:
            description: Username is not unique
          404:
            description: Username not found
        """
        username = request.args.get('username', '')
        # retrieve a user using it's username
        user = UserMongoDB.find_by_username(username=username)
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404, 'User not found')
        elif request.method == 'PUT':
            username = str(request.data.get('username', ''))
            firstname = str(request.data.get('firstname', ''))
            lastname = str(request.data.get('lastname', ''))
            
            user.username = username if username else user.username
            user.firstname = firstname if firstname else user.firstname
            user.lastname = lastname if lastname else user.lastname
            
            user.delete()
            test = UserMongoDB.get_all()
            user.save()
            response = jsonify({
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname
            })
            response.status_code = 200
            return response
    
    return app

