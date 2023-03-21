import os

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from application.blueprints import general_blueprint
from application.blueprints.v1 import auth_blueprint


application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*"}})
swagger = Swagger(
    application,
    template_file=f"{os.getcwd()}/application/swagger/template.yml"
)

application.register_blueprint(general_blueprint)
application.register_blueprint(auth_blueprint)
