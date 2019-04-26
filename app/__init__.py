from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()
from flask import request, jsonify, abort

def create_app(config_name):
    from app.API.V1.models.models import Ireporter
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

   
    @app.route('/API/V1/Ireporter/', methods=['POST', 'GET'])
    def ireporters():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                ireporter = Ireporter(name=name)
                ireporter.save()
                response = jsonify({
                    'id': ireporter.id,
                    'name': ireporter.name,
                    'email': ireporter.email,
                    'comment': ireporter.comment,
                    'date_created': ireporter.date_created,
                    'date_modified': ireporter.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            ireporters = Ireporter.get_all()
            results = []

            for ireporter in ireporters:
                obj = {
                    'id': ireporter.id,
                    'name': ireporter.name,
                    'email': ireporter.email,
                    'comment': ireporter.comment,
                    'date_created': ireporter.date_created,
                    'date_modified': ireporter.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    @app.route('/API/V1/Ireporter/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def ireporter_manipulation(id, **kwargs):
     # retrieve a buckelist using it's ID
        ireporter = Ireporter.query.filter_by(id=id).first()
        if not ireporter:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            ireporter.delete()
            return {
            "message": "ireporter {} deleted successfully".format(ireporter.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            ireporter.name = name
            ireporter.save()
            response = jsonify({
              'id': ireporter.id,
              'name': ireporter.name,
              'email': ireporter.email,
              'comment': ireporter.comment,
              'date_created': ireporter.date_created,
              'date_modified': ireporter.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': ireporter.id,
                'name': ireporter.name,
                'email': ireporter.email,
                'comment': ireporter.comment,
                'date_created': ireporter.date_created,
                'date_modified': ireporter.date_modified
            })
            response.status_code = 200
            return response

   

    return app


