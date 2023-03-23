from flask import Blueprint, request
from flasgger import swag_from

from application.structure import structure


polls_blueprint = Blueprint("polls_v1", __name__, url_prefix="/v1/polls")
base_swagger_path = "./../../swagger/polls"


@polls_blueprint.route("", methods=["POST"])
@swag_from(f"{base_swagger_path}/create_poll.yml")
def create_poll():
    return structure.create_poll_handler.handle(request)
