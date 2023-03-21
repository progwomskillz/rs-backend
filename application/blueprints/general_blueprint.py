import json

from flask import Blueprint, Response
from flasgger import swag_from


general_blueprint = Blueprint("general", __name__)
base_swagger_path = "./../swagger/general"


@general_blueprint.route("/health_check", methods=["GET"])
@swag_from(f"{base_swagger_path}/health_check.yml")
def health_check():
    return Response(
        response=json.dumps({"message": "Healthy"}),
        status=200,
        mimetype="application/json"
    )
