from flask import Blueprint, request
from flasgger import swag_from

from application.structure import structure


auth_blueprint = Blueprint("auth_v1", __name__, url_prefix="/v1/auth")
base_swagger_path = "./../../swagger/auth"


@auth_blueprint.route("/login", methods=["POST"])
@swag_from(f"{base_swagger_path}/login.yml")
def login():
    return structure.login_handler.handle(request)


@auth_blueprint.route("/refresh", methods=["POST"])
@swag_from(f"{base_swagger_path}/refresh.yml")
def refresh():
    return structure.refresh_handler.handle(request)


@auth_blueprint.route("/logout", methods=["POST"])
@swag_from(f"{base_swagger_path}/logout.yml")
def logout():
    return structure.logout_handler.handle(request)
