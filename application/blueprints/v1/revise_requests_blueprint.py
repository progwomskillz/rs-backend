from flask import Blueprint, request
from flasgger import swag_from

from application.structure import structure


revise_requests_blueprint = Blueprint(
    "revise_requests_v1",
    __name__,
    url_prefix="/v1/revise-requests"
)
base_swagger_path = "./../../swagger/revise_requests"


@revise_requests_blueprint.route("", methods=["POST"])
@swag_from(f"{base_swagger_path}/create_revise_request.yml")
def create_revise_request():
    return structure.create_revise_request_handler.handle(request)
