from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config
from flask import request, jsonify, abort
# initialize sql-alchemy

db = SQLAlchemy()

def create_postgres(app):
    from app.models import UserPostgres

    
    db.init_app(app)
        
    @app.route('/postgresqlUser', methods=['POST'])
    def create_user_postgres():
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
            user = UserPostgres(username=username, firstname=firstname, lastname=lastname)
            users = UserPostgres.get_all()
            if any(obj.username == username for obj in users):
                abort(400, 'Username is not unique')
            user.save()
            response = jsonify({
                'id': user.id,
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
        users = UserPostgres.get_all()
        results = []

        for user in users:
            obj = {
                'id': user.id,
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response
    
    @app.route('/postgresqlUser/<int:id>', methods=['DELETE'])
    def delete_user_postgres(id, **kwargs):
        """
        Delete a user
        ---
        tags:
            - User API
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          500:
            description: General error
          200:
            description: User deleted successfully
          404:
            description: User not found
        """
        # retrieve a user using it's ID
        user = UserPostgres.query.filter_by(id=id).first()
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404, 'User not found')
        if request.method == 'DELETE':
            user.delete()
            return {
            "message": "User '{}' deleted successfully".format(user.id) 
         }, 200

    @app.route('/postgresqlUser', methods=['GET'])
    def get_user_postgres(**kwargs):
        """
        Get a user by id or all users if no id is supplied
        ---
        tags:
            - User API
        parameters:
          - name: id
            in: query
            required: false
            type: integer
        responses:
          500:
            description: General error
          200:
            description: Users listed
          404:
            description: User not found
        """
        id = request.args.get('id', '')
        if not id:
            users = UserPostgres.get_all()
            results = []

            for user in users:
                obj = {
                    'id': user.id,
                    'username': user.username,
                    'firstname': user.firstname,
                    'lastname': user.lastname
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            user = UserPostgres.query.filter_by(id=id).first()
            if not user:
                # Raise an HTTPException with a 404 not found status code
                abort(404, 'User not found')
            response = jsonify({
                'id': user.id,
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname
            })
            response.status_code = 200
            return response

    @app.route('/postgresqlUser', methods=['PUT'])
    def edit_user_postgres(**kwargs):
        """
        Edit a user
        ---
        tags:
            - User API
        parameters:
          - name: id
            in: query
            required: true
            type: integer
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
        # retrieve a user using it's ID
        id = request.args.get('id', '')
        user = UserPostgres.query.filter_by(id=id).first()
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404, 'User not found')

        username = str(request.data.get('username', ''))
        firstname = str(request.data.get('firstname', ''))
        lastname = str(request.data.get('lastname', ''))
        users = UserPostgres.query.filter(UserPostgres.id != user.id).all()

        if any(obj.username == username for obj in users):
            abort(400, 'Username is not unique')
        
        user.username = username if username else user.username
        user.firstname = firstname if firstname else user.firstname
        user.lastname = lastname if lastname else user.lastname
        
        user.save()
        response = jsonify({
            'id': user.id,
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname
        })
        response.status_code = 200
        return response
        
    return app



