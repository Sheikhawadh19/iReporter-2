from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
auth_blueprint = Blueprint('auth', __name__)

from app.API.V1.views import views