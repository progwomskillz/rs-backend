from flask import Blueprint, request
from flasgger import swag_from

from application.structure import structure


users_blueprint = Blueprint("users_v1", __name__, url_prefix="/v1/users")
base_swagger_path = "./../../swagger/users"


@users_blueprint.route("", methods=["POST"])
@swag_from(f"{base_swagger_path}/create_user.yml")
def create_user():
    return structure.create_user_handler.handle(request)


@users_blueprint.route("", methods=["GET"])
@swag_from(f"{base_swagger_path}/get_users_page.yml")
def get_users_page():
    return structure.get_users_page_handler.handle(request)
