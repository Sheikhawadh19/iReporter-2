from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

from flask import request, jsonify, abort

def create_app(config_name):
    from app.API.V1.models.models import Ireporter, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

   
    @app.route('/API/V1/Ireporter/', methods=['POST', 'GET'])
    def ireporters():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        ireporter = Ireporter(name=name, created_by=user_id)
                        ireporter.save()
                        response = jsonify({
                            'id': ireporter.id,
                            'name': ireporter.name,
                            'date_created': ireporter.date_created,
                            'date_modified': ireporter.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET all the bucketlists created by this user
                    ireporters = Ireporter.query.filter_by(created_by=user_id)
                    results = []

                    for Ireporter in ireporters:
                        obj = {
                            'id': ireporter.id,
                            'name': ireporter.name,
                            'date_created': ireporter.date_created,
                            'date_modified': ireporter.date_modified,
                            'created_by': ireporter.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401
    @app.route('/API/V1/Ireporter/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def ireporter_manipulation(id, **kwargs):
        # get the access token from the authorization header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                ireporter = Ireporter.query.filter_by(id=id).first()
                if not ireporter:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    # delete the bucketlist using our delete method
                    ireporter.delete()
                    return {
                        "message": "ireporter {} deleted".format(ireporter.id)
                    }, 200

                elif request.method == 'PUT':
                    # Obtain the new name from the request data
                    name = str(request.data.get('name', ''))

                    ireporter.name = name
                    ireporter.save()

                    response = {
                        'id': ireporter.id,
                        'name': ireporter.name,
                        'date_created': ireporter.date_created,
                        'date_modified': ireporter.date_modified,
                        'created_by': ireporter.created_by
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # Handle GET request, sending back the bucketlist to the user
                    response = {
                        'id': ireporter.id,
                        'name': ireporter.name,
                        'date_created': ireporter.date_created,
                        'date_modified': ireporter.date_modified,
                        'created_by': ireporter.created_by
                    }
                    return make_response(jsonify(response)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401

   
   

    # import the authentication blueprint and register it on the app
    from .API.V1.views import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app




